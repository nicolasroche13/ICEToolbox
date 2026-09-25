# Architecture

This document describes the current architecture of ICE Toolbox. It reflects
only what exists today — no planned or future components.

## Overview

ICE Toolbox is a desktop application built with Python and PySide6 (Qt).
At this stage, it is a minimal foundation: a single window displaying the
application name and version.

## Package layout

```
src/ice_toolbox/
├── __main__.py       Entry point for `python -m ice_toolbox`
├── app/               Application bootstrap and lifecycle (Qt app + main window)
├── ui/                Graphical interface only (windows, widgets)
│   └── widgets/       Reusable UI widgets (currently empty)
├── core/              Cross-cutting components: configuration, logging
└── services/          Placeholder for future external service integrations
```

## Layer responsibilities

- **`app/`** — Owns the `QApplication` instance and the main window's
  lifecycle. This is the only place that starts/stops the Qt event loop.
- **`ui/`** — Contains only graphical interface code. No business logic,
  no external service calls.
- **`core/`** — Cross-cutting, framework-agnostic components shared across
  the application: configuration constants and logging setup.
- **`services/`** — Reserved for future communication with external
  services (e.g. Microsoft Graph, Intune, Entra ID). Empty at this stage,
  by design.

## Versioning

The application version has a single source of truth: the `VERSION` file
at the project root. `pyproject.toml` reads it via `tool.setuptools.dynamic`
to populate the package's installed metadata, and `ice_toolbox.core.config`
reads that metadata at runtime via `importlib.metadata`. No version number
is hardcoded anywhere else in the code.

## Explicit non-goals (for this version)

- No Microsoft Graph, Intune, or Entra ID integration.
- No repository pattern, dependency injection framework, or event bus.
- No configuration persistence, settings UI, or secrets handling.

These will be introduced only when a real, concrete need justifies them.
