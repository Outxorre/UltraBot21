import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "cool_points.json"

# Загружаем данные
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        points = json.load(f)
else:
    points = {}

def save_points():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(points, f, indent=4)

def get_user_id(user):
    return str(user.id)

def add_points(user, amount):
    uid = get_user_id(user)
    points[uid] = points.get(uid, 0) + amount
    save_points()

def get_points(user):
    return points.get(get_user_id(user), 0)

# Команда: !очки @пользователь
@bot.command()
async def очки(ctx, member: discord.Member):
    score = get_points(member)
    await ctx.send(f"У {member.display_name} {score} очков крутости")

# Команда: !сколько у меня очков
@bot.command(name="сколько")
async def сколько_у_меня_очков(ctx):
    score = get_points(ctx.author)
    await ctx.send(f"{ctx.author.display_name}, у тебя {score} очков крутости")

# Команда: !плюс 5 (ответом на сообщение)
@bot.command()
@has_permissions(administrator=True)
async def плюс(ctx, amount: int):
    if ctx.message.reference:
        replied = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        target_user = replied.author
        add_points(target_user, amount)
        await ctx.send(f"{target_user.display_name} получил {amount} очков крутости!")
    else:
        await ctx.send("Ответь на сообщение пользователя, которому хочешь добавить очки!")

# Команда: !минус 5 (ответом на сообщение)
@bot.command()
@has_permissions(administrator=True)
async def минус(ctx, amount: int):
    if ctx.message.reference:
        replied = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        target_user = replied.author
        add_points(target_user, -amount)
        await ctx.send(f"{target_user.display_name} потерял {amount} очков крутости...")
    else:
        await ctx.send("Ответь на сообщение пользователя, у которого хочешь отнять очки!")

# Обработка ошибки прав
@плюс.error
@минус.error
async def permission_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("СОСИ МОЮ ЖОПУ У ТЕБЯ НЕТ АДМИНКИ")

# Запуск
bot.run("ТВОЙ_ТОКЕН_БОТА")