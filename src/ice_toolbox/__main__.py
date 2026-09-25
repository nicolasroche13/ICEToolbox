"""Entry point for `python -m ice_toolbox`."""

import sys

from ice_toolbox.app.application import Application


def main() -> int:
    app = Application()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
