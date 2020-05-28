import discord, json, random, time, os
from discord.ext import commands
from discord.ext.commands import Bot

prefixUser = "="
Bot = commands.Bot( command_prefix = prefixUser )

# time.strftime("%B:%d:%Y", time.localtime())
# Команды

@Bot.command(pass_context = True)
async def удалить(ctx, amount = 1):
	await ctx.channel.purge(limit = 1)
	author_id = "{0.author.id}".format(ctx)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if (author_id in config_data["admins"]) or (author_id in config_data["moderations"]):
		wag_clear = 0
		while True:
			await ctx.channel.purge(limit = 1)
			wag_clear += 1
			if wag_clear == amount:
				break
			time.sleep(0.5)
		emd = discord.Embed(title = "Чистка", description = "Удаление сообщений", color = discord.Color.blue())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Очищено", inline = True)
		emd.add_field(name = "Удалено", value = "{0} сообщений".format(amount), inline = True)
		await ctx.send(embed = emd)
	elif not((author_id in config_data["admins"]) or (author_id in config_data["moderations"])):
		emd = discord.Embed(title = "Чистка", description = "Удаление сообщений", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def плюс_админ(ctx, member: discord.Member,*, reason = None ):
	author_id = "{0.author.id}".format(ctx)
	user_id = "{0.id}".format(member)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if author_id == config_data["ID-YOU"]:
		if not(user_id in config_data["admins"]):
			config_data["admins"].append("{0}".format(user_id))
			with open('config.json', 'w') as configFile:
				json.dump(config_data, configFile)
			emd = discord.Embed(title = "Добавление админов", description = "Добавление админов в базу бота", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Добавен", inline = True)
			await ctx.send(embed = emd)
			emd = discord.Embed(title = "Вы админ", description = "Вы были добавлены в список админов бота", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Добавлен", inline = True)
			await member.send(embed = emd)
		elif user_id in config_data["admins"]:
			emd = discord.Embed(title = "Добавление админов", description = "Добавление админов в базу бота", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Уже есть в базе", inline = True)
			await ctx.send(embed = emd)
	elif not(author_id == config_data["ID-YOU"]):
		emd = discord.Embed(title = "Добавление админов", description = "Добавление админов в базу бота", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def минус_админ(ctx, member: discord.Member,*, reason = None ):
	author_id = "{0.author.id}".format(ctx)
	user_id = "{0.id}".format(member)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if author_id == config_data["ID-YOU"]:
		if not(user_id in config_data["admins"]):
			emd = discord.Embed(title = "Удаление админов", description = "Удаление админов из базу бота", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Нету в базе бота", inline = True)
			await ctx.send(embed = emd)
		elif user_id in config_data["admins"]:
			wag = 0
			while True:
				if config_data["admins"][wag] == "{0}".format(user_id):
					break
				wag += 1
			del config_data["admins"][wag]
			with open('config.json', 'w') as configFile:
				json.dump(config_data, configFile)
			emd = discord.Embed(title = "Удаление админов", description = "Удаление админов из базу бота", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Удалён", inline = True)
			await ctx.send(embed = emd)
			emd = discord.Embed(title = "Вы не админ", description = "Вы были удалены из базы админов бота", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Удалён", inline = True)
			await member.send(embed = emd)
	elif not(author_id == config_data["ID-YOU"]):
		emd = discord.Embed(title = "Удаление админов", description = "Удаление админов из базу бота", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def копать(ctx):
	author_id = "{0.author.id}".format(ctx)
	with open('users_data.json') as usersFile:
		users = json.load(usersFile)
	if author_id in users["users_id"]:
		wag = 0
		while True:
			if author_id == users["users"][wag]["id"]:
				break
			wag += 1
		if not(1 in users["users"][wag]["inventory_id"]):
			emd = discord.Embed(title = "Копать", description = "Копни по глубже...", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Нету 'Shovel'", inline = True)
			emd.add_field(name = "Что делать?", value = "Купи 'Shovel'", inline = False)
			await ctx.send(embed = emd)
		elif 1 in users["users"][wag]["inventory_id"]:
			emd = discord.Embed(title = "Копать", description = "Копни по глубже...", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			wag_item = 0
			items_int = len(users["users"][wag]["inventory"])
			while wag_item != items_int:
				if users["users"][wag]["inventory"][wag_item]["id"] == 1:
					break
				wag_item += 1
			if not(users["users"][wag]["inventory"][wag_item]["strength"] == 0):
				with open('ores.json') as oresFile:
					ores = json.load(oresFile)
				ore_int = random.randint(1, 10)
				ore_quantity = random.randint(1, 20)
				if ore_int >= 10:
					money_plus = ores[0]["sell"] * ore_quantity
					users["users"][wag]["inventory"][wag_item]["strength"] -= 1
					users["users"][wag]["money"] += money_plus
					emd.add_field(name = "Руда", value = "Золото", inline = True)
					emd.add_field(name = "Выкопано", value = "{0} штук".format(ore_quantity), inline = True)
					emd.add_field(name = "Продано за", value = "{0} флорбо".format(money_plus), inline = True)
					emd.add_field(name = "Прочность лопаты", value = "{0} использований".format(users["users"][wag]["inventory"][wag_item]["strength"]), inline = True)
					await ctx.send(embed = emd)
				if ore_int >= 1 and ore_int <= 5:
					money_plus = ores[2]["sell"] * ore_quantity
					users["users"][wag]["inventory"][wag_item]["strength"] -= 1
					users["users"][wag]["money"] += money_plus
					emd.add_field(name = "Руда", value = "Камень", inline = True)
					emd.add_field(name = "Выкопано", value = "{0} штук".format(ore_quantity), inline = True)
					emd.add_field(name = "Продано за", value = "{0} флорбо".format(money_plus), inline = True)
					emd.add_field(name = "Прочность лопаты", value = "{0} использований".format(users["users"][wag]["inventory"][wag_item]["strength"]), inline = True)
					await ctx.send(embed = emd)
				elif ore_int >= 6 and ore_int <= 9:
					money_plus = ores[1]["sell"] * ore_quantity
					users["users"][wag]["inventory"][wag_item]["strength"] -= 1
					users["users"][wag]["money"] += money_plus
					emd.add_field(name = "Руда", value = "Железо", inline = True)
					emd.add_field(name = "Выкопано", value = "{0} штук".format(ore_quantity), inline = True)
					emd.add_field(name = "Продано за", value = "{0} флорбо".format(money_plus), inline = True)
					emd.add_field(name = "Прочность лопаты", value = "{0} использований".format(users["users"][wag]["inventory"][wag_item]["strength"]), inline = True)
					await ctx.send(embed = emd)
			elif users["users"][wag]["inventory"][wag_item]["strength"] == 0:
				emd = discord.Embed(title = "Копать", description = "Копни по глубже...", color = discord.Color.red())
				emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
				emd.add_field(name = "Статус", value = "Отменено", inline = True)
				emd.add_field(name = "Причина", value = "Лопата сломана", inline = True)
				await ctx.send(embed = emd)
			with open('users_data.json', 'w') as usersFile:
				json.dump(users, usersFile)
	elif not(author_id in users["users_id"]):
		emd = discord.Embed(title = "Копать", description = "Копни по глубже...", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Нету в базе бота", inline = True)
		emd.add_field(name = "Что делать?", value = "Напишите, админам или модераторам они вас добавят", inline = False)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def минус_модер(ctx, member: discord.Member,*, reason = None ):
	author_id = "{0.author.id}".format(ctx)
	user_id = "{0.id}".format(member)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if author_id in config_data["admins"]:
		if not(user_id in config_data["moderations"]):
			emd = discord.Embed(title = "Удаление модераторов", description = "Удаление модераторов из базу бота", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Нету в базе бота", inline = True)
			await ctx.send(embed = emd)
		elif user_id in config_data["moderations"]:
			wag = 0
			while True:
				if config_data["moderations"][wag] == "{0}".format(user_id):
					break
				wag += 1
			del config_data["moderations"][wag]
			with open('config.json', 'w') as configFile:
				json.dump(config_data, configFile)
			emd = discord.Embed(title = "Удаление модераторов", description = "Удаление модераторов из базу бота", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Удалён", inline = True)
			await ctx.send(embed = emd)
			emd = discord.Embed(title = "Вы не модератор", description = "Вы были удалены из базы модераторов бота", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Удалён", inline = True)
			await member.send(embed = emd)
	elif not(author_id in config_data["admins"]):
		emd = discord.Embed(title = "Удаление модераторов", description = "Удаление модераторов из базу бота", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def плюс_модер(ctx, member: discord.Member,*, reason = None ):
	author_id = "{0.author.id}".format(ctx)
	user_id = "{0.id}".format(member)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if author_id in config_data["admins"]:
		if not(user_id in config_data["moderations"]):
			config_data["moderations"].append("{0}".format(user_id))
			with open('config.json', 'w') as configFile:
				json.dump(config_data, configFile)
			emd = discord.Embed(title = "Добавление модераторов", description = "Добавление модераторов в базу бота", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Добавен", inline = True)
			emd.add_field(name = "Добавлен", value = "{0}".format(member), inline = True)
			await ctx.send(embed = emd)
			emd = discord.Embed(title = "Вы модератор", description = "Вы были добавлены в список модераторов бота", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Добавлен", inline = True)
			await member.send(embed = emd)
		if user_id in config_data["moderations"]:
			emd = discord.Embed(title = "Добавление модераторов", description = "Добавление модераторов в базу бота", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Уже есть в базе", inline = True)
			await ctx.send(embed = emd)
	elif not(author_id in config_data["admins"]):
		emd = discord.Embed(title = "Добавление модераторов", description = "Добавление модераторов в базу бота", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)


			
@Bot.command(pass_context = True)
async def кик(ctx, member: discord.Member,*, reason = None ):
	author_id = "{0.author.id}".format(ctx)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if author_id in config_data["admins"]:
		try:
			await member.kick(reason = reason)
			emd = discord.Embed(title = "Кик пользователей", description = "Кик пользователей с сервера", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Кикнут", inline = True)
			emd.add_field(name = "Кикнут", value = "{0} - {0.id}".format(member), inline = True)
			await ctx.send(embed = emd)
		except:
			emd = discord.Embed(title = "Кик пользователей", description = "Кик пользователей с сервера", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Ошибка", inline = True)
			emd.add_field(name = "Возможные причины ошибки", value = "Пользователя нету на сервере или является админом", inline = False)
			await ctx.send(embed = emd)
	elif not(author_id in config_data["admins"]):
		emd = discord.Embed(title = "Кик пользователей", description = "Кик пользователей с сервера", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def бан(ctx, member: discord.Member,*, reason = None ):
	author_id = "{0.author.id}".format(ctx)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if author_id in config_data["admins"]:
		try:
			await member.ban(reason = reason)
			emd = discord.Embed(title = "Бан пользователей", description = "Бан пользователей с сервера", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Забанен", inline = True)
			emd.add_field(name = "Забанен", value = "{0} - {0.id}".format(member), inline = True)
			await ctx.send(embed = emd)
		except:
			emd = discord.Embed(title = "Бан пользователей", description = "Бан пользователей с сервера", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Ошибка", inline = False)
			emd.add_field(name = "Возможные причины ошибки", value = "Пользователя нету на сервере или является админом", inline = True)
			await ctx.send(embed = emd)
	elif not(author_id in config_data["admins"]):
		emd = discord.Embed(title = "Бан пользователей", description = "Бан пользователей с сервера", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def время(ctx):
	hour =  time.strftime("%H", time.localtime())
	hour = int(hour) + 1
	if hour == 24:
		hour = 0
	emd = discord.Embed(title = "Показ времени", description = "Показывает время и дату", color = discord.Color.blue())
	emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
	emd.add_field(name = "Часовой пояс", value = "Москва (+ 1 час)", inline = False)
	emd.add_field(name = "Часов", value ="{0}".format(hour), inline = True)
	emd.add_field(name = "Минут", value =  "{0}".format(time.strftime("%M", time.localtime())), inline = True)
	await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def СПП(ctx, member: discord.Member,*, reason = None ):
	author_id = "{0.author.id}".format(ctx)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if (author_id in config_data["admins"]) or (author_id in config_data["moderations"]):
		try:
			emd = discord.Embed(title = "Здавствуйте", description = "Я <Rick>, и готов помочь вам...", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Напишите", value = "=помощь", inline = True)
			await member.send(embed = emd)
			emd = discord.Embed(title = "Отправка приветия", description = "Отправка приветвия в личные сообщения ботом", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отправлено", inline = True)
			await ctx.send(embed = emd)
		except:
			emd = discord.Embed(title = "Отправка приветия", description = "Отправка приветвия в личные сообщения ботом", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Ошибка", inline = True)
			emd.add_field(name = "Возможные причины ошибки", value =  "Пользователя несуществует или неправильно введён member", inline = False)
			await ctx.send(embed = emd)
	elif not((author_id in config_data["admins"]) or (author_id in config_data["moderations"])):
		emd = discord.Embed(title = "Отправка приветия", description = "Отправка приветвия в личные сообщения ботом", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def плюс_юзер(ctx, member: discord.Member,*, reason = None ):
	author_id = "{0.author.id}".format(ctx)
	user_id = "{0.id}".format(member)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if (author_id in config_data["admins"]) or (author_id in config_data["moderations"]):
		with open('users_data.json') as usersFile:
			users = json.load(usersFile)
		if user_id in users["users_id"]:
			emd = discord.Embed(title = "Добавление пользователей", description = "Добавление пользоваетелей в базу бота", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Пользователь уже есть в базе", inline = True)
			await ctx.send(embed = emd)
		elif not(user_id in users["users_id"]):
			users["users_id"].append("{0}".format(user_id))
			user_data = {"name": "{0}".format(member), "id": "{0}".format(user_id), "warnings": 0, "money": 1000, "inventory_id": [], "inventory": []}
			users["users"].append(user_data)
			with open('users_data.json', 'w') as usersFile:
				json.dump(users, usersFile)
			emd = discord.Embed(title = "Добавление пользователей", description = "Добавление пользоваетелей в базу бота", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Добавлен", inline = True)
			await ctx.send(embed = emd)
	elif not((author_id in config_data["admins"]) or (author_id in config_data["moderations"])):
		emd = discord.Embed(title = "Добавление пользователей", description = "Добавление пользоваетелей в базу бота", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def варн(ctx, member: discord.Member,*, reason = None ):
	author_id = "{0.author.id}".format(ctx)
	user_id = "{0.id}".format(member)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if (author_id in config_data["admins"]) or (author_id in config_data["moderations"]):
		with open('users_data.json') as usersFile:
			users = json.load(usersFile)
		if user_id in users["users_id"]:
			wag = 0
			while True:
				if users["users"][wag]["id"] == user_id:
					break
				wag += 1
			if users["users"][wag]["warnings"] != 3:
				users["users"][wag]["warnings"] += 1
				with open('users_data.json', 'w') as usersFile:
					json.dump(users, usersFile)
				emd = discord.Embed(title = "Предупреждение", description = "Выдача предупреждения пользователю", color = discord.Color.blue())
				emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
				emd.add_field(name = "Предупреждений", value = "{0}".format(users["users"][wag]["warnings"]), inline = True)
				emd.add_field(name = "Статус", value = "Выдано", inline = True)
				await ctx.send(embed = emd)
				emd = discord.Embed(title = "Предупреждение", description = "Выдача предупреждения пользователю", color = discord.Color.red())
				emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
				emd.add_field(name = "Предупреждений", value = "{0}".format(users["users"][wag]["warnings"]), inline = True)
				emd.add_field(name = "Статус", value = "Выдано", inline = True)
				await member.send(embed = emd)
			elif users["users"][wag]["warnings"] == 3:
				emd = discord.Embed(title = "Предупреждение", description = "Выдача предупреждения пользователю", color = discord.Color.blue())
				emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
				emd.add_field(name = "Статус", value = "Отменено", inline = True)
				emd.add_field(name = "Причина", value = "У пользователя уже 3 предупреждения", inline = True)
				emd.add_field(name = "Совет", value = "Кикнут млм забанить", inline = False)
				await member.send(embed = emd)
		elif not(user_id in users["users_id"]):
			emd = discord.Embed(title = "Предупреждение", description = "Выдача предупреждения пользователю", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Пользователя нету в базе бота", inline = True)
			await ctx.send(embed = emd)
	elif not((author_id in config_data["admins"]) or (author_id in config_data["moderations"])):
		emd = discord.Embed(title = "Предупреждение", description = "Выдача предупреждения пользователю", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def минус_варн(ctx, member: discord.Member,*, reason = None ):
	author_id = "{0.author.id}".format(ctx)
	user_id = "{0.id}".format(member)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if (author_id in config_data["admins"]) or (author_id in config_data["moderations"]):
		with open('users_data.json') as usersFile:
			users = json.load(usersFile)
		wag = 0
		while True:
			if users["users"][wag]["id"] == user_id:
				break
			wag += 1
		if users["users"][wag]["warnings"] > 0:
			users["users"][wag]["warnings"] = 0
			with open('users_data.json', 'w') as usersFile:
				json.dump(users, usersFile)
			emd = discord.Embed(title = "Удаление предупреждений", description = "Удаление предупреждений пользователя", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Удалены", inline = True)
			await ctx.send(embed = emd)
			emd = discord.Embed(title = "Удаление предупреждений", description = "Удаление предупреждений пользователя", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Удалены", inline = True)
			await member.send(embed = emd)
		elif users["users"][wag]["warnings"] <= 0:
			emd = discord.Embed(title = "Удаление предупреждений", description = "Удаление предупреждений пользователя", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "У пользователя нету предепреждений", inline = True)
			await ctx.send(embed = emd)
	elif not((author_id in config_data["admins"]) or (author_id in config_data["moderations"])):
		emd = discord.Embed(title = "Удаление предупреждений", description = "Удаление предупреждений пользователя", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def купить(ctx, amount = 0):
	author_id = "{0.author.id}".format(ctx)
	with open('users_data.json') as usersFile:
		users = json.load(usersFile)
	if author_id in users["users_id"]:
		wag = 0
		while True:
			if author_id == users["users"][wag]["id"]:
				break
			wag += 1
		with open('score.json') as scoreData:
			score = json.load(scoreData)
		if amount == 0:
			emd = discord.Embed(title = "Магазин", description = "Купите, что-то себе...", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Нету такого товара или вы нечего не ввели", inline = True)
			await ctx.send(embed = emd)
		else:
			if amount != 0:
				if not(amount in users["users"][wag]["inventory_id"]):
					if amount in score["range_id"]:
						users["users"][wag]["inventory_id"].append(int(amount))
						wag_range = 0
						while True:
							if score["range"][wag_range]["id"] == int(amount):
								break
							wag_range += 1
						users["users"][wag]["inventory"].append(score["range"][wag_range])
						users["users"][wag]["money"] -= score["range"][wag_range]["sell"]
						emd = discord.Embed(title = "Магазин", description = "Купите, что-то себе...", color = discord.Color.blue())
						emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
						emd.add_field(name = "Статус", value = "Куплен", inline = False)
						emd.add_field(name = "Куплен за", value = "{0} флорбо".format(score["range"][wag_range]["sell"]), inline = True)
						emd.add_field(name = "Куплен", value = "{0}".format(score["range"][wag_range]["name"]), inline = True)
						await ctx.send(embed = emd)
					elif not(amount in score["range_id"]):
						emd = discord.Embed(title = "Магазин", description = "Купите, что-то себе...", color = discord.Color.red())
						emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
						emd.add_field(name = "Статус", value = "Отменено", inline = True)
						emd.add_field(name = "Причина", value = "Нету такого товара", inline = True)
						await ctx.send(embed = emd)
				elif amount in users["users"][wag]["inventory_id"]:
					emd = discord.Embed(title = "Магазин", description = "Купите, что-то себе...", color = discord.Color.red())
					emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
					emd.add_field(name = "Статус", value = "Отменено", inline = True)
					emd.add_field(name = "Причина", value = "У вас уже есть этот предмет", inline = True)
					await ctx.send(embed = emd)
			else:
				emd = discord.Embed(title = "Магазин", description = "Купите, что-то себе...", color = discord.Color.red())
				emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
				emd.add_field(name = "Статус", value = "Отменено", inline = True)
				emd.add_field(name = "Причина", value = "Ошибка", inline = True)
				emd.add_field(name = "Возможные причины ошибки", value = "Неправильно введён айди товара", inline = False)
				await ctx.send(embed = emd)
		with open('users_data.json', 'w') as usersFile:
			json.dump(users, usersFile)
	elif not(author_id in users["users_id"]):
		emd = discord.Embed(title = "Магазин", description = "Купите, что-то себе...", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Нету в базе бота", inline = True)
		emd.add_field(name = "Что делать?", value = "Напишите, админам или модераторам они вас добавят", inline = False)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def продать(ctx, amount = 0):
	author_id = "{0.author.id}".format(ctx)
	with open('users_data.json') as usersFile:
		users = json.load(usersFile)
	if author_id in users["users_id"]:
		wag = 0
		while True:
			if author_id == users["users"][wag]["id"]:
				break
			wag += 1
		if not(amount in users["users"][wag]["inventory_id"]):
			emd = discord.Embed(title = "Айкцион", description = "Продайте, что-то не нужное...", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "У вас нету этого предмета", inline = True)
			await ctx.send(embed = emd)
		elif amount in users["users"][wag]["inventory_id"]:
			wag_item = 0
			while True:
				if users["users"][wag]["inventory"][wag_item]["id"] == amount:
					break
				wag_item += 1
			users["users"][wag]["money"] += users["users"][wag]["inventory"][wag_item]["cost"]
			cost_copy = users["users"][wag]["inventory"][wag_item]["cost"]
			name_copy = users["users"][wag]["inventory"][wag_item]["name"]
			del users["users"][wag]["inventory"][wag_item]
			del users["users"][wag]["inventory_id"][wag_item]
			emd = discord.Embed(title = "Айкцион", description = "Продайте, что-то не нужное...", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Продано", inline = True)
			emd.add_field(name = "Продана за", value = "{0} флорбо".format(cost_copy), inline = True)
			emd.add_field(name = "Продан", value = "{0}".format(name_copy), inline = True)
			await ctx.send(embed = emd)
	elif not(author_id in users["users_id"]):
		emd = discord.Embed(title = "Айкцион", description = "Продайте, что-то не нужное...", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Нету в базе бота", inline = True)
		emd.add_field(name = "Что делать?", value = "Напишите, админам или модераторам они вас добавят", inline = False)
		await ctx.send(embed = emd)
	with open('users_data.json', 'w') as usersFile:
		json.dump(users, usersFile)

@Bot.command(pass_context = True)
async def магазин(ctx):
	author_id = "{0.author.id}".format(ctx)
	with open('users_data.json') as usersFile:
		users = json.load(usersFile)
	if author_id in users["users_id"]:
		with open('score.json') as scoreData:
			score = json.load(scoreData)
		score_int = len(score["range"])
		emd = discord.Embed(title = "Магазин", description = "Вот, наш ассортимент...", color = discord.Color.blue())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		wag_score_range = 0
		while True:
			if wag_score_range == score_int:
				break
			emd.add_field(name = "{0} - {1}".format(score["range"][wag_score_range]["name"], score["range"][wag_score_range]["id"]), value = "{0} флорбо".format(score["range"][wag_score_range]["sell"]), inline = False)
			wag_score_range += 1
		await ctx.send(embed = emd)
	elif not(author_id in users["users_id"]):
		emd = discord.Embed(title = "Магазин", description = "Вот, наш ассортимент...", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Нету в базе бота", inline = True)
		emd.add_field(name = "Что делать?", value = "Напишите, админам или модераторам они вас добавят", inline = False)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def помощь(ctx):
	await ctx.channel.purge(limit = 1)
	author_id = "{0.author.id}".format(ctx)
	with open('users_data.json') as usersFile:
		users = json.load(usersFile)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if author_id in users["users_id"]:
		emd = discord.Embed(title = "Помощь", color = discord.Color.green())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "=время", value = "Показывает время", inline = False)
		emd.add_field(name = "=профиль", value = "Показывает ваши данные", inline = False)
		emd.add_field(name = "=магазин", value = "Показывает ассортимент c их айди", inline = False)
		emd.add_field(name = "=купить {id}", value = "Покупаете предмет из магазина", inline = False)
		emd.add_field(name = "=продать {id}", value = "Продаёте что-то из инвентаря", inline = False)
		emd.add_field(name = "=копать", value = "Вы начинаете копать руду", inline = False)
		if (author_id in config_data["admins"]) or (author_id in config_data["moderations"]):
			emd.add_field(name = "=СПП {member}", value = "Отправляет приветвие бота", inline = False)
			emd.add_field(name = "=ОПП {member} {ссылка приглашения}", value = "Отправляет пользователю приглашение", inline = False)
			emd.add_field(name = "=варн {member}", value = "Выдаёт предупреждение", inline = False)
			emd.add_field(name = "=минус_варн {member}", value = "Убирает все предупреждений", inline = False)
			emd.add_field(name = "=удалить {количество}", value = "Удаляет определёное количество последних сообщений", inline = False)
		if author_id in config_data["admins"]:
			emd.add_field(name = "=кик {member}", value = "Кикает пользователей с сервера", inline = False)
			emd.add_field(name = "=бан {member}", value = "Банит пользователей с сервера", inline = False)
			emd.add_field(name = "=плюс_модер {member}", value = "Добавляет модератора", inline = False)
			emd.add_field(name = "=минус_модер {member}", value = "Убирает модератора", inline = False)
			emd.add_field(name = "=плюс_юзер {member}", value = "Добавляет пользователя в базу бота", inline = False)
		if author_id == "384060067680616468":
			emd.add_field(name = "=плюс_админ {member}", value = "Добавляет админа", inline = False)
			emd.add_field(name = "=минус_админ {member}", value = "Убирает админа", inline = False)
		await ctx.author.send(embed = emd)
	elif not(author_id in users["users_id"]):
		emd = discord.Embed(title = "Помощь", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.set_image(url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Нету в базе бота", inline = True)
		emd.add_field(name = "Что делать?", value = "Напишите, админам или модераторам они вас добавят", inline = False)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def профиль(ctx):
	author_id = "{0.author.id}".format(ctx)
	with open('users_data.json') as usersFile:
		users = json.load(usersFile)
	if author_id in users["users_id"]:
		wag = 0
		while True:
			if author_id == users["users"][wag]["id"]:
				break
			wag += 1
		emd = discord.Embed(title = "Профиль", color = discord.Color.blue())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.set_image(url = "{0.avatar_url}".format(ctx.author))
		with open('config.json') as configData:
			config = json.load(configData)
		while True:
			if author_id in config["admins"]:
				role_user = "Админ"
				break
			elif author_id in config["moderations"]:
				role_user = "Модератор"
				break
			else:
				role_user = "Участник"
				break
		emd.add_field(name = "Должность", value = "{0}".format(role_user), inline = True)
		emd.add_field(name = "ID", value = "{0.id}".format(ctx.author), inline = True)
		emd.add_field(name = "Баланс", value = "{0} флорбо".format(users["users"][wag]["money"]), inline = False)
		emd.add_field(name = "Предупреждений", value = "{0}".format(users["users"][wag]["warnings"]), inline = True)
		wag_text = 0
		inventory_int = len(users["users"][wag]["inventory"])
		text_inventory = ""
		if inventory_int != 0:
			while True:
				if wag_text == inventory_int:
					break
				if wag_text == 0:
					text_inventory = text_inventory + "{0}".format(users["users"][wag]["inventory"][wag_text]["name"])
				elif wag_text != 0:
					text_inventory = text_inventory + ", {0}".format(users["users"][wag]["inventory"][wag_text]["name"])
				wag_text += 1
		elif inventory_int == 0:
			text_inventory = "Пусто"
		emd.add_field(name = "Инвентарь", value = "{0}".format(text_inventory), inline = False)
		await ctx.send(embed = emd)
	elif not(author_id in users["users_id"]):
		emd = discord.Embed(title = "Показ профиля", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.set_image(url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Нету в базе бота", inline = True)
		emd.add_field(name = "Что делать?", value = "Напишите, админам или модераторам они вас добавят", inline = False)
		await ctx.send(embed = emd)

@Bot.command(pass_context = True)
async def ОПП(ctx, member: discord.Member, amount = ""):
	author_id = "{0.author.id}".format(ctx)
	with open('config.json') as configFile:
		config_data = json.load(configFile)
	if (author_id in config_data["admins"]) or (author_id in config_data["moderations"]):
		if len(amount) != 0:
			emd = discord.Embed(title = "Отправка приглашений пользователю", color = discord.Color.blue())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отправлено", inline = True)
			await ctx.send(embed = emd)
			emd = discord.Embed(title = "Вам приглашение", description = "Вас пригласил {0.author},\nв {1}".format(ctx, amount), color = discord.Color.green())
			emd.set_author(name = "{0}".format(member), icon_url = "{0.avatar_url}".format(member))
			await member.send(embed = emd)
		elif len(amount) == 0:
			emd = discord.Embed(title = "Отправка приглашений пользователю", color = discord.Color.red())
			emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
			emd.add_field(name = "Статус", value = "Отменено", inline = True)
			emd.add_field(name = "Причина", value = "Ссылка не введена", inline = True)
			await ctx.send(embed = emd)
	elif not((author_id in config_data["admins"]) or (author_id in config_data["moderations"])):
		emd = discord.Embed(title = "Отправка приглашений пользователю", color = discord.Color.red())
		emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
		emd.add_field(name = "Статус", value = "Отменено", inline = True)
		emd.add_field(name = "Причина", value = "Недостаток прав", inline = True)
		await ctx.send(embed = emd)

@Bot.event
async def on_command_error(ctx, error):
	emd = discord.Embed(title = "Ошибка команды", color = discord.Color.red())
	emd.set_author(name = "{0.author}".format(ctx), icon_url = "{0.avatar_url}".format(ctx.author))
	emd.add_field(name = "Статус", value = "Отправлено", inline = False)
	emd.add_field(name = "Ошибка", value = f"{error}", inline = False)
	emd.add_field(name = "Причина", value = "Неправильно введена команда", inline = False)
	await ctx.send(embed = emd)

# При включение
@Bot.event
async def on_ready():
	print('Bot теперь в сети')

# Авторизация
with open('config.json') as configFile:
	config_data = json.load(configFile)

token = (config_data["token"])
Bot.run(token)
