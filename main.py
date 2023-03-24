import discord
from discord.ext import commands
from keep_alive import keep_alive
from datetime import datetime
import datetime
import requests
from jikanpy import Jikan
from jikanpy.exceptions import APIException
import qrcode
import jikanpy
import aiohttp
import random
import os

afk_users = {}
jikan = jikanpy.Jikan()
	
GIPHY_API_KEY = os.getenv('gvtSvH8OHsBP4CP91WAtQgsdemioBnqe')

blacklist = ["1234567890", "0987654321"]
bot = commands.Bot(command_prefix="m/", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Miku is online")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Jugando a ser un bot'))

@bot.command()
async def hello(ctx):
    username = ctx.message.author.mention
    await ctx.send("Hola mi querid@ amig@ " + username)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def ban(ctx, member:discord.Member, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned by {ctx.author.mention} for {reason}.")

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def kick(ctx, member:discord.Member, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked by {ctx.author.mention} for {reason}.")

@bot.command()
async def mute(ctx, member:discord.Member, timelimit="604800"):
    if not timelimit:
        await ctx.send("Please provide a valid timelimit")
        return
    if "s" in timelimit:
        gettime = ''.join(filter(str.isdigit, timelimit))
        newtime = datetime.timedelta(seconds=int(gettime))
        await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
        await ctx.send(f"{member.mention} has been muted by {ctx.author.mention} for {gettime} seconds.")
    else:
        await ctx.send("Please provide a valid timelimit")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message):
    await ctx.send(message)

@bot.command()
async def bola8(ctx, *, question):
    responses = ["Sí", "No", "Quizás", "Probablemente", "No lo sé", "Absolutamente", "Nunca", "Tal vez"]

    await ctx.send(f"🎱 **Pregunta:** {question}\n🎱 **Respuesta:** {random.choice(responses)}")

@bot.command()
async def rps(ctx):
    emojis = ['🪨', '📜', '✂️'] # Emoji para piedra, papel y tijera respectivamente
    results = ['Empate', 'Ganaste', 'Perdiste'] # Resultados posibles del juego
    
    def check_win(p1, p2):
        if p1 == p2:
            return results[0] # Empate
        elif (p1 == emojis[0] and p2 == emojis[2]) or (p1 == emojis[1] and p2 == emojis[0]) or (p1 == emojis[2] and p2 == emojis[1]):
            return results[1] # Ganaste
        else:
            return results[2] # Perdiste
    
    embed = discord.Embed(title="Piedra, Papel o Tijera", description="Reacciona al emoji correspondiente para jugar:", color=discord.Color.green())
    embed.add_field(name="Piedra", value=emojis[0])
    embed.add_field(name="Papel", value=emojis[1])
    embed.add_field(name="Tijera", value=emojis[2])
    msg = await ctx.send(embed=embed)
    
    for emoji in emojis:
        await msg.add_reaction(emoji)
        
    def check_reaction(reaction, user):
        return user == ctx.author and str(reaction.emoji) in emojis and reaction.message.id == msg.id
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check_reaction)
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, tiempo agotado. Vuelve a intentarlo.")
    else:
        bot_choice = random.choice(emojis)
        result = check_win(str(reaction.emoji), bot_choice)
        
        embed_result = discord.Embed(title="Resultado", color=discord.Color.green())
        embed_result.add_field(name="Tu elección", value=str(reaction.emoji))
        embed_result.add_field(name="Elección del bot", value=bot_choice)
        embed_result.add_field(name="Resultado", value=result)
        
        await ctx.send(embed=embed_result)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('m/afk '):
        afk_users[message.author.id] = message.content[7:]
        await message.channel.send(f"{message.author.mention} está ahora AFK: {afk_users[message.author.id]}")
    elif message.author.id in afk_users:
        del afk_users[message.author.id]
        await message.channel.send(f"{message.author.mention} ya no está AFK.")
    else:
        for user_id in afk_users:
            user = await bot.fetch_user(user_id)
            if message.content.find(user.mention) != -1:
                await message.channel.send(f"{message.author.mention}, {user.mention} está AFK: {afk_users[user_id]}")
                break
    await bot.process_commands(message)

@bot.command()
async def qr(ctx, *, text: str):
    qr_img = qrcode.make(text)
    qr_img.save('qr.png')
    with open('qr.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@bot.command()
async def afk(ctx, *, message=""):
    afk_users[ctx.author.id] = message
    await ctx.send(f"{ctx.author.mention} está ahora AFK: {message}")

@bot.command()
async def unafk(ctx):
    if ctx.author.id in afk_users:
        del afk_users[ctx.author.id]
        await ctx.send(f"{ctx.author.mention} ya no está AFK.")
    else:
        await ctx.send(f"{ctx.author.mention} no está AFK.")

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned by {ctx.author.mention}.")
            return

    await ctx.send(f"Could not find a ban entry for {member}.")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! Mi latencia es {round(bot.latency * 1000)}ms.")


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    embed = discord.Embed(title=f"Avatar de {member}", color=discord.Color.purple())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def unkick(ctx, member: discord.Member):
    """
    Deshace el último kick realizado por un moderador.
    """
    audit_logs = await ctx.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
    for entry in audit_logs:
        if entry.target == member:
            await entry.target.edit(roles=entry.before.roles)
            await ctx.send(f"{entry.target.mention} ha sido desbaneado por {entry.user.mention}")
            return
    await ctx.send(f"No se ha encontrado el registro de un kick reciente de {member.mention}")

@bot.event
async def on_message(message):
    # Comprueba si el usuario está en la lista negra
    if str(message.author.id) in blacklist:
        await message.channel.send(f"Lo siento, {message.author.mention}, estás en la lista negra y no puedes usar el bot.")
        return

    await bot.process_commands(message)

@bot.command()
async def blacklistadd(ctx, user_id: int):
    # Añade un usuario a la lista negra
    blacklist.append(str(user_id))
    await ctx.send(f"{user_id} ha sido añadido a la lista negra.")

@bot.command()
async def blacklistremove(ctx, user_id: int):
    # Elimina un usuario de la lista negra
    if str(user_id) in blacklist:
        blacklist.remove(str(user_id))
        await ctx.send(f"{user_id} ha sido eliminado de la lista negra.")
    else:
        await ctx.send(f"{user_id} no está en la lista negra.")

@bot.command()
async def kiss(ctx, member: discord.Member):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.giphy.com/v1/gifs/search?api_key=gvtSvH8OHsBP4CP91WAtQgsdemioBnqe&q=kiss&limit=5&offset=0&rating=g&lang=es"
        async with session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                if len(js['data']) > 0:
                    gif = js['data'][0]['url']
                    embed = discord.Embed(title=f"{ctx.author.display_name} besó a {member.display_name} 💋", color=0xff69b4)
                    embed.set_image(url=gif)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Lo siento, no pude encontrar ningún gif de beso 😔")
            else:
                await ctx.send("Ocurrió un error al obtener el gif de beso. Inténtalo de nuevo más tarde.")

@bot.command()
async def creador(ctx):
    embed = discord.Embed(title="Información del Creador", description="¡Hola! Mi nombre es Daniel (pero me dicen Dani o Seven), y soy el creador de este bot de Discord.", color=0xff69b4)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/935293477904846888/1018678032350847006/Picsart_22-09-09_23-14-53-339.jpg")
    embed.add_field(name="Nombre de usuario:", value="Rukkus#0072", inline=False)
    embed.add_field(name="Lenguaje de programación:", value="El bot ha sido programado usando Python y Discord.py. En la version 2.2.2 .", inline=False)
    embed.add_field(name="Descripción:", value="Este bot está diseñado para hacer que tu experiencia en el servidor sea más divertida y organizada. Con una amplia gama de comandos administrativos, de diversión y de utilidad, este bot es el compañero perfecto para cualquier servidor de Discord. Actualmente estoy intentando implementar una funcion de chatbot, que te permitirá hablar con el bot como si fuera una persona real. Mientras tanto, disfruta de lo que el bot ofrece :3", inline=False)
    embed.add_field(name="Agradecimientos:", value="Quiero agradecer a Whigrey y Exdetsoul por su ayuda en la creación de este bot, así como a hizer por proporcionar recursos útiles.", inline=False)
    embed.add_field(name="Redes sociales:", value="Puedes encontrarme en [Twitter](https://twitter.com/S_Kitty05) y [YouTube](https://www.youtube.com/channel/UCCawTLnpgbc7_ltyGScoQpw).", inline=False)
    embed.set_footer(text="Estatus del bot: Aún en desarrollo, por lo que se pueden encontrar errores.")
    await ctx.send(embed=embed)

@bot.command()
async def about(ctx):
    embed = discord.Embed(title="Acerca de", color=discord.Color.blue())
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.add_field(name="Nombre del bot", value=bot.user.name, inline=True)
    embed.add_field(name="Creador", value="Rukkus", inline=True)
    embed.add_field(name="Lenguaje de programación", value="Python 3.10", inline=True)
    embed.add_field(name="Librería de Discord", value="discord.py", inline=True)
    embed.add_field(name="Versión de la librería", value=discord.__version__, inline=True)
    embed.add_field(name="Servidores", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="Usuarios", value=str(len(set(bot.get_all_members()))), inline=True)
    embed.add_field(name="Comandos", value=str(len(bot.commands)), inline=True)
    embed.set_footer(text="¡Gracias por usar el bot!")
    await ctx.send(embed=embed)

@bot.command()
async def invitar(ctx):
    """
    Muestra un enlace para invitar al bot a tu servidor.
    """
    embed = discord.Embed(title="¡Invita a MyBot a tu servidor!", description="¡Haz clic en el enlace para invitar al bot a tu servidor!", color=discord.Color.green())
    embed.add_field(name="Enlace de invitación:", value="[Haz clic aquí](https://discord.com/oauth2/authorize?client_id=872866276232540190&scope=bot&permissions=2147483647)", inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/fu3yit1.png")
    await ctx.send(embed=embed)

@bot.command()
async def encuesta(ctx, pregunta: str, *opciones: str):
    # Lista de emojis que se usarán como opciones de respuesta
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    # Si no hay suficientes emojis para cada opción, se muestra un mensaje de error
    if len(opciones) > len(emojis):
        await ctx.send("Lo siento, solo puedo manejar hasta 10 opciones.")
        return

    # Construye la pregunta y las opciones de respuesta como un mensaje embed
    embed = discord.Embed(title="Encuesta", description=pregunta, color=discord.Color.blue())
    opciones_str = "\n".join([f"{emojis[i]} {opcion}" for i, opcion in enumerate(opciones)])
    embed.add_field(name="Opciones", value=opciones_str, inline=False)

    # Enviar el mensaje embed y agregar las reacciones correspondientes para cada opción
    message = await ctx.send(embed=embed)
    for i in range(len(opciones)):
        await message.add_reaction(emojis[i])

    await ctx.message.delete()  # Eliminar el mensaje del usuario que envió el comando

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    """
    Borra una cantidad especificada de mensajes en el canal actual.
    Solo puede ser utilizado por moderadores con permiso para gestionar mensajes.
    """
    if limit <= 0 or limit > 100:
        await ctx.send("Debes especificar un número entre 1 y 100.")
    else:
        try:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit)
            message = await ctx.send(f"Se han eliminado {len(deleted)} mensajes.")
            await asyncio.sleep(5)
            await message.delete()
        except discord.Forbidden:
            await ctx.send("No tengo los permisos necesarios para borrar mensajes.")
        except discord.HTTPException:
            await ctx.send("Se produjo un error al borrar los mensajes.")

@bot.command()
async def animegirl(ctx):
    response = requests.get("https://api.waifu.pics/sfw/neko")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes una linda chica anime!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def ship(ctx, user1: discord.Member, user2: discord.Member):
    """Ship two users together"""
    # Generate a random percentage for the ship
    ship_percent = random.randint(0, 100)

    # Create the ship name by combining the first three letters of each username
    ship_name = f"{user1.name[:3]}{user2.name[:3]}"

    # Generate the ship message with the percentage and ship name
    ship_message = f"He shipeado a  **{user1.display_name}** y **{user2.display_name}**! :heart:\nEl nombre del ship es **{ship_name}** Y su porcentaje de relacion es **{ship_percent}%**!"

    # Send the ship message in the channel where the command was used
    await ctx.send(ship_message)

@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(title="Comandos del bot", description="Aquí están todos los comandos disponibles en el bot:", color=discord.Color.blue())

    # División de comandos administrativos
    admin_cmds = ""
    admin_cmds += "**m/kick [usuario] [razón]**: Expulsa a un usuario del servidor\n"
    admin_cmds += "**m/mute [usuario] [tiempo]**: Mutea a un usuario por un tiempo específico\n"
    admin_cmds += "**m/unmute [usuario]**: Quita el mute de un usuario\n"
    admin_cmds += "**m/unban [usuario]**: Quita el baneo de un usuario\n"
    admin_cmds += "**m/unkick [usuario]**: Quita el kick de un usuario\n"
    admin_cmds += "**m/encuesta [pregunta]**: Crea una encuesta para que los usuarios voten\n"
    admin_cmds += "**m/purge [cantidad]**: Elimina la cantidad especificada de mensajes (solo moderadores)\n"
    embed.add_field(name="Comandos Administrativos", value=admin_cmds, inline=False)

   # División de comandos de diversión
    fun_cmds = ""
    fun_cmds += "**m/hello**: Saluda al usuario que ejecutó el comando\n"
    fun_cmds += "**m/say [mensaje]**: Envía un mensaje como el bot\n"
    fun_cmds += "**m/8ball [pregunta]**: Responde una pregunta de sí o no\n"
    fun_cmds += "**m/kiss [usuario]**: Besa a un usuario\n"
    fun_cmds += "**m/rps [piedra/papel/tijera]**: Juega piedra, papel o tijera con el bot\n"
    fun_cmds += "**m/animegirl**: Envía una imagen de una chica de anime\n"
    fun_cmds += "**m/ship [usuario1] [usuario2]**: Hace un shipeo entre dos usuarios\n"
    embed.add_field(name="Comandos de Diversión", value=fun_cmds, inline=False)
	
    # División de comandos de utilidad
    util_cmds = ""
    util_cmds += "**m/ping**: Muestra la latencia del bot\n"
    util_cmds += "**m/avatar**: Muestra el avatar de un usuario\n"
    util_cmds += "**m/afk [razón]**: Establece un estado de ausencia y muestra una respuesta personalizada cuando te mencionen\n"
    util_cmds += "**m/unafk**: Quita el estado de ausencia\n"
    util_cmds += "**m/qr [texto]**: Genera un código QR a partir de un texto\n"
    embed.add_field(name="Comandos de Utilidad", value=util_cmds, inline=False)

    # Comandos Misceláneos
    misc_cmds = ""
    misc_cmds += "**m/about**: Muestra información sobre el bot\n"
    misc_cmds += "**m/invite**: Genera un enlace para invitar al bot a tu servidor\n"
    misc_cmds += "**m/creador**: Muestra información sobre el creador y el bot\n"
    embed.add_field(name="Comandos Misceláneos", value=misc_cmds, inline=False)

    # Comando de ayuda
    help_cmds = ""
    help_cmds += "**m/ayuda**: Muestra este mensaje de ayuda\n"
    embed.add_field(name="Comandos de Ayuda", value=help_cmds, inline=False)
	
    await ctx.send(embed=embed)
	
keep_alive()
bot.run("ODcyODY2Mjc2MjMyNTQwMTkw.G82B10.a5sXNtGc203IgGRWmmDj52rvLgq7dqMtswMiJo")