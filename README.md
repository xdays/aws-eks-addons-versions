# AWS EKS Addon Versions

A compatibility matrix showing supported addon versions for each AWS EKS Kubernetes version.

**Live site:** https://aws-eks-addons-versions.pages.dev

## Features

- Complete version matrix for all AWS EKS addons
- Filterable by addon type (networking, storage, observability, etc.)
- Searchable addon list
- Auto-updated via GitHub Actions

## Development

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- AWS credentials configured

### Setup

```bash
uv sync
```

### Usage

Fetch addon data from AWS:

```bash
uv run python scripts/fetch_addons.py
```

Generate HTML page:

```bash
uv run python scripts/generate_html.py
```

### Deploy

Deploy to Cloudflare Pages:

```bash
npx wrangler pages deploy output --project-name=aws-eks-addons-versions
```

## Project Structure

```
.
├── scripts/
│   ├── fetch_addons.py    # Fetches addon data from AWS EKS API
│   └── generate_html.py   # Generates static HTML from data
├── templates/
│   └── index.html.j2      # Jinja2 template for the web page
├── output/
│   ├── addons_data.json   # Fetched addon data
│   └── index.html         # Generated static site
├── pyproject.toml         # Project dependencies
└── uv.lock                # Locked dependencies
```

## License

MIT
