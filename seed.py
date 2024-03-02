from faker import Faker
import psycopg2, logging, random

fake = Faker()

conn = psycopg2.connect(host="localhost", port="5432", dbname="hw03", user="postgres", password="pass")
c = conn.cursor()

# Заповнюємо статуси
status_ids = []
for s in ["new", "in progress", "completed"]:
    c.execute("INSERT INTO status (name) VALUES (%s) RETURNING id", (s,))
    status_ids.append(c.fetchone()[0])

# Заповнюємо користувачів з тасками
for _ in range(1000): # Кількість користувачів
    c.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id", (fake.unique.name(),fake.unique.email()))
    user_id = c.fetchone()[0]
    for _ in range(random.randint(0,4)): # Кількість тасків
        c.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                   (fake.word(), fake.word(), random.choice(status_ids), user_id))


try:
    conn.commit()
except psycopg2.DatabaseError as err:
    logging.error(f"Database Error: {err}")
    conn.rollback()
finally:
    c.close()
    conn.close()