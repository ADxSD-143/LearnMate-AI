from sqlalchemy import text
from app.database.session import SessionLocal

def run_academic_migration():
    db = SessionLocal()
    try:
        # Check if user_id column exists on subjects
        check_user_id = db.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'subjects' AND column_name = 'user_id'
        """)).fetchone()

        if not check_user_id:
            print("Adding user_id to subjects and migrating constraints...")
            db.execute(text("""
                ALTER TABLE subjects ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE;
            """))
            db.execute(text("""
                UPDATE subjects SET user_id = 1 WHERE user_id IS NULL;
            """))
            db.execute(text("""
                ALTER TABLE subjects ALTER COLUMN user_id SET NOT NULL;
            """))
            db.execute(text("""
                ALTER TABLE subjects DROP CONSTRAINT IF EXISTS subjects_name_key;
            """))
            db.execute(text("""
                ALTER TABLE subjects ADD CONSTRAINT uq_user_subject_name UNIQUE (user_id, name);
            """))
            db.execute(text("""
                ALTER TABLE subjects ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            """))
            print("Subjects migration complete.")
        else:
            print("Subjects table already has user_id.")

        # Topics migration
        print("Migrating topics...")
        db.execute(text("""
            ALTER TABLE topics ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
        """))
        db.execute(text("""
            ALTER TABLE topics DROP CONSTRAINT IF EXISTS uq_subject_topic_name;
        """))
        db.execute(text("""
            ALTER TABLE topics ADD CONSTRAINT uq_subject_topic_name UNIQUE (subject_id, name);
        """))
        print("Topics migration complete.")

        # Tasks migration
        print("Migrating tasks...")
        db.execute(text("""
            ALTER TABLE tasks ADD COLUMN IF NOT EXISTS description TEXT;
        """))
        db.execute(text("""
            ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR DEFAULT 'Medium';
        """))
        db.execute(text("""
            ALTER TABLE tasks ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'Pending';
        """))
        db.execute(text("""
            ALTER TABLE tasks ADD COLUMN IF NOT EXISTS deadline TIMESTAMP WITH TIME ZONE;
        """))
        db.execute(text("""
            ALTER TABLE tasks ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
        """))
        print("Tasks migration complete.")

        db.commit()
        print("Academic migration completed successfully!")
    except Exception as e:
        db.rollback()
        print("Migration error:", e)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run_academic_migration()
