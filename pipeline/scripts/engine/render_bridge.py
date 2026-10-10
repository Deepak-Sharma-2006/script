"""
Presentation Engine — Render Bridge
Automates PowerPoint COM PDF export and PyMuPDF high-resolution PNG rendering.
"""

import os
import sys
import subprocess
from typing import List
import pymupdf

try:
    import win32com.client
    HAS_WIN32COM = True
except ImportError:
    HAS_WIN32COM = False

from scripts.engine.schema import DeckManifest
from scripts.engine.pptx_compiler import PPTXCompiler


def export_pptx_to_pdf(pptx_path: str, pdf_path: str) -> str:
    """Exports a PPTX file to PDF using PowerPoint COM on Windows or headless fallback on Linux/macOS."""
    abs_pptx = os.path.abspath(pptx_path)
    abs_pdf = os.path.abspath(pdf_path)
    os.makedirs(os.path.dirname(abs_pdf), exist_ok=True)

    if HAS_WIN32COM and sys.platform == "win32":
        try:
            print(f"Exporting {abs_pptx} to PDF via PowerPoint COM...")
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            try:
                deck = powerpoint.Presentations.Open(abs_pptx, WithWindow=False)
                # 32 = ppSaveAsPDF
                deck.SaveAs(abs_pdf, 32)
                deck.Close()
                print(f"PDF exported successfully -> {abs_pdf}")
                return abs_pdf
            finally:
                powerpoint.Quit()
        except Exception as com_err:
            print(f"⚠️ PowerPoint COM automation failed: {com_err}. Attempting portable fallback...")

    # Portable Cross-Platform Fallback (LibreOffice or Headless Chrome/Playwright)
    print(f"Attempting portable headless PDF export for {abs_pptx}...")
    try:
        res = subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", abs_pptx, "--outdir", os.path.dirname(abs_pdf)], capture_output=True, timeout=30)
        if res.returncode == 0 and os.path.exists(abs_pdf):
            print(f"PDF exported via LibreOffice -> {abs_pdf}")
            return abs_pdf
    except Exception:
        pass

    raise RuntimeError(
        f"PDF export requires either desktop Microsoft PowerPoint on Windows, LibreOffice in PATH, "
        f"or the standalone HTML presentation deck compiler (scripts/engine/html_deck_compiler.py)."
    )


def render_pdf_to_images(pdf_path: str, output_dir: str, prefix: str = "slide", dpi: int = 200) -> List[str]:
    """Renders all pages of a PDF into high-resolution PNG images."""
    abs_pdf = os.path.abspath(pdf_path)
    abs_out_dir = os.path.abspath(output_dir)
    os.makedirs(abs_out_dir, exist_ok=True)

    rendered_files = []
    doc = pymupdf.open(abs_pdf)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        out_png = os.path.join(abs_out_dir, f"{prefix}_{i+1}.png")
        pix.save(out_png)
        rendered_files.append(out_png)
        print(f"Rendered Page {i+1} -> {out_png} ({pix.width}x{pix.height})")

    return rendered_files


def compile_and_render_deck(
    manifest: DeckManifest,
    pptx_path: str,
    pdf_path: str,
    render_dir: str,
    slide_prefix: str = "slide",
    dpi: int = 200
) -> List[str]:
    """
    End-to-End Orchestrator:
    1. Compiles DeckManifest to PPTX using native PowerPoint shapes.
    2. Exports PPTX to PDF via PowerPoint COM.
    3. Renders PDF to high-resolution PNGs via PyMuPDF.
    """
    compiler = PPTXCompiler(manifest)
    compiler.compile(pptx_path)

    export_pptx_to_pdf(pptx_path, pdf_path)
    rendered_images = render_pdf_to_images(pdf_path, render_dir, prefix=slide_prefix, dpi=dpi)
    return rendered_images


class RenderBridge:
    """Class wrapper for render operations."""
    export_pptx_to_pdf = staticmethod(export_pptx_to_pdf)
    render_pdf_to_images = staticmethod(render_pdf_to_images)
    compile_and_render_deck = staticmethod(compile_and_render_deck)
