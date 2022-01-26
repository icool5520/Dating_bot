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
				db_cmd.upd_state_user(uid, "main_menu")
			else:
				bot.send_message(chat_id=cid, text="Вы зарегистрированы, однако для полноценного доступа к функциям " +
												   "бота необходимо одобрение Администратора")
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
			if profile_data[4] != '-':
				bot.send_photo(chat_id=cid, photo=f"{profile_data[4]}", caption=f"Мой профиль\n{'-'*25}\nИмя:" +
				f" {profile_data[0]}\nВозраст: {profile_data[1]}\nГород: {profile_data[2]}\nО себе: {profile_data[3]}")
			else:
				bot.send_message(chat_id=cid, text=f"Мой профиль\n--------------\nИмя: {profile_data[0]}\n" +
				f" Возраст: {profile_data[1]}\nГород: {profile_data[2]}\nО себе: {profile_data[3]}")
			bot.send_message(chat_id=cid, text="Выберите действие", reply_markup=markup.gen_markup_profile())
	except Exception as ex:
		print('edit_profile:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "user_info")
def callback_edit_profile(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid:
			db_cmd.upd_state_user(uid, "view_profile")
			profile_data = db_cmd.get_user_profile(uid)
			print(profile_data)
			if profile_data[4] != '-':
				bot.send_photo(chat_id=cid, photo=f"{profile_data[4]}", caption=f"Мой профиль\n{'-' * 25}\nИмя:" +
				f" {profile_data[0]}\nВозраст: {profile_data[1]}\nГород: {profile_data[2]}\nО себе: {profile_data[3]}")
			else:
				bot.send_message(chat_id=cid, text=f"Мой профиль\n--------------\nИмя: {profile_data[0]}\n" +
								   f" Возраст: {profile_data[1]}\nГород: {profile_data[2]}\nО себе: {profile_data[3]}")
			bot.send_message(chat_id=cid, text="Выберите действие", reply_markup=markup.gen_markup_profile())
	except Exception as ex:
		print('callback_edit_profile:', ex)


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
def edit_profile(message):
	cid = message.chat.id
	uid = message.from_user.id
	global profile_data
	try:
		if cid == uid and db_cmd.get_state_user(uid)[0] == "edit_profile_name":
			profile_data = [message.text.replace('*', '')]
			db_cmd.upd_state_user(uid, "edit_profile_age")
			bot.send_message(chat_id=cid, text="Введите Ваш возраст:")
		elif cid == uid and db_cmd.get_state_user(uid)[0] == "edit_profile_age":
			profile_data.append(message.text.replace('*', ''))
			db_cmd.upd_state_user(uid, "edit_profile_city")
			bot.send_message(chat_id=cid, text="Введите город:")
		elif cid == uid and db_cmd.get_state_user(uid)[0] == "edit_profile_city":
			profile_data.append(message.text.replace('*', ''))
			db_cmd.upd_state_user(uid, "edit_profile_about")
			bot.send_message(chat_id=cid, text="Введите данные о себе:")
		elif cid == uid and db_cmd.get_state_user(uid)[0] == "edit_profile_about":
			profile_data.append(message.text.replace('*', ''))
			bot.send_message(chat_id=cid, text="Для добавления фотографии профиля отправьте боту фото",
							 reply_markup=markup.gen_markup_confirm_profile())

			# data = f'{profile_data[1]}*{profile_data[2]}*{profile_data[3]}'
			# db_cmd.upd_user_profile(uid, profile_data[0], data)
			db_cmd.upd_state_user(uid, "edit_profile_photo")
	except Exception as ex:
		print('edit_profile:', ex)

#****************************************************************************
@bot.message_handler(content_types=["photo"])
def add_photo(message):
	cid = message.chat.id
	uid = message.from_user.id
	try:
		if cid == uid:
			file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
			data = f'{profile_data[1]}*{profile_data[2]}*{profile_data[3]}*{file_info.file_id}'
			db_cmd.upd_user_profile(uid, profile_data[0], data)
			bot.send_message(chat_id=cid, text="Главное меню", reply_markup=markup.gen_markup_user())
			db_cmd.upd_state_user(uid, "main_menu")

	except Exception as ex:
		print('add_photo:', ex)


@bot.callback_query_handler(func=lambda call: call.data.endswith("confirm_profile_without_photo"))
def back_to_menu(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid:
			data = f'{profile_data[1]}*{profile_data[2]}*{profile_data[3]}*-'
			db_cmd.upd_user_profile(uid, profile_data[0], data)


	except Exception as ex:
		print('back_to_menu:', ex)


@bot.callback_query_handler(func=lambda call: call.data.endswith("Back_to_menu"))
def back_to_menu(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid and call.data.startswith("admin"):
			db_cmd.upd_state_admin(uid, "menu_admin")
			bot.send_message(chat_id=cid, text="Меню администратора", reply_markup=markup.gen_markup_admin())
		elif cid == uid and call.data.startswith("user"):
			bot.send_message(chat_id=cid, text="Главное меню", reply_markup=markup.gen_markup_user())
	except Exception as ex:
		print('back_to_menu:', ex)


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
	except Exception as e:
		print('callback_activate_user:', e)

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
