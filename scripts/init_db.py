#!/usr/bin/env python3
"""Initialize database with Alembic migrations safely."""
import sys
import os
import subprocess
from sqlalchemy import create_engine, inspect, text


def check_tables_exist(engine):
    """Check if application tables already exist."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    # Check for key application tables
    app_tables = ['organizations', 'users', 'campaigns', 'documents', 'meetings']
    return any(table in tables for table in app_tables)


def get_alembic_current_version(engine):
    """Get current alembic version from database, or None if not set."""
    inspector = inspect(engine)
    if 'alembic_version' not in inspector.get_table_names():
        return None

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            row = result.fetchone()
            return row[0] if row else None
    except Exception:
        return None


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
        current_version = get_alembic_current_version(engine)

        print(f"  Tables exist: {tables_exist}")
        print(f"  Alembic current version: {current_version if current_version else 'None'}")

        if tables_exist and not current_version:
            # Tables exist but Alembic doesn't know about them
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
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
