import sqlite3

conn = sqlite3.connect('hotel.db')
conn.execute(
    "INSERT INTO bookings (user_id, room, check_in, check_out, total) VALUES (?, ?, ?, ?, ?)",
    (4, "Ocean View Suite Room 305", "2026-09-01", "2026-09-05", 650.00)
)
conn.commit()

rows = conn.execute("SELECT * FROM bookings WHERE user_id = 4").fetchall()
for row in rows:
    print(row)

conn.close()