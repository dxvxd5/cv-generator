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
| `-t, --template` | Template to use. Defaults to `prometheus`. See [Adding a template](#adding-a-template).                     |
| `--no-escape`    | Skip escaping LaTeX special characters in the input (use only if your JSON already contains escaped LaTeX). |

## JSON schema

The input is validated against [src/schema/cv.schema.json](src/schema/cv.schema.json) before any LaTeX is generated. Any structural issues (missing fields, wrong types, unknown keys) are reported up front with their JSON path. The input file must be a JSON object with the following top-level sections:

```jsonc
{
  "user":        { ... },           // required
  "education":   [ { ... }, ... ],  // optional; omit or pass [] to hide the section
  "experiences": [ { ... }, ... ],  // optional; omit or pass [] to hide the section
  "projects":    [ { ... }, ... ],  // optional; omit or pass [] to hide the section
  "skills":      [ { ... }, ... ]   // optional; omit or pass [] to hide the section
}
```

`user` is required, and at least one of `education`, `experiences` or `projects` must contain at least one entry. Any section that is omitted (or empty) is skipped entirely — no heading is rendered for it.

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

## Adding a template

Templates are auto-discovered from `src/converters/`. To add one named `mytheme`:

1. Create `src/converters/mytheme/` with your converter class and any LaTeX assets it needs (e.g. `templates/mytheme/main.tex`, `.cls` files).
2. Implement a converter class. The only contract required by the CLI is a single method:

   ```python
   class MyThemeConverter:
       @staticmethod
       def generate_latex_files(cv: CV, output_folder: str) -> str:
           """
           Render `cv` into LaTeX files under `output_folder` and return the
           absolute path of the main `.tex` file to compile.
           """
           ...
   ```

   `cv` is a [`CV`](src/sections/cv.py) instance exposing `user`, `education`, `experiences`, `projects`, `skills`. Use the [`Latex`](src/utils/latex.py) helpers (`escape`, `join`, `bold`, `link`, `build_command`, …) so escaping stays consistent — pass raw strings in and let the helpers escape display content. See [src/converters/prometheus/prometheus.py](src/converters/prometheus/prometheus.py) for a full example.

3. Expose the converter in `src/converters/mytheme/__init__.py`:

   ```python
   from converters.mytheme.mytheme import MyThemeConverter

   CONVERTER = MyThemeConverter
   ```

4. Run with `--template mytheme`. The CLI's `--template` choices are derived from the registry, so no other code changes are required.

## Tests

```sh
poetry run pytest
```
