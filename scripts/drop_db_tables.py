"""Drop specific app tables and their migration records.

CAUTION: This is destructive and will permanently delete data. Ensure you
have a backup before running. The script uses Django DB settings from
`DJANGO_SETTINGS_MODULE` (defaults to `backend.settings` when run from
project root with manage.py). It prints each statement before executing.
"""
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so Python can import the project package
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Ensure we can import Django project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from django.db import connection, transaction


SQL_STATEMENTS = [
    "DROP TABLE IF EXISTS courses_review CASCADE;",
    "DROP TABLE IF EXISTS courses_userlessonprogress CASCADE;",
    "DROP TABLE IF EXISTS courses_lesson CASCADE;",
    "DROP TABLE IF EXISTS courses_module CASCADE;",
    "DROP TABLE IF EXISTS courses_course CASCADE;",
    "DROP TABLE IF EXISTS courses_category CASCADE;",
    "DROP TABLE IF EXISTS enrollments_enrollment CASCADE;",
    # Remove migration records so Django can reapply migrations cleanly
    "DELETE FROM django_migrations WHERE app IN ('courses','enrollments');",
]


def main(dry_run=False):
    print("Running drop_db_tables.py")
    with connection.cursor() as cursor:
        for sql in SQL_STATEMENTS:
            print('\n-- Executing:\n', sql)
            if not dry_run:
                try:
                    cursor.execute(sql)
                except Exception as e:
                    print(f"ERROR executing SQL: {e}")
                    raise
    # commit if not in autocommit
    try:
        if not connection.get_autocommit():
            transaction.commit()
    except Exception:
        pass


if __name__ == '__main__':
    # allow optional --dry-run flag
    dry = '--dry-run' in sys.argv
    if dry:
        print('Dry run mode - statements will not be executed')
    main(dry_run=dry)
