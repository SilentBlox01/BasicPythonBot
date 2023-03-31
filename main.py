import discord
from discord.ext import commands
from keep_alive import keep_alive
from datetime import datetime
import datetime
import requests
from jikanpy import Jikan
from jikanpy.exceptions import APIException
from discord.ext.commands import Bot
import qrcode
import jikanpy
import json
import aiohttp
import random
import os
import asyncio
import math

afk_users = {}
jikan = jikanpy.Jikan()
	
GIPHY_API_KEY = os.getenv('gvtSvH8OHsBP4CP91WAtQgsdemioBnqe')

blacklist = ["1234567890", "0987654321"]
blacklisted_users = [123456789012345678, 987654321098765432]
bot = commands.Bot(command_prefix="m/", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Miku is online")
	
@bot.command()
async def hello(ctx):
    username = ctx.message.author.mention
    await ctx.send("Hola mi querid@ amig@ " + username)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def ban(ctx, member:discord.Member, reason="Sin razón establecida."):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} fue baneado por {ctx.author.mention} por {reason}.")

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def kick(ctx, member:discord.Member, reason="Sin razón establecida."):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} fue expulsado por {ctx.author.mention} por {reason}.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
async def serverinfo(ctx):
    """Muestra la información del servidor"""
    embed = discord.Embed(title="Información del servidor", color=0x9208ea)
    embed.add_field(name="Nombre del servidor", value=ctx.guild.name, inline=True)

    roles = ", ".join([role.name for role in ctx.guild.roles])
    embed.add_field(name="Roles", value=roles, inline=True)

    embed.add_field(name="Miembros", value=len(ctx.guild.members))
    embed.add_field(name="Canales", value=len(ctx.guild.channels))
    embed.add_field(name="Pedido por", value="{}".format(ctx.author.mention))
    embed.set_footer(text="Creado con amor")

    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    if member == ctx.bot.user:
        return await ctx.send("¿Qué quieres saber?, si soy yo misma :D")
    embed = discord.Embed(title=f"{member.name}'s Info", color=0x00f549)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Nombre de usuario:", value=member.name, inline=False)
    embed.add_field(name="Apodo:", value=member.nick or "Ninguno", inline=False)
    embed.add_field(name="ID de usuario:", value=member.id, inline=False)
    embed.add_field(name="Fecha de creación de la cuenta:", value=member.created_at.strftime("%m/%d/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Fecha de ingreso al servidor:", value=member.joined_at.strftime("%m/%d/%Y %H:%M:%S"), inline=False)
    roles = ", ".join([role.mention for role in member.roles if not role.is_default()])
    embed.add_field(name="Roles:", value=roles or "Ninguno", inline=False)
    embed.add_field(name="Estado:", value=str(member.status).title(), inline=False)
    activity = f"{str(member.activity.type).split('.')[-1].title()} {member.activity.name}" if member.activity else "Ninguna"
    embed.add_field(name="Actividad:", value=activity, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def morse(ctx, *, message):
    """Convierte un texto a código Morse"""
    morse_code = {
        'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
        'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
        'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
        's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
        'y': '-.--', 'z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
        '!': '-.-.--', '-': '-....-', '/': '-..-.', '@': '.--.-.', '(': '-.--.',
        ')': '-.--.-', ' ': '/'
    }

    # Convertimos el mensaje a minúsculas
    message = message.lower()

    # Creamos una lista con el código Morse correspondiente a cada caracter del mensaje
    morse_message = [morse_code.get(char, char) for char in message]

    # Unimos los caracteres con un espacio y enviamos el mensaje en código Morse
    await ctx.send(' '.join(morse_message))

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

@bot.command(pass_context=True)
async def kiss(ctx, member: discord.Member):
    if member == ctx.message.author:
        return await ctx.send("¡No puedes besarte a ti mismo!")
    if member == bot.user:
        return await ctx.send("Hmmm no, no gracias.")
    
    kisses = ['https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjM3ZjI3NzBmOGFhMTM5YmM1ZDYwYWE5MDVmZDk2YTM0NjE5ODMwNSZjdD1n/zkppEMFvRX5FC/giphy.gif',
              'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDU4Njc4NjRjNjdhZDE1OTM2YzJlMzE4NzkzNDRjYmM0ZTBhMWQzYiZjdD1n/MQVpBqASxSlFu/giphy.gif',
							'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYThlYTZmMzQzMzUyOTJlNDU5OTZmNjljNjQxYjUwNGM2NzYwNTA1MyZjdD1n/vaSA1fpCkY06I/giphy.gif',
							'https://media.giphy.com/media/XZYxeRlIEdmKI/giphy.gif',
							'https://media.giphy.com/media/12VXIxKaIEarL2/giphy.gif',
							'https://media.giphy.com/media/11rWoZNpAKw8w/giphy.gif',
							'https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif',
							'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExODhhYTlhMjhiMDE3ZjgzZDBmNzZmNTllNmUxZGIwZTU3YjNkMDA3MCZjdD1n/hnNyVPIXgLdle/giphy.gif',
							'https://media.giphy.com/media/FqBTvSNjNzeZG/giphy.gif']
    k = discord.Embed(description=f"¡{member.mention} recibió un beso de {ctx.message.author.mention}!", color=0xff69b4)
    k.set_image(url=random.choice(kisses))
    await ctx.send(embed=k)

@bot.command()
async def pat(ctx, member: discord.Member):
    if member == ctx.message.author:
        return await ctx.send("¡No puedes acariciarte a ti mismo!")
    if member == bot.user:
        return await ctx.send("Te lo agradezco, pero no tengo cuerpo para sentirlo")
    
    pats = ['https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDJiMTg0OTAxMDljYTA5ZTA0YjM1ZTJkYTgxZWVjYTJmZGEzNmRlNyZjdD1n/zIbMVLlZlYY2iX62kZ/giphy.gif',
            'https://media.giphy.com/media/osYdfUptPqV0s/giphy.gif',
            'https://media.giphy.com/media/5tmRHwTlHAA9WkVxTU/giphy.gif',
            'https://media.giphy.com/media/ye7OTQgwmVuVy/giphy.gif',
						'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTM4ODMxN2FhOWYzZTg4MzdlYjJmMGFhOTI0OWEzNWJhMjliYTM5MiZjdD1n/7weOpkiSaVOCmABmoK/giphy.gif',
						'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDdhMmExN2MyMjk4ZTNlYWM0MTJjM2U3M2M4NTA0ZmExZjNmMjk0MCZjdD1n/jNKYleiHDwypEPkymR/giphy.gif']
    
    pat = discord.Embed(description=f"¡{member.mention} recibió una caricia de {ctx.message.author.mention}!", color=0xff69b4)
    pat.set_image(url=random.choice(pats))
    await ctx.send(embed=pat)

@bot.command()
async def cry(ctx):
    cries = ['https://media.giphy.com/media/59d1zo8SUSaUU/giphy.gif',
             'https://media.giphy.com/media/Ui7MfO6OaLz4k/giphy.gif',
             'https://media.giphy.com/media/ShPv5tt0EM396/giphy.gif',
             'https://media.giphy.com/media/8YutMatqkTfSE/giphy.gif',
             'https://media.giphy.com/media/5t4gifYFrcwAcxt6t3/giphy.gif',
             'https://media.giphy.com/media/zHGXhFJCVCbD2/giphy.gif',
             'https://media.giphy.com/media/gMzPyvdzoDikU/giphy.gif',
             'https://media.giphy.com/media/AI7yqKC5Ov0B2/giphy.gif']

    cry = discord.Embed(description=f"{ctx.author.mention} está llorando 😢.", color=0xff69b4)
    cry.set_image(url=random.choice(cries))
    await ctx.send(embed=cry)

@bot.command()
async def hi(ctx, user: discord.Member = None):
    hi_gifs = ['https://media.giphy.com/media/AFdcYElkoNAUE/giphy.gif',
             'https://media.giphy.com/media/DHiqBbtjaB30s/giphy.gif',
             'https://media.giphy.com/media/yyVph7ANKftIs/giphy.gif',
             'https://media.giphy.com/media/AmVFCGRpBsY24/giphy.gif',
             'https://media.giphy.com/media/AsKhf57LTqQ9QvqKxC/giphy.gif',
             'https://media.giphy.com/media/n3wMtdOm17LwYh7Eac/giphy.gif',
             'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTU4OTAyZDVjNmU2NGIzNWQ1NzMzZDliMzMzODYwNTE5YTNhNmVkNCZjdD1n/OiPr3CaEoC2AKzKyfg/giphy.gif',
             'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWViYjliZDdlM2Q0ODdiZjUxMjMyOGNlYjRiMTFhOGMxZTA3MTliYyZjdD1n/FS2JF2NOyN9fJRS1wk/giphy.gif']

    if user is None:
        hi = discord.Embed(description=f"{ctx.author.mention} está saludando 👋.", color=discord.Color.blue())
        hi.set_image(url=random.choice(hi_gifs))
        await ctx.send(embed=hi)
    else:
        hi = discord.Embed(description=f"{ctx.author.mention} está saludando a {user.mention} 👋.", color=discord.Color.blue())
        hi.set_image(url=random.choice(hi_gifs))
        await ctx.send(embed=hi)

@bot.command()
async def hug(ctx, member: discord.Member):
    if member == ctx.message.author:
        return await ctx.send("¡No puedes abrazarte a ti mismo!")
    if member == bot.user:
        return await ctx.send("Gracias por tu amable gesto, pero no tengo cuerpo para recibir abrazos :3")
    
    hugs = ['https://media.giphy.com/media/lrr9rHuoJOE0w/giphy.gif',
            'https://media.giphy.com/media/IRUb7GTCaPU8E/giphy.gif',
            'https://media.giphy.com/media/qscdhWs5o3yb6/giphy.gif',
            'https://media.giphy.com/media/GMFUrC8E8aWoo/giphy.gif',
            'https://media.giphy.com/media/JLovyTOWK4cuc/giphy.gif',
						'https://media.giphy.com/media/LIqFOpO9Qh0uA/giphy.gif',
						'https://media.giphy.com/media/5eyhBKLvYhafu/giphy.gif']
    
    hug = discord.Embed(description=f"¡{member.mention} recibió un abrazo de {ctx.message.author.mention}!", color=0xff69b4)
    hug.set_image(url=random.choice(hugs))
    await ctx.send(embed=hug)

@bot.command()
async def slap(ctx, member: discord.Member):
    if member == ctx.message.author:
        return await ctx.send("No seas estupido, ¿Para qué quieres abofetearte a ti mismo? T-T")
    if member == bot.user:
        return await ctx.send("E-e-en serio ¿quieres abofetearme? No, no puedo creerlo. ¿Por qué querrías hacer algo así? Yo... yo no he hecho nada malo, ¿verdad? Oh, por favor, no lo hagas.")
    
    slaps = ['https://media.giphy.com/media/tX29X2Dx3sAXS/giphy.gif',
             'https://media.giphy.com/media/k1uYB5LvlBZqU/giphy.gif',
             'https://media.giphy.com/media/9U5J7JpaYBr68/giphy.gif',
             'https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif',
             'https://media.giphy.com/media/6Fad0loHc6Cbe/giphy.gif',
						 'https://media.giphy.com/media/xUNd9HZq1itMkiK652/giphy.gif']
    
    slap = discord.Embed(description=f"¡{member.mention} fue abofeteado por {ctx.message.author.mention}!", color=0xff69b4)
    slap.set_image(url=random.choice(slaps))
    await ctx.send(embed=slap)

@bot.command()
async def knockout(ctx, member: discord.Member):
    if member == ctx.message.author:
        return await ctx.send("¿Necesitas ayuda?")
    if member == bot.user:
        return await ctx.send("E-eh... ¿en verdad quieres noquearme? No estoy segura de que sea una buena idea, ¿sabes? Es decir, no creo que sea necesario llegar a ese extremo. No quiero meterme en problemas contigo, pero no me siento cómoda con esta situación. ¿Podríamos resolver esto de otra manera?")
    
    knockouts = ['https://media.giphy.com/media/kqvXSKcCgI8BLdkPUp/giphy.gif',
                 'https://media.giphy.com/media/4oPI0FmV4e34XWeUq9/giphy.gif',
                 'https://media.giphy.com/media/jbhLppNiWrTXRrjgCh/giphy.gif',
                 'https://media.giphy.com/media/Ctb7y7oLeZpUsZwlhG/giphy.gif',
                 'https://media.giphy.com/media/TnzPcwFLl1ztXX2UfD/giphy.gif',
								 'https://media.giphy.com/media/pdSDauIEkPscuipQbP/giphy.gif',
								 'https://media.giphy.com/media/sC1PWN9DV0QXKJCalZ/giphy.gif']
    
    knockout = discord.Embed(description=f"¡{member.mention} ha sido noqueado por {ctx.message.author.mention}!", color=0xff0000)
    knockout.set_image(url=random.choice(knockouts))
    await ctx.send(embed=knockout)

@bot.command()
async def punch(ctx, member: discord.Member):
    if member == ctx.message.author:
        return await ctx.send("¡No puedes golpearte a ti mismo!")
    if member == bot.user:
        return await ctx.send("¡No me golpees! ¡Solo soy un bot!")
    
    punches = ['https://media.giphy.com/media/12n2skyAAjOGhq/giphy.gif',
               'https://media.giphy.com/media/Z5zuypybI5dYc/giphy.gif',
               'https://media.giphy.com/media/okECPQ0lVQeD6/giphy.gif',
               'https://media.giphy.com/media/S8nGEQ0yR8z6M/giphy.gif',
               'https://media.giphy.com/media/1Bgr0VaRnx3pCZbaJa/giphy.gif',
               'https://media.giphy.com/media/11HeubLHnQJSAU/giphy.gif','https://media.giphy.com/media/HhOyX2GniWeSsyuhw3/giphy.gif',
							 'https://media.giphy.com/media/HhOyX2GniWeSsyuhw3/giphy.gif',
							 'https://media.giphy.com/media/yBeej2d9kB4FYXeg2Z/giphy.gif',
							 'https://media.giphy.com/media/cBruI3Qdn6hOhMidkt/giphy.gif',
							 'https://media.giphy.com/media/loYc1ZY5iIziuGAc3I/giphy.gif',
							 'https://media.giphy.com/media/lr3sdw7Ti0cmiQinvg/giphy.gif',
							 'https://media.giphy.com/media/mQvhVqt4xhYsMhOO3B/giphy.gif']
    
    punch = discord.Embed(description=f"¡{member.mention} recibió un puñetazo de {ctx.message.author.mention}!", color=0xff69b4)
    punch.set_image(url=random.choice(punches))
    await ctx.send(embed=punch)

@bot.command()
async def patear(ctx, member: discord.Member):
    if member == ctx.message.author:
        return await ctx.send("Hay Dios T-T")
    if member == bot.user:
        return await ctx.send("E-e-en s-serio... ¿q-quieres p-patearme? No entiendo por qué, ¿qué he hecho mal? ¿A-algo te ha molestado? Lo siento si te he ofendido, por favor, no me hagas daño.")
    
    kicks = ['https://media.giphy.com/media/qrXbqxGJq91ceNXOfM/giphy.gif',
             'https://media.giphy.com/media/40hu2eMWSLmBqS00nz/giphy.gif',
             'https://media.giphy.com/media/Pq9wegdS2sE8cfDQIZ/giphy.gif',
             'https://media.giphy.com/media/zczRdwNV7g2s3uxVfJ/giphy.gif',
             'https://media.giphy.com/media/OE98XY0o0VwpaMQFqg/giphy.gif',
             'https://media.giphy.com/media/PIMCexKGD4gIB4ORZL/giphy.gif',
             'https://media.giphy.com/media/pefBhma2UqwPVOg1Hs/giphy.gif',
             'https://media.giphy.com/media/WJwkaHaEb7ml4jRAgT/giphy.gif',
             'https://media.giphy.com/media/wOly8pa4s4W88/giphy.gif',
             'https://media.giphy.com/media/cb4Pg4jau2SEE/giphy.gif',
             'https://media.giphy.com/media/u2LJ0n4lx6jF6/giphy.gif',
             'https://media.giphy.com/media/tZ7UQF5qKaFiJrRmX3/giphy.gif',
						 'https://media.giphy.com/media/RHRSIak4wow3v4Rwcj/giphy.gif']
    
    kick = discord.Embed(description=f"¡{member.mention} recibió una patada de {ctx.message.author.mention}!", color=0xff69b4)
    kick.set_image(url=random.choice(kicks))
    await ctx.send(embed=kick)

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
async def sobremi(ctx):
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
async def soporte(ctx):
    """
    Muestra el enlace al servidor de soporte del bot
    """
    embed = discord.Embed(title="Servidor de Soporte", description="¡Únete al servidor de soporte para obtener ayuda con el bot!", color=0x7289DA)
    embed.add_field(name="Enlace", value="https://discord.gg/PvJNZQUQGf", inline=False)
    embed.set_footer(text="¡Únete ahora para recibir ayuda y estar al tanto de las actualizaciones!")
    await ctx.send(embed=embed)

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
    response = requests.get("https://api.waifu.pics/sfw/waifu")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes una linda chica anime!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def awoo(ctx):
    response = requests.get("https://api.waifu.pics/sfw/awoo")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes un awoo!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def neko(ctx):
    response = requests.get("https://api.waifu.pics/sfw/neko")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes una linda neko!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def animegirlnsfw(ctx):
    if not ctx.channel.nsfw:
        await ctx.send("Lo siento, este comando solo puede ser usado en canales con restricción de edad.")
        return

    response = requests.get("https://api.waifu.pics/nsfw/waifu")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes una linda chica anime!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def nekonsfw(ctx):
    if not ctx.channel.is_nsfw():
        await ctx.send("Este comando solo se puede usar en canales con restricción de edad.")
        return

    response = requests.get("https://api.waifu.pics/nsfw/neko")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes una linda neko!", color=discord.Color.blue())
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
async def calcular(ctx, *, expresion):
    try:
        # Evalúa la expresión matemática ingresada por el usuario
        resultado = eval(expresion)
        
        # Formatea el resultado con dos decimales si es un número de punto flotante
        if isinstance(resultado, float):
            resultado = round(resultado, 2)
        
        # Envía el resultado de vuelta al usuario
        await ctx.send(f"El resultado es: {resultado}")
    except Exception as e:
        # Si hay un error, devuelve un mensaje de error al usuario
        await ctx.send(f"Ocurrió un error: {e}")
	
@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(title="Comandos del bot", description="Aquí están todos los comandos disponibles en el bot:", color=discord.Color.blue())

    # División de comandos administrativos
    admin_cmds = ""
    admin_cmds += "**m/kick [usuario] [razón]**: Expulsa a un usuario del servidor\n"
    admin_cmds += "**m/ban [usuario] [razón]**: Banea a un usuario del servidor\n"
    admin_cmds += "**m/unmute [usuario]**: Quita el mute de un usuario\n"
    admin_cmds += "**m/unban [usuario]**: Quita el baneo de un usuario\n"
    admin_cmds += "**m/unkick [usuario]**: Quita el kick de un usuario\n"
    admin_cmds += "**m/purge [cantidad]**: Elimina la cantidad especificada de mensajes (solo moderadores)\n"
    embed.add_field(name="Comandos Administrativos", value=admin_cmds, inline=False)

    # División de comandos de diversión
    fun_cmds = ""
    fun_cmds += "**m/hello**: Saluda al usuario que ejecutó el comando\n"
    fun_cmds += "**m/say [mensaje]**: Envía un mensaje como el bot\n"
    fun_cmds += "**m/8ball [pregunta]**: Responde una pregunta de sí o no\n"
    fun_cmds += "**m/kiss [usuario]**: Besa a un usuario\n"
    fun_cmds += "**m/rps [piedra/papel/tijera]**: Juega piedra, papel o tijera con el bot\n"
    fun_cmds += "**m/ship [usuario1] [usuario2]**: Hace un shipeo entre dos usuarios\n"
    fun_cmds += "**m/cry**: Envía un gif de llanto en un embed\n"
    fun_cmds += "**m/pat [usuario]**: Envía un gif de caricia en un embed\n"
    fun_cmds += "**m/hi [usuario]**: Saluda a otro usuario.\n"
    fun_cmds += "**m/slap [usuario]**: Abofetea a un usuario\n"
    fun_cmds += "**m/hug [usuario]**: Abraza a un usuario\n"
    fun_cmds += "**m/kill [usuario]**: Mata a un usuario\n"
    fun_cmds += "**m/knockout [usuario]**: Noquea a un usuario\n"
    fun_cmds += "**m/punch [usuario]**: Golpea a un usuario\n"
    fun_cmds += "**m/patear [usuario]**: Patea a un usuario\n"
    embed.add_field(name="Comandos de Diversión", value=fun_cmds, inline=False)

    # División de comandos de anime
    ani_cmds = ""
    ani_cmds += "**m/animegirl**: Envía una imagen de una chica de anime\n"
    ani_cmds += "**m/neko**: Envía una imagen de una neko\n"
    ani_cmds += "**m/awoo [pregunta]**: Envía un awoo\n"
    embed.add_field(name="Comandos de Anime", value=ani_cmds, inline=False)

    # División de comandos de anime nsfw
    nsfw_cmds = ""
    nsfw_cmds += "**m/animegirlnsfw**: Envía una imagen de una chica de anime en NSFW\n"
    nsfw_cmds += "**m/nekonsfw**: Envía una imagen de una neko en NSFW\n"
    embed.add_field(name="Comandos de Anime NSFW", value=nsfw_cmds, inline=False)
	
    # División de comandos de utilidad
    util_cmds = ""
    util_cmds += "**m/ping**: Muestra la latencia del bot\n"
    util_cmds += "**m/userinfo [usuario]**: Muestra información sobre un usuario\n"
    util_cmds += "**m/afk [razón]**: Establece un estado de ausencia y muestra una respuesta personalizada cuando te mencionen\n"
    util_cmds += "**m/unafk**: Quita el estado de ausencia\n"
    util_cmds += "**m/qr [texto]**: Genera un código QR a partir de un texto\n"
    util_cmds += "**m/morse [texto]**: Devuelve el código morse de un texto escrito\n"
    util_cmds += "**m/serverinfo**: Muestra información del servidor\n"
    util_cmds += "**m/calcular [expresión matemática]**: Calcula el resultado de una expresión matemática\n"
    embed.add_field(name="Comandos de Utilidad", value=util_cmds, inline=False)

    # Comandos Misceláneos
    misc_cmds = ""
    misc_cmds += "**m/sobremi**: Muestra información sobre el bot\n"
    misc_cmds += "**m/invite**: Genera un enlace para invitar al bot a tu servidor\n"
    misc_cmds += "**m/creador**: Muestra información sobre el creador y el bot\n"
    misc_cmds += "**m/soporte**: Obten el enlace al servidor de soporte del bot\n"
    embed.add_field(name="Comandos Misceláneos", value=misc_cmds, inline=False)

    # Comando de ayuda
    help_cmds = ""
    help_cmds += "**m/ayuda**: Muestra este mensaje de ayuda\n"
    embed.add_field(name="Comandos de Ayuda", value=help_cmds, inline=False)

# Nota del creador
    creator_note = "Este bot envía los comandos NSFW en canales que no son de este tipo. Favor de utilizar estos comandos donde es debido. Si una persona está usando dichos comandos en canales no destinados al NSFW, haz un reporte en el servidor de soporte, el cual, lo encuentras usando el comando m/soporte. Una vez hecho el reporte con las debidas pruebas el usuario será agregado a la Lista Negra del bot y no podrá interactuar con el. No hay garantía de que esto siempre funcione, por lo que se debe tener precaución al usar comandos NSFW. Además, el creador del bot no se hace responsable del mal uso de este bot."
    embed.add_field(name="Nota del Creador", value=creator_note, inline=False)

 # Pie de página
    embed.set_footer(text="Algunos comandos estan en desarrollo y algunos errores pueden presentarse. !Gracias por seguir usando el servicio en desarrollo de Hikari¡")
	
    await ctx.send(embed=embed)
	
keep_alive()
bot.run("")