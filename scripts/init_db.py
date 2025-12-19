#!/usr/bin/env python3
"""Initialize database with Alembic migrations safely."""
import sys
import os
import subprocess
from sqlalchemy import create_engine, inspect


def check_tables_exist(engine):
    """Check if application tables already exist."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    # Check for key application tables
    app_tables = ['organizations', 'users', 'campaigns', 'documents', 'meetings']
    return any(table in tables for table in app_tables)


def check_alembic_version_exists(engine):
    """Check if alembic_version table exists."""
    inspector = inspect(engine)
    return 'alembic_version' in inspector.get_table_names()


def main():
    """Main initialization logic."""
    print("🔍 Checking database state...")

    try:
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL environment variable not set")
            sys.exit(1)

        engine = create_engine(database_url)

        tables_exist = check_tables_exist(engine)
        alembic_version_exists = check_alembic_version_exists(engine)

        print(f"  Tables exist: {tables_exist}")
        print(f"  Alembic version table exists: {alembic_version_exists}")

        if tables_exist and not alembic_version_exists:
            # Tables were created without Alembic, stamp the current version
            print("✅ Tables exist but not tracked by Alembic")
            print("🏷️  Stamping database with current migration version...")
            result = subprocess.run(
                ['alembic', 'stamp', '001'],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"❌ Failed to stamp database: {result.stderr}")
                sys.exit(1)
            print("✅ Database stamped successfully")

        # Now run migrations (will be a no-op if already at head)
        print("🔄 Running Alembic migrations...")
        result = subprocess.run(
            ['alembic', 'upgrade', 'head'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ Migration failed: {result.stderr}")
            sys.exit(1)

        print("✅ Database migrations complete")
        sys.exit(0)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
