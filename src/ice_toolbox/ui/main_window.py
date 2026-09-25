"""Main application window."""

from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget

from ice_toolbox.core.config import APP_NAME, get_version


class MainWindow(QMainWindow):
    """Minimal main window displaying the application name and version."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(QLabel(APP_NAME))
        layout.addWidget(QLabel(f"Version {get_version()}"))

        self.setCentralWidget(central_widget)
