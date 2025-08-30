import sqlite3, random

DB = "app.db"

NAMES = [
    "Ravi","Suresh","Amit","Pooja","Neha","Sunita","Ramesh","Vikas","Anita","Rajesh",
    "Deepak","Kiran","Mohit","Anil","Geeta","Raju","Meena","Ajay","Rekha","Sanjay",
    "Manoj","Seema","Prakash","Vivek","Rita","Santosh","Lata","Nitesh","Radha","Arun"
]

def ensure_users_table(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        password TEXT
    )
    """)

def seed_users(n=100):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    ensure_users_table(conn)

    rows = []
    for i in range(n):
        name = random.choice(NAMES) + str(i)
        email = f"user{i}@example.com"
        phone = f"9{random.randint(100000000,999999999)}"
        password = "123456"  # dummy password
        rows.append((name, email, phone, password))

    cur.executemany("""
        INSERT OR IGNORE INTO users (name, email, phone, password)
        VALUES (?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()
    print(f"Inserted {n} users into {DB}")

if __name__ == "__main__":
    seed_users(100)