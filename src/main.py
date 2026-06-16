from pathlib import Path
import argparse

import yaml
from jinja2 import Environment, FileSystemLoader


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="data/template.yaml",
        help="Path to the YAML input file",
    )
    parser.add_argument(
        "--template",
        default="templates/profile_forms/fortil.md.j2",
        help="Path to the Jinja2 template",
    )
    parser.add_argument(
        "--output",
        default="build/fortil.md",
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

    template = env.get_template(template_file.name)
    rendered = template.render(**data)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(rendered, encoding="utf-8")

    print("Generated: {}".format(output_file))


if __name__ == "__main__":
    main()