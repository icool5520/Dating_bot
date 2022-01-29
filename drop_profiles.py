import sqlite3


def drop_table_profiles():
	db_file = "db.db"
	conn = None
	try:
		sql = f"""DROP TABLE IF EXISTS profiles;"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('drop_table_profiles:', ex)
	finally:
		if conn is not None:
			conn.close()


def create_tables():
	db_file = "db.db"
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()
	with conn:
		cur.execute(f"""CREATE TABLE IF NOT EXISTS profiles(
						profile_id INTEGER PRIMARY KEY NOT NULL,
						city TEXT NOT NULL,
						name TEXT NOT NULL,
						age TEXT NOT NULL,
						about TEXT,
						photo TEXT)""")

drop_table_profiles()
create_tables()
