#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import sys
import os

from internals.config import wrapper as config_wrapper
from internals.app import ascii_art


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nazri.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    ascii_art.project_name()
    main()
