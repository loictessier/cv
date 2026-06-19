# CV Generator

Small personal tool to generate CV-related documents from structured YAML data.

The idea is to keep my CV information in one place, then use templates to generate different outputs depending on the need: a full CV, a company profile form, or later a static HTML version for my personal website.

## How it works

The project is based on three main steps:

1. Read CV data from YAML files.
2. Inject this data into Jinja2 templates.
3. Generate the output files in `build/`.

Some templates are simple Markdown files meant to be copied into external documents. Others may be used to generate HTML or PDF versions of the CV.

## Pipelines

### Profile forms

Profile forms are Markdown templates used for company-specific skill sheets or recruiter documents.

They usually stop at the Markdown generation step, because the result is mostly meant to be copied into another format.

```text
YAML → Jinja2 template → Markdown
```

### Markdown CV

The Markdown CV pipeline generates a full CV from a Markdown template.

The generated Markdown can then be converted to HTML, and the HTML can also be used to generate a PDF with WeasyPrint.

```text
YAML → Jinja2 template → Markdown → HTML → PDF
```

### Quarkdown

A Quarkdown pipeline may also be used later.

In that case, Jinja2 generates a Quarkdown file, then the Quarkdown CLI handles the final rendering.

```text
YAML → Jinja2 template → Quarkdown → HTML/PDF
```

## Project structure

```text
data/
  template.yaml
  private/
templates/
  markdown/
    cv.md.j2
    profile_forms/
      company.md.j2
  quarkdown/
    cv.qd.j2
src/
  main.py
build/
```
