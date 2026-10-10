import { existsSync, readFileSync, readdirSync, statSync } from "fs";
import { join } from "path";

const NODE_BUILTINS = new Set([
  "assert", "async_hooks", "buffer", "child_process", "cluster", "console",
  "constants", "crypto", "dgram", "diagnostics_channel", "dns", "domain",
  "events", "fs", "fs/promises", "http", "http2", "https", "inspector",
  "module", "net", "os", "path", "path/posix", "path/win32", "perf_hooks",
  "process", "punycode", "querystring", "readline", "repl", "stream",
  "stream/promises", "stream/web", "string_decoder", "sys", "timers",
  "timers/promises", "tls", "trace_events", "tty", "url", "util",
  "util/types", "v8", "vm", "wasi", "worker_threads", "zlib", "test", "sqlite"
]);

const PYTHON_BUILTINS = new Set([
  "abc", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore", "atexit",
  "audioop", "base64", "bdb", "binascii", "binhex", "bisect", "builtins", "bz2",
  "cProfile", "calendar", "cgi", "cgitb", "chunk", "cmath", "cmd", "code",
  "codecs", "codeop", "collections", "colorsys", "compileall", "concurrent",
  "configparser", "contextlib", "contextvars", "copy", "copyreg", "crypt",
  "csv", "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal",
  "difflib", "dis", "distutils", "doctest", "dummy_threading", "email",
  "encodings", "ensurepip", "enum", "errno", "faulthandler", "fcntl", "filecmp",
  "fileinput", "fnmatch", "formatter", "fpectl", "fractions", "ftplib",
  "functools", "gc", "getopt", "getpass", "gettext", "glob", "graphlib",
  "grp", "gzip", "hashlib", "heapq", "hmac", "html", "http", "imaplib",
  "imghdr", "imp", "importlib", "inspect", "io", "ipaddress", "itertools",
  "json", "keyword", "lib2to3", "linecache", "locale", "logging", "lzma",
  "mailbox", "mailcap", "marshal", "math", "mimetypes", "mmap", "modulefinder",
  "msilib", "msvcrt", "multiprocessing", "netrc", "nis", "nntplib", "numbers",
  "operator", "optparse", "os", "ossaudiodev", "parser", "pathlib", "pdb",
  "pickle", "pickletools", "pipes", "pkgutil", "platform", "plistlib", "poplib",
  "posix", "posixpath", "pprint", "profile", "pstats", "pty", "pwd", "py_compile",
  "pyclbr", "pydoc", "queue", "quopri", "random", "re", "readline", "reprlib",
  "resource", "rlcompleter", "runpy", "sched", "secrets", "select", "selectors",
  "shelve", "shlex", "shutil", "signal", "site", "smtpd", "smtplib", "sndhdr",
  "socket", "socketserver", "spwd", "sqlite3", "sre", "ssl", "stat", "statistics",
  "string", "stringprep", "struct", "subprocess", "sunau", "symbol", "symtable",
  "sys", "sysconfig", "syslog", "tabnanny", "tarfile", "telnetlib", "tempfile",
  "termios", "test", "textwrap", "threading", "time", "timeit", "tkinter",
  "token", "tokenize", "tomllib", "trace", "traceback", "tracemalloc", "tty",
  "turtle", "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib",
  "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser", "winreg",
  "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile",
  "zipimport", "zlib", "_thread", "ntpath"
]);

const PYTHON_IMPORT_ALIASES: Record<string, string[]> = {
  "scikit-learn": ["sklearn"],
  "python-pptx": ["pptx"],
  "pillow": ["PIL"],
  "pyyaml": ["yaml"],
  "pytest-cov": ["pytest_cov"],
  "opencv-python": ["cv2"],
  "pymupdf": ["fitz"],
  "pywin32": ["win32com"],
  "segmentation-models-pytorch": ["segmentation_models_pytorch", "smp"],
};

export function getDeclaredDependencies(projectRoot: string): Set<string> {
  const pkgPath = join(projectRoot, "package.json");
  const declared = new Set<string>();

  if (!existsSync(pkgPath)) {
    return declared;
  }

  try {
    const pkg = JSON.parse(readFileSync(pkgPath, "utf-8"));
    if (pkg.dependencies) {
      Object.keys(pkg.dependencies).forEach((dep) => declared.add(dep));
    }
    if (pkg.devDependencies) {
      Object.keys(pkg.devDependencies).forEach((dep) => declared.add(dep));
    }
    if (pkg.peerDependencies) {
      Object.keys(pkg.peerDependencies).forEach((dep) => declared.add(dep));
    }
  } catch {
    // Malformed package.json
  }

  return declared;
}

export function getDeclaredPythonDependencies(projectRoot: string): Set<string> {
  const reqPath = join(projectRoot, "requirements.txt");
  const declared = new Set<string>([
    "scripts", "src", "tests", "templates", "specs", "torch", "torchvision", "torchaudio"
  ]);

  if (!existsSync(reqPath)) {
    return declared;
  }

  try {
    const lines = readFileSync(reqPath, "utf-8").split("\n");
    for (const rawLine of lines) {
      const line = rawLine.trim();
      if (!line || line.startsWith("#")) continue;
      const cleanPkg = line.split(/[=<>~!@\s]/)[0].toLowerCase().trim();
      if (cleanPkg) {
        declared.add(cleanPkg);
        declared.add(cleanPkg.replace(/-/g, "_"));
        if (PYTHON_IMPORT_ALIASES[cleanPkg]) {
          for (const alias of PYTHON_IMPORT_ALIASES[cleanPkg]) {
            declared.add(alias);
          }
        }
      }
    }
  } catch {
    // Malformed requirements.txt
  }

  return declared;
}

function extractImports(fileContent: string): string[] {
  // Strip single-line and multi-line comments first to prevent matching in comments
  const strippedContent = fileContent
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/\/\/.*/g, "");

  const imports: string[] = [];
  const importRegex = /(?:import\s+(?:[\w*\s{},]*\s+from\s+)?['"]([^'"]+)['"])|(?:require\(['"]([^'"]+)['"]\))/g;
  let match;

  while ((match = importRegex.exec(strippedContent)) !== null) {
    const specifier = match[1] || match[2];
    if (specifier) {
      imports.push(specifier);
    }
  }

  return imports;
}

function extractPythonImports(fileContent: string): string[] {
  // Strip multiline docstrings and triple-quoted code templates
  const strippedContent = fileContent
    .replace(/"""[\s\S]*?"""/g, "")
    .replace(/'''[\s\S]*?'''/g, "");

  const imports: string[] = [];
  const lines = strippedContent.split("\n");

  for (const rawLine of lines) {
    const line = rawLine.replace(/#.*$/, "").trim();
    if (!line) continue;

    // Matches: from package.sub import foo
    const fromMatch = line.match(/^from\s+([a-zA-Z0-9_.]+)\s+import/);
    if (fromMatch && fromMatch[1]) {
      const topPkg = fromMatch[1].split(".")[0];
      if (topPkg && /^[a-zA-Z_][a-zA-Z0-9_]*$/.test(topPkg)) {
        imports.push(topPkg);
      }
      continue;
    }

    // Matches: import package, package2
    const importMatch = line.match(/^import\s+([a-zA-Z0-9_.,\s]+)$/);
    if (importMatch && importMatch[1]) {
      // Must not contain 'from' which indicates JS/TS import syntax
      if (importMatch[1].includes(" from ")) continue;

      const pkgs = importMatch[1].split(",");
      for (const p of pkgs) {
        const clean = p.trim().split(/\s+as\s+/)[0].trim().split(".")[0];
        if (clean && /^[a-zA-Z_][a-zA-Z0-9_]*$/.test(clean)) {
          imports.push(clean);
        }
      }
    }
  }

  return imports;
}

export function validateFileImports(filePath: string, declaredDeps: Set<string>): { valid: boolean; ghostDependencies: string[] } {
  const content = readFileSync(filePath, "utf-8");
  const imports = extractImports(content);
  const ghostDependencies: string[] = [];

  for (const imp of imports) {
    if (imp.startsWith(".") || imp.startsWith("/") || imp.startsWith("\\")) {
      continue;
    }

    let packageName = imp;
    if (imp.startsWith("@")) {
      const parts = imp.split("/");
      packageName = parts.slice(0, 2).join("/");
    } else {
      packageName = imp.split("/")[0];
    }

    const cleanName = packageName.replace(/^node:/, "");
    if (NODE_BUILTINS.has(cleanName)) {
      continue;
    }

    if (!declaredDeps.has(packageName)) {
      ghostDependencies.push(packageName);
    }
  }

  return {
    valid: ghostDependencies.length === 0,
    ghostDependencies,
  };
}

export function validatePythonFileImports(filePath: string, declaredPyDeps: Set<string>): { valid: boolean; ghostDependencies: string[] } {
  const content = readFileSync(filePath, "utf-8");
  const imports = extractPythonImports(content);
  const ghostDependencies: string[] = [];

  for (const pkg of imports) {
    if (pkg.startsWith(".")) continue;
    if (PYTHON_BUILTINS.has(pkg)) continue;

    if (!declaredPyDeps.has(pkg.toLowerCase()) && !declaredPyDeps.has(pkg)) {
      ghostDependencies.push(pkg);
    }
  }

  return {
    valid: ghostDependencies.length === 0,
    ghostDependencies,
  };
}

export function scanDirectory(
  dir: string,
  declaredDeps: Set<string>,
  declaredPyDeps: Set<string> = getDeclaredPythonDependencies(process.cwd())
): boolean {
  console.log(`🔍 [Anti-Hallucination] Scanning directory: ${dir}`);
  let hasErrors = false;

  function walk(currentDir: string): void {
    if (!existsSync(currentDir)) return;
    const items = readdirSync(currentDir);

    for (const item of items) {
      if (item === "node_modules" || item === ".git" || item === "dist" || item === "build" || item === "skills" || item === "__pycache__" || item === ".venv") {
        continue;
      }
      const fullPath = join(currentDir, item);
      const stat = statSync(fullPath);

      if (stat.isDirectory()) {
        walk(fullPath);
      } else if (stat.isFile()) {
        if (item.endsWith(".ts") || item.endsWith(".tsx") || item.endsWith(".js") || item.endsWith(".jsx")) {
          const result = validateFileImports(fullPath, declaredDeps);
          if (!result.valid) {
            hasErrors = true;
            console.error(`\n🚨 HALLUCINATION DETECTED in ${fullPath}:`);
            for (const ghost of result.ghostDependencies) {
              console.error(`   ❌ Ghost Dependency: '${ghost}' is imported but NOT declared in package.json!`);
            }
          }
        } else if (item.endsWith(".py")) {
          const result = validatePythonFileImports(fullPath, declaredPyDeps);
          if (!result.valid) {
            hasErrors = true;
            console.error(`\n🚨 HALLUCINATION DETECTED in ${fullPath}:`);
            for (const ghost of result.ghostDependencies) {
              console.error(`   ❌ Ghost Dependency: '${ghost}' is imported but NOT declared in requirements.txt!`);
            }
          }
        }
      }
    }
  }

  walk(dir);

  if (hasErrors) {
    console.error(`\n❌ Anti-Hallucination Shield: Process failed! Remove phantom imports or declare in dependencies.`);
    return false;
  }

  console.log("✅ Anti-Hallucination Shield: Zero ghost dependencies detected.");
  return true;
}

import { fileURLToPath } from "node:url";

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("anti-hallucination-checker.ts") ||
  process.argv[1].endsWith("anti-hallucination-checker.js")
);

if (isMain) {
  const root = process.cwd();
  const declared = getDeclaredDependencies(root);
  const declaredPy = getDeclaredPythonDependencies(root);
  const rawArgs = process.argv.slice(2);
  const targets = rawArgs.length > 0 ? rawArgs : ["scripts", "src", "tests", "browser_tests"];
  let allOk = true;

  for (const t of targets) {
    const fullPath = join(root, t);
    if (existsSync(fullPath)) {
      const ok = scanDirectory(fullPath, declared, declaredPy);
      if (!ok) allOk = false;
    }
  }

  process.exit(allOk ? 0 : 1);
}
