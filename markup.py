from telebot import types

def gen_markup_admin():
	try:
		markup = types.InlineKeyboardMarkup()

		btn1 = types.InlineKeyboardButton(text="\U00002b50 Активировать участников", callback_data='activate_user')
		btn2 = types.InlineKeyboardButton(text="\U0000274c Удалить участников", callback_data='delete_user')
		btn3 = types.InlineKeyboardButton(text="Добавить анкету", callback_data='add_dating_profile')
		btn4 = types.InlineKeyboardButton(text="Удалить анкету", callback_data='delete_dating_profile')
		
		markup.add(btn1)
		markup.add(btn2)
		markup.add(btn3)
		markup.add(btn4)
	except Exception as ex:
		print('gen_murkup_admin:', ex)
	finally:
		return markup


def gen_markup_user():
	try:
		markup = types.InlineKeyboardMarkup()

		btn1 = types.InlineKeyboardButton(text="Мой профиль", callback_data='user_info')
		btn2 = types.InlineKeyboardButton(text="Поиск анкеты", callback_data='search_dating_profile')
		markup.add(btn1)
		markup.add(btn2)
	except Exception as ex:
		print('gen_murkup_user:', ex)
	finally:
		return markup


def gen_markup_users_inactive(_list_users_inactive):
	try:
		markup = types.InlineKeyboardMarkup()
		if len(_list_users_inactive) > 0:
			for i in range(len(_list_users_inactive)):
				button_text = f'{i + 1}. id: {_list_users_inactive[i][0]}, Имя: {_list_users_inactive[i][1]}'
				callback_data_text = f'activate_user:{_list_users_inactive[i][0]}'
				btn = types.InlineKeyboardButton(text=button_text, callback_data=callback_data_text)
				markup.add(btn)
			btn = types.InlineKeyboardButton(text='Активировать всех', callback_data='activate_user:All')
			markup.add(btn)
			btn = types.InlineKeyboardButton(text='<< Назад', callback_data='activate_user:Back_to_admin_menu')
			markup.add(btn)
		else:
			btn = types.InlineKeyboardButton(text='<< Назад', callback_data='activate_user:Back_to_admin_menu')
			markup.add(btn)
	except Exception as ex:
		print('gen_murkup_users_inactive:', ex)
	finally:
		return markup


def gen_markup_users(_list_users):
	try:
		markup = types.InlineKeyboardMarkup()
		for i in range(len(_list_users)):
			button_text = f'{i + 1}. Удалить - id: {_list_users[i][0]}, Имя: {_list_users[i][1]}'
			callback_data_text = f'delete_user:{_list_users[i][0]}'
			btn = types.InlineKeyboardButton(text=button_text, callback_data=callback_data_text)
			markup.add(btn)
		btn = types.InlineKeyboardButton(text='<< Назад', callback_data='delete_user:Back_to_admin_menu')
		markup.add(btn)
	except Exception as ex:
		print('gen_murkup_users:', ex)
	finally:
		return markup