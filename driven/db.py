from flask import g
import sqlite3

def sqlite_connect():
    conn = sqlite3.connect(
        "test.db",
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    return sqlite_connect()

def execute(conn, stmt, *args, **kwargs):
    return sqlite_execute(conn, stmt, *args, **kwargs)

def sqlite_execute(conn, stmt, *args, **kwargs):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute(stmt, *args, **kwargs)
    return [dict(r) for r in cursor.fetchall()]
