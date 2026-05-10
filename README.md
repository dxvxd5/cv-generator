# cv-generator

Generate a typeset PDF CV from a JSON file using a LaTeX template.

The bundled `prometheus` template is adapted (with modifications) from
[chrisby/prometheusCV](https://github.com/chrisby/prometheusCV).
See [examples/cv.example.pdf](examples/cv.example.pdf) for what the output looks like.

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/) for dependency management
- A working LaTeX toolchain with `latexmk` and `lualatex`
  - macOS: `brew install --cask mactex` (or `mactex-no-gui`)
  - Debian/Ubuntu: `sudo apt install texlive-full latexmk`
- Fonts used by the Prometheus template:
  - [Cormorant Garamond](https://github.com/CatharsisFonts/Cormorant)
  - The `fontawesome5` LaTeX package (bundled with most TeX distributions)

## Install

```sh
poetry install
```

## Usage

```sh
poetry run python src/main.py <json cv> [-o output.pdf] [-t prometheus] [--no-escape]
```

Try it with the bundled example:

```sh
poetry run python src/main.py examples/cv.example.json -o /tmp/cv.pdf
```

Options:

| Flag             | Description                                                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| `-o, --output`   | Path to the generated PDF. Defaults to the input path with a `.pdf` extension.                              |
| `-t, --template` | Template to use. Currently only `prometheus`.                                                               |
| `--no-escape`    | Skip escaping LaTeX special characters in the input (use only if your JSON already contains escaped LaTeX). |

## JSON schema

The input is validated against [src/schema/cv.schema.json](src/schema/cv.schema.json) before any LaTeX is generated. Any structural issues (missing fields, wrong types, unknown keys) are reported up front with their JSON path. The input file must be a JSON object with the following top-level sections:

```jsonc
{
  "user":        { ... },           // required
  "education":   [ { ... }, ... ],  // required (may be empty)
  "experiences": [ { ... }, ... ],  // required (may be empty)
  "projects":    [ { ... }, ... ],  // required (may be empty)
  "skills":      [ { ... }, ... ]   // required (may be empty)
}
```

See [examples/cv.example.json](examples/cv.example.json) for a complete, working example.

### `user`

| Field            | Required | Notes                                                        |
| ---------------- | -------- | ------------------------------------------------------------ |
| `firstName`      | yes      |                                                              |
| `lastName`       | yes      |                                                              |
| `city`           | yes      |                                                              |
| `country`        | yes      |                                                              |
| `email`          | yes      |                                                              |
| `linkedinUrl`    | no       | If omitted, the LinkedIn icon is hidden.                     |
| `githubUrl`      | no       | Hidden unless both `githubUrl` and `githubUsername` are set. |
| `githubUsername` | no       |                                                              |

### `education[]`

Required: `startDate`, `endDate`, `city`, `country`, `school`, `degree`, `description` (list of strings).

### `experiences[]`

Required: `startDate`, `endDate`, `city`, `country`, `companyName`, `title`, `description`.
Optional: `companyLink` (renders the company name as a hyperlink).

### `projects[]`

Required: `startDate`, `endDate`, `city`, `country`, `context`, `title`, `description`, `link` (use `""` for no link).

### `skills[]`

Required: `area` (e.g. `"Languages"`), `skills` (list of strings).

## Tests

```sh
poetry run pytest
```
