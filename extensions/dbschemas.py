from extensions.extensions import get_db_connection

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS authentication (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        status ENUM('active', 'inactive', 'banned') DEFAULT 'active',
        last_login TIMESTAMP NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS balance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
        currency ENUM('ngn', 'cfa') DEFAULT 'ngn',
        tx_id VARCHAR(255) NOT NULL
    )
""")


    conn.commit()
    cur.close()
    conn.close()
