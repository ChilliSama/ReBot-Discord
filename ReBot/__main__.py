from multiprocessing.connection import wait
import os
import hikari
import lightbulb

from ReBot.extensions.ssh import pyssh
from ReBot import GUILD_ID, REBOT_CHANNEL_ID, IP_DEB, PORT_DEB

with open("./secrets/token") as f:
    _token = f.read().strip()

bot = lightbulb.BotApp(
    token = _token,
    prefix = "!",
    default_enabled_guilds=GUILD_ID,
)

bot.load_extensions_from("./ReBot/extensions")

@bot.listen(hikari.StartedEvent)
async def on_started(event) -> None:
    channel = await bot.rest.fetch_channel(REBOT_CHANNEL_ID)
    await channel.send("Connected to discord !")

ssh = ''

@bot.command()
@lightbulb.option('password', 'Entrez votre mot de passe', type=str)
@lightbulb.option('username', 'Entrez votre nom d\'utilisateur', type=str)
@lightbulb.command('connect', 'Connecte le bot à votre ssh')
@lightbulb.implements(lightbulb.SlashCommand)
async def connect(ctx):
    global ssh 
    ssh = pyssh(IP_DEB, PORT_DEB, ctx.options.username, ctx.options.password)
    await ctx.respond(ssh.connect())

@bot.command()
@lightbulb.option('command', 'Entrez votre commande', type=str)
@lightbulb.command('ssh', 'Envoie une commande à votre ssh')
@lightbulb.implements(lightbulb.SlashCommand)
async def connect(ctx):
    global ssh 
    await ctx.respond(ssh.send_cmd(ctx.options.command))

@bot.command()
@lightbulb.command('disconnect', 'Déconnecte le bot de votre ssh')
@lightbulb.implements(lightbulb.SlashCommand)
async def connect(ctx):
    global ssh 
    ssh.logout()
    await ctx.respond("Déconnecté")


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

bot.run()