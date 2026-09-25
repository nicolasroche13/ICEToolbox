# ICE Toolbox

ICE Toolbox is a desktop application built with Python and PySide6. This is
the initial foundation of the project: a clean, minimal, testable base with
no business features yet.

## Requirements

- Python 3.12 or later
- Git

## Setup

Create and activate a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
```

Install the project and its dependencies (editable install):

```bash
pip install -e ".[dev]"
```

## Running ICE Toolbox

```bash
python -m ice_toolbox
```

This opens a window displaying "ICE Toolbox" and the current version.

## Running the tests

```bash
pytest
```

All tests must pass before any commit is considered stable.

## Git workflow

The project uses a simple branching model:

```
main
  ↑
develop
  ↑
feature/nom-fonctionnalite
```

- `main` — always stable.
- `develop` — integration branch for validated work.
- `feature/*` — one branch per feature (e.g. `feature/intune-device-search`).
- `fix/*` — one branch per bug fix (e.g. `fix/window-title`).

Never commit directly to `main`. Development happens in `feature/*` branches,
merged into `develop`, which is later merged into `main` once validated.

### Commits

Commits follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: ...
fix: ...
test: ...
docs: ...
refactor: ...
chore: ...
```

## Versioning

The project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).
The single source of truth for the version number is the `VERSION` file at
the project root.
