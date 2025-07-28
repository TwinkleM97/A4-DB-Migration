import os
import mysql.connector
import unittest

# Use ACT port if running locally
if os.getenv('ACT'):
    DB_CONFIG = {
        "host": "127.0.0.1",
        "port": 3307,
        "user": "subuser",
        "password": "subpass",
        "database": "subscriptions"
    }
else:
    DB_CONFIG = {
        "host": "mysql",
        "port": 3307,
        "user": "subuser",
        "password": "subpass",
        "database": "subscriptions"
    }

class TestSubscribersDB(unittest.TestCase):
    def setUp(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def test_insert_subscriber(self):
        self.cursor.execute("INSERT INTO subscribers (email, status) VALUES ('test@example.com', 'active')")
        self.conn.commit()
        self.cursor.execute("SELECT COUNT(*) FROM subscribers WHERE email='test@example.com'")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_update_status(self):
        self.cursor.execute("UPDATE subscribers SET status='inactive' WHERE email='test@example.com'")
        self.conn.commit()
        self.cursor.execute("SELECT status FROM subscribers WHERE email='test@example.com'")
        status = self.cursor.fetchone()[0]
        self.assertEqual(status, 'inactive')

    def test_delete_subscriber(self):
        self.cursor.execute("DELETE FROM subscribers WHERE email='test@example.com'")
        self.conn.commit()
        self.cursor.execute("SELECT COUNT(*) FROM subscribers WHERE email='test@example.com'")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 0)

if __name__ == '__main__':
    unittest.main()
