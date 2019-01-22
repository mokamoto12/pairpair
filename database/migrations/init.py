import sqlite3

db_name = 'database/pairpair.sqlite3'


def create_pairs_table(cursor) -> None:
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS pairs(data TEXT, created_at DATETIME)")


if __name__ == '__main__':
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    try:
        create_pairs_table(cursor)

        connect.commit()
    except Exception as e:
        connect.rollback()
        print(e)
    finally:
        connect.close()
