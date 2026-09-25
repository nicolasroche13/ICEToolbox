"""Application bootstrap and lifecycle."""

import sys

from PySide6.QtWidgets import QApplication

from ice_toolbox.core.logging import setup_logging
from ice_toolbox.ui.main_window import MainWindow


class Application:
    """Owns the Qt application instance and the main window lifecycle."""

    def __init__(self) -> None:
        setup_logging()
        self._qt_app = QApplication.instance() or QApplication(sys.argv)
        self._main_window = MainWindow()

    def run(self) -> int:
        """Show the main window and start the Qt event loop."""
        self._main_window.show()
        return self._qt_app.exec()
