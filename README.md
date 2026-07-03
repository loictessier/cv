# CV Generator

Small personal tool to generate CV-related documents from structured YAML data.

The idea is to keep my CV information in one place, then use templates to generate different outputs depending on the need: a full CV, a company profile form, an HTML page, or a PDF version.

## How it works

The project is based on a simple flow:

```text
YAML data → Jinja2 template → Markdown → HTML → PDF
```

The main script reads a YAML file, renders a Markdown template with Jinja2, then generates:

* a Markdown file
* an HTML page
* a PDF file

Generated files are written to `build/`.

## Usage

Install dependencies:

```bash
pipenv install
```

Generate the default CV:

```bash
pipenv run python src/main.py
```

By default, this uses:

```text
data/template.yaml
templates/markdown/cv.md.j2
build/cv.md
```

It also generates:

```text
build/cv/index.html
build/cv/style.css
build/cv/cv.pdf
```

You can override the input data, Markdown template, and Markdown output:

```bash
pipenv run python src/main.py \
  --input data/private/loictessier.yaml \
  --template templates/markdown/cv-with-contact.md.j2 \
  --output build/cv.md
```

## Templates

Markdown templates are stored in:

```text
templates/markdown/
```

Current CV templates:

```text
templates/markdown/cv.md.j2
templates/markdown/cv-with-contact.md.j2
```

Profile form templates are also Markdown templates, but they are intended for company-specific skill sheets:

```text
templates/markdown/profile_forms/
```

Examples:

```text
templates/markdown/profile_forms/fortil.md.j2
templates/markdown/profile_forms/celad.md.j2
```

The HTML wrapper and CSS used for the CV rendering are stored together:

```text
templates/html/cv/
  page.html.j2
  style.css
```

The generated Markdown is converted to HTML, then inserted into `page.html.j2`. The CSS file is copied to the generated output folder.

## Pipelines

### Profile forms

Profile forms usually stop at the Markdown step.

```text
YAML → Jinja2 Markdown template → Markdown
```

They are useful for content that will be copied into external documents or recruiter/company forms.

### CV Markdown / HTML / PDF

The main CV pipeline generates a Markdown CV first, then converts it to HTML and PDF.

```text
YAML → Jinja2 Markdown template → Markdown → HTML → PDF
```

The Markdown conversion uses Python-Markdown with the `extra` and `attr_list` extensions.

The PDF is generated from the final HTML with WeasyPrint.

### Quarkdown

A Quarkdown template folder exists for future experiments:

```text
templates/quarkdown/
```

This pipeline is not currently handled by `main.py`.

## Project structure

```text
.
├── data/
│   ├── template.yaml
│   └── private/
│
├── src/
│   └── main.py
│
├── templates/
│   ├── html/
│   │   └── cv/
│   │       ├── page.html.j2
│   │       └── style.css
│   │
│   ├── markdown/
│   │   ├── cv.md.j2
│   │   ├── cv-with-contact.md.j2
│   │   └── profile_forms/
│   │       ├── celad.md.j2
│   │       └── fortil.md.j2
│   │
│   └── quarkdown/
│       └── cv.qd.j2
│
└── build/
```

## Private data and generated files

Private YAML files are kept under:

```text
data/private/
```

This folder is ignored by Git, except for `.gitkeep`.

Generated files are written under:

```text
build/
```

The `build/` folder is also ignored by Git, except for `.gitkeep`.

PDF and HTML outputs are ignored as well.

This keeps private data and generated artifacts out of version control.
