#!/usr/bin/env python3
"""Generate HTML page from addon data using Jinja2 template."""

import json
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def main():
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "output"
    template_dir = base_dir / "templates"

    # Load addon data
    data_file = output_dir / "addons_data.json"
    with open(data_file) as f:
        data = json.load(f)

    # Group addons by type
    addons_by_type = {}
    for addon in data["addons"]:
        addon_type = addon["type"] or "other"
        if addon_type not in addons_by_type:
            addons_by_type[addon_type] = []
        addons_by_type[addon_type].append(addon)

    # Sort types and addons within each type
    sorted_types = sorted(addons_by_type.keys())

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("index.html.j2")

    # Render template
    html = template.render(
        eks_versions=data["eks_versions"],
        addons=data["addons"],
        addons_by_type=addons_by_type,
        sorted_types=sorted_types,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    )

    # Write output
    output_file = output_dir / "index.html"
    with open(output_file, "w") as f:
        f.write(html)

    print(f"Generated {output_file}")


if __name__ == "__main__":
    main()
