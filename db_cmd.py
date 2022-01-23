import sqlite3


def create_tables():
	db_file = "db.db"
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()
	with conn:
		cur.execute(f"""CREATE TABLE IF NOT EXISTS users(
						user_id INTEGER PRIMARY KEY NOT NULL,
						name TEXT NOT NULL,
						state TEXT NOT NULL,
						data TEXT)""")
		cur.execute(f"""CREATE TABLE IF NOT EXISTS admins(
						user_id INTEGER PRIMARY KEY NOT NULL,
						state TEXT NOT NULL,
						data TEXT)""")


def check_user_id(_user_id, _name):
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT * FROM users WHERE user_id = {_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if not data:
			cur.close()
			add_user(_user_id, _name)
			check = True
		else:
			cur.close()
	except Exception as ex:
		print('check_user_id:', ex)
	finally:
		if conn is not None:
			conn.close()
	return check


def add_user(_user_id, _name):
	db_file = "db.db"
	conn = None
	
	try:
		sql = f"""INSERT INTO users(user_id, name, state, data) VALUES(?, ?, ?, ?);"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql, (_user_id, _name, 'inactive', ''))
		conn.commit()
		cur.close()
	except Exception as ex:
		print('add_user:', ex)
	finally:
		if conn is not None:
			conn.close()


def check_admin(_user_id):
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT * FROM admins WHERE user_id = {_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if data is not None:
			check = True
		else:
			cur.close()
	except Exception as ex:
		print('check_admin:', ex)
	finally:
		if conn is not None:
			conn.close()
	return check


def check_user_state(_user_id):
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT state FROM users WHERE user_id = {_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if data[0] != 'inactive':
			check = True
		else:
			cur.close()
	except Exception as ex:
		print('check_user_state:', ex)
	finally:
		if conn is not None:
			conn.close()
	return check


def get_users_inactive():
	# Достаем список неактивных юзеров для админа
	db_file = "db.db"
	conn = None
	data = None
	try:
		sql = f"""SELECT user_id, name FROM users WHERE state='inactive'"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
	except Exception as ex:
		print('get_users_inactive:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def get_users_all():
	db_file = "db.db"
	conn = None
	data = None
	try:
		sql = f"""SELECT user_id, name FROM users"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
	except Exception as ex:
		print('get_users_all:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def upd_state_admin(_user_id, _state):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE admins SET state='{_state}' WHERE user_id={_user_id};"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_state_admin:', ex)
	finally:
		if conn is not None:
			conn.close()


def get_state_admin(_user_id):
	db_file = "db.db"
	conn = None
	data = None
	try:
		sql = f"""SELECT state FROM admins WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_state_admin:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def upd_state_users(_user_id, _state):
	db_file = "db.db"
	conn = None
	if len(_user_id) == 1:
		_user_id = _user_id[0]
		sql = f"""UPDATE users SET state='{_state}' WHERE user_id={_user_id}"""
	else:
		sql = f"""UPDATE users SET state='{_state}' WHERE user_id IN {_user_id}"""
	try:
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print("upd_state_users:", ex)
	finally:
		if conn is not None:
			conn.close()


def delete_user(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""DELETE FROM users WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print("delete_user:", ex)
	finally:
		if conn is not None:
			conn.close()


'''
def check_user_id(user_id):
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT * FROM users WHERE user_id = {user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if not data:
			cur.close()
			add_user(user_id)
			check = True
		else:
			cur.close()
	except Exception as ex:
		print('check_user_id:', ex)
	finally:
		if conn is not None:
			conn.close()
		return check

def add_user(user_id):
	db_file = "db.db"
	conn = None
	
	try:
		sql = f"""INSERT INTO users(user_id, state, data) VALUES(?, ?, ?);"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql, (user_id, 'start', ''))
		conn.commit()
		cur.close()
	except Exception as ex:
		print('add_user:', ex)
	finally:
		if conn is not None:
			conn.close()
		return check

def get_state_user(user_id):
	db_file = "db.db"
	conn = None
	data = None
	try:
		sql = f"""SELECT state FROM users WHERE user_id={user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_state_user:', ex)
	finally:
		if conn is not None:
			conn.close()
		print(data)
		return data


def up_state_user(user_id, state):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE users SET state='{state}' WHERE user_id={user_id};"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_state_user:', ex)
	finally:
		if conn is not None:
			conn.close()
'''

create_tables()
