import psycopg2, logging
from contextlib import contextmanager

@contextmanager
def create_connect():
    try:
        conn = psycopg2.connect(host="localhost", port="5432", dbname="hw03", user="postgres", password="pass")
        try:
            yield conn
        finally:
            conn.close()
    except psycopg2.OperationalError:
        print("DB connection Failed")


def create_tab(conn, sql_stmt):
    c = conn.cursor()
    try:
        c.execute(sql_stmt)
        conn.commit()
    except psycopg2.DatabaseError as err:
        logging.error(f"Database Error: {err}")
        conn.rollback()
    finally:
        c.close()
        conn.close()


def main():
    sql_stmt = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE
    );
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER,
        user_id INTEGER,  
        FOREIGN KEY (user_id) REFERENCES users (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (status_id) REFERENCES status (id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
    )
    """

    try:
        with create_connect() as conn:
            create_tab(conn, sql_stmt)
    except RuntimeError as err:
        logging.error(f"Runtime Error: {err}")



if __name__ == "__main__":
    main()