from pathlib import Path
import argparse
import shutil

import yaml
from jinja2 import Environment, FileSystemLoader
import markdown
from weasyprint import HTML


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def flatten(items):
    result = []
    for item in items:
        if item:
            result.extend(item)
    return result


def generate_html_from_markdown(markdown_file, html_template_dir, output_dir, data):
    markdown_file = Path(markdown_file)
    html_template_dir = Path(html_template_dir)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    markdown_content = markdown_file.read_text(encoding="utf-8")

    html_content = markdown.markdown(
        markdown_content,
        extensions=["extra", "attr_list"]
    )

    env = Environment(
        loader=FileSystemLoader(str(html_template_dir)),
        autoescape=True
    )

    template = env.get_template("page.html.j2")

    final_html = template.render(
        **data,
        content=html_content
    )

    (output_dir / "index.html").write_text(final_html, encoding="utf-8")

    shutil.copyfile(
        html_template_dir / "style.css",
        output_dir / "style.css"
    )


def generate_pdf_from_html(html_file, output_pdf):
    html_file = Path(html_file)
    output_pdf = Path(output_pdf)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    HTML(
        filename=str(html_file),
        base_url=str(html_file.parent)
    ).write_pdf(str(output_pdf))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="data/template.yaml",
        help="Path to the YAML input file",
    )
    parser.add_argument(
        "--template",
        default="templates/markdown/cv.md.j2",
        help="Path to the Jinja2 template",
    )
    parser.add_argument(
        "--output",
        default="build/cv.md",
        help="Path to the generated output file",
    )

    args = parser.parse_args()

    data_file = PROJECT_ROOT / args.input
    template_file = PROJECT_ROOT / args.template
    output_file = PROJECT_ROOT / args.output

    with open(data_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    env = Environment(
        loader=FileSystemLoader(template_file.parent),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    env.filters["flatten"] = flatten

    template = env.get_template(template_file.name)
    rendered = template.render(**data)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(rendered, encoding="utf-8")

    print("Generated Markdown: {}".format(output_file))

    generate_html_from_markdown(
        markdown_file=output_file,
        html_template_dir=PROJECT_ROOT / "templates/html/cv",
        output_dir=PROJECT_ROOT / "build/cv",
        data=data
    )

    print("Generated HTML: {}".format(PROJECT_ROOT / "build/cv/index.html"))

    generate_pdf_from_html(
        html_file=PROJECT_ROOT / "build/cv/index.html",
        output_pdf=PROJECT_ROOT / "build/cv/cv.pdf"
    )

    print("Generated PDF: {}".format(PROJECT_ROOT / "build/cv/cv.pdf"))


if __name__ == "__main__":
    main()