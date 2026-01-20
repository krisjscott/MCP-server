import sqlite3
from datetime import datetime
from typing import Optional, List, Dict

DB_PATH = "mcp_bank.db"

def _conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    c = _conn()
    cur = c.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        ts TEXT NOT NULL,
        FOREIGN KEY(account_id) REFERENCES accounts(id)
    )
    """)
    c.commit()
    c.close()

def create_account(owner: str, initial_deposit: float = 0.0) -> Dict:
    c = _conn()
    cur = c.cursor()
    cur.execute("INSERT INTO accounts (owner, balance) VALUES (?, ?)", (owner, float(initial_deposit)))
    account_id = cur.lastrowid
    if initial_deposit:
        cur.execute("INSERT INTO transactions (account_id, type, amount, ts) VALUES (?, ?, ?, ?)",
                    (account_id, "deposit", float(initial_deposit), datetime.utcnow().isoformat()))
    c.commit()
    cur.execute("SELECT id, owner, balance FROM accounts WHERE id = ?", (account_id,))
    row = cur.fetchone()
    c.close()
    return {"id": row[0], "owner": row[1], "balance": row[2]}

def get_account(account_id: int) -> Optional[Dict]:
    c = _conn()
    cur = c.cursor()
    cur.execute("SELECT id, owner, balance FROM accounts WHERE id = ?", (account_id,))
    row = cur.fetchone()
    c.close()
    if not row:
        return None
    return {"id": row[0], "owner": row[1], "balance": row[2]}

def update_balance(account_id: int, delta: float):
    c = _conn()
    cur = c.cursor()
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (float(delta), account_id))
    c.commit()
    c.close()

def add_transaction(account_id: int, ttype: str, amount: float):
    c = _conn()
    cur = c.cursor()
    cur.execute("INSERT INTO transactions (account_id, type, amount, ts) VALUES (?, ?, ?, ?)",
                (account_id, ttype, float(amount), datetime.utcnow().isoformat()))
    c.commit()
    c.close()

def get_transactions(account_id: int, limit: int = 20) -> List[Dict]:
    c = _conn()
    cur = c.cursor()
    cur.execute("SELECT id, type, amount, ts FROM transactions WHERE account_id = ? ORDER BY id DESC LIMIT ?", (account_id, limit))
    rows = cur.fetchall()
    c.close()
    return [{"id": r[0], "type": r[1], "amount": r[2], "ts": r[3]} for r in rows]