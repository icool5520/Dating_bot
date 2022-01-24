import telebot
import markup
import db_cmd


token = '2005668889:AAFGnIiyzHUfwwzK8JqYOQ95TeDORFfcSbo'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_msg(message):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		first_name = message.from_user.first_name
		last_name = message.from_user.last_name
		if last_name == None:
			last_name = ''
		name = f'{first_name} {last_name}'
		if cid == uid:
			db_cmd.check_user_id(uid, name.strip())
			if db_cmd.check_user_state(uid):
				bot.send_message(chat_id=cid, text="Главное меню", reply_markup=markup.gen_markup_user())
			else:
				bot.send_message(chat_id=cid, text="Вы зарегистрированы, однако для полноценного доступа к функциям " +
												   "бота необходимо одобрение Администратора")
				bot.send_message(chat_id=cid, text="А тем временем по команде /EditProfile Вы можете заполнить" +
												   " информацию в своем профиле")
	except Exception as ex:
		print('start_msg:', ex)

@bot.message_handler(commands=['admin'])
def admin_start(message):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		if cid == uid and db_cmd.check_admin(uid):
			db_cmd.upd_state_admin(uid, "menu_admin")
			bot.send_message(chat_id=cid, text="Меню администратора", reply_markup=markup.gen_markup_admin())
	except Exception as ex:
		print('admin_start:', ex)


@bot.message_handler(commands=['edit_profile'])
def edit_profile(message):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		if cid == uid:
			db_cmd.upd_state_user(uid, "view_profile")
			profile_data = db_cmd.get_user_profile(uid)
			bot.send_message(chat_id=cid, text=f"Мой профиль\n\nИмя: {profile_data[0]}\nВозраст: {profile_data[1]}" +
							 f"\nГород: {profile_data[2]}\nО себе: {profile_data[3]}",
							 reply_markup=markup.gen_markup_profile())
	except Exception as ex:
		print('edit_profile:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "edit_profile")
def callback_edit_profile(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid:
			db_cmd.upd_state_user(uid, "edit_profile_name")
			bot.send_message(chat_id=cid, text="Введите Имя (оставьте поле пустым чтобы оставить текущее имя):")
	except Exception as ex:
		print('callback_edit_profile:', ex)


@bot.message_handler(content_types=["text"])
def edit_profile_name(message):
	cid = message.chat.id
	uid = message.from_user.id
	print(db_cmd.get_state_user(uid)[0] == "edit_profile_name", 'edit_profile_name')
	try:
		if cid == uid and db_cmd.get_state_user(uid)[0] == "edit_profile_name":
			if message.text != '':
				global profile_data
				profile_data = [message.text.replace('*', '')]
			else:
				profile_data = [db_cmd.get_name_user(uid)]
			db_cmd.upd_state_user(uid, "edit_profile_age")
			bot.send_message(chat_id=cid, text="Введите Ваш возраст:")
	except Exception as ex:
		print('edit_profile_name:', ex)



def edit_profile_age(message):
	cid = message.chat.id
	uid = message.from_user.id
	print(db_cmd.get_state_user(uid)[0])
	try:
		if cid == uid and db_cmd.get_state_user(uid)[0] == "edit_profile_age":
			profile_data.append(message.text.replace('*', ''))
			db_cmd.upd_state_user(uid, "edit_profile_city")
			bot.send_message(chat_id=cid, text="Введите город:")
	except Exception as ex:
		print('callback_edit_age:', ex)



def edit_profile_age(message):
	cid = message.chat.id
	uid = message.from_user.id
	print(db_cmd.get_state_user(uid)[0])
	try:
		if cid == uid and db_cmd.get_state_user(uid)[0] == "edit_profile_city":
			profile_data.append(message.text.replace('*', ''))
			db_cmd.upd_state_user(uid, "edit_profile_about")
			bot.send_message(chat_id=cid, text="Введите данные о себе:")
	except Exception as ex:
		print('callback_edit_age:', ex)



def edit_profile_age(message):
	cid = message.chat.id
	uid = message.from_user.id
	print(db_cmd.get_state_user(uid)[0])
	try:
		if cid == uid and db_cmd.get_state_user(uid)[0] == "edit_profile_about":
			profile_data.append(message.text.replace('*', ''))
			db_cmd.upd_state_user(uid, "start")

			bot.send_message(chat_id=cid, text="Done!")
	except Exception as ex:
		print('callback_edit_age:', ex)


# @bot.callback_query_handler(func=lambda call: call.data.endswith("Back_to_user_menu"))
# def edit_profile(call):
# 	try:
# 		cid = call.message.chat.id
# 		uid = call.from_user.id
# 		if cid == uid:
# 			bot.send_message(chat_id=cid, text="Меню администратора", reply_markup=markup.gen_markup_admin())
# 			#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 	except Exception as ex:
# 		print('admin_start_back:', ex)


@bot.callback_query_handler(func=lambda call: call.data.endswith("Back_to_admin_menu"))
def admin_start_back(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid and db_cmd.check_admin(uid):
			db_cmd.upd_state_admin(uid, "menu_admin")
			bot.send_message(chat_id=cid, text="Меню администратора", reply_markup=markup.gen_markup_admin())
	except Exception as ex:
		print('admin_start_back:', ex)




@bot.callback_query_handler(func=lambda call: call.data == "activate_user")
def callback_activate_user(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		if cid == uid:
			db_cmd.upd_state_admin(uid, "activate_user")
			global list_users_inactive
			list_users_inactive = db_cmd.get_users_inactive()
			if len(list_users_inactive) > 0:
				bot.send_message(chat_id=cid, text="Список неактивных пользователей:",
								 reply_markup=markup.gen_markup_users_inactive(list_users_inactive))
			else:
				bot.send_message(chat_id=cid, text="Неактивные пользователи отсутствуют",
								 reply_markup=markup.gen_markup_users_inactive(list_users_inactive))
	except Exception as ex:
		print('callback_activate_user:', ex)


@bot.callback_query_handler(func=lambda call: call.data.startswith("activate_user:"))
def activate_users(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		user_to_activate_id = call.data.split(':')[1]
		if cid == uid and db_cmd.get_state_admin(uid)[0] == 'activate_user':
			if user_to_activate_id.lower() == 'all':
				bot.answer_callback_query(call.id, f'Все пользователи активированы')
				db_cmd.upd_state_inactive_users(tuple([i[0] for i in list_users_inactive]), "start")
			elif user_to_activate_id.lower() == 'back':
				pass
			else:
				bot.answer_callback_query(call.id, f'Пользователь с id: {user_to_activate_id} активирован')
				db_cmd.upd_state_inactive_users((int(user_to_activate_id),), "start")
	except Exception as ex:
		print('activate_users:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "delete_user")
def callback_delete_user(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid:
			db_cmd.upd_state_admin(uid, "delete_user")
			global list_users
			list_users = db_cmd.get_users_all()
			bot.send_message(chat_id=cid, text="Список пользователей:",
								 reply_markup=markup.gen_markup_users(list_users))
	except Exception as ex:
		print('callback_delete_user:', ex)


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_user:"))
def delete_user(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		user_to_delete_id = call.data.split(':')[1]
		if cid == uid and db_cmd.get_state_admin(uid)[0] == 'delete_user':
			bot.answer_callback_query(call.id, f'Пользователь с id: {user_to_delete_id} удалён')
			db_cmd.delete_user(int(user_to_delete_id))
	except Exception as ex:
		print('delete_user:', ex)


if __name__ == '__main__':
	bot.polling()
