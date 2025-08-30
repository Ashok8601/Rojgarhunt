import sqlite3 
db_name='app.db'
def get_connection():
    conn=sqlite3.connect(db_name)
    return conn
    
def init_db():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        department TEXT,
        company TEXT NOT NULL,
        location TEXT NOT NULL,
        work_mode TEXT NOT NULL,
        job_type TEXT NOT NULL,
        experience TEXT NOT NULL,
        salary_min INTEGER,
        salary_max INTEGER,
        currency TEXT DEFAULT 'INR',
        description TEXT NOT NULL,
        responsibilities TEXT,
        requirements TEXT,
        skills TEXT,
        apply_url TEXT,
        apply_email TEXT,
        deadline DATE,
        logo TEXT,
        visa_supported BOOLEAN DEFAULT 0,
        urgent BOOLEAN DEFAULT 0,
        disability_friendly BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
    )
""")
    conn.commit()
    conn.close()
def alter():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("ALTER TABLE jobs ADD COLUMN posted_at TEXT NOT NULL DEFAULT ' ' ")
    conn.commit()
    conn.close()
def delete():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM user")   # कोई WHERE condition नहीं है
    conn.commit()
    conn.close()
    print("All users deleted successfully!")
init_db() 
#alter()
#delete()