"""Pytest configuration: force an offscreen Qt platform for headless test runs."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
