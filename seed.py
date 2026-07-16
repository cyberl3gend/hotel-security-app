import sqlite3

def seed_db():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # Add test bookings for different users
    bookings = [
        (1, 'Deluxe Suite — Room 412', '2026-06-14', '2026-06-17', 499.00),
        (1, 'Standard Room — Room 201', '2026-07-01', '2026-07-03', 199.00),
        (2, 'Penthouse Suite — Room 801', '2026-06-20', '2026-06-25', 1299.00),
        (2, 'Standard Room — Room 105', '2026-08-10', '2026-08-12', 179.00),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO bookings 
        (user_id, room, check_in, check_out, total)
        VALUES (?, ?, ?, ?, ?)
    ''', bookings)

    conn.commit()
    conn.close()
    print("Database seeded successfully")

if __name__ == '__main__':
    seed_db()