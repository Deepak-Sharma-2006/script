# Progressive Disclosure Skill Library

This directory contains specialized workflows, cheatsheets, and domain capabilities dynamically retrieved by agents via `npm run skill:search` or `scripts/skill-finder.ts`.

## Structure
Each subfolder represents a self-contained skill containing a `SKILL.md` file with YAML frontmatter specifying its name, trigger criteria, and operational directives.

## Progressive Loading
To preserve token economy and prevent prompt saturation, skills are discovered dynamically on demand and boundedly viewed via slice ranges rather than loaded in bulk.
