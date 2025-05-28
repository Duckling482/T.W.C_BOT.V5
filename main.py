import os
import asyncio
from dotenv import load_dotenv
import random
import discord
from discord.ext import commands
from keep_alive import keep_alive

from keep_alive import keep_alive

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1216781760155881613  # ID du salon

@bot.command()
async def bonjour(ctx):
    await ctx.send(f"Bonjour {ctx.author.mention} !")

CHANNEL_ID = 1216781760155881613  # ID du salon

# Configuration complète des intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1216781760155881613  # Remplace par l'ID de ton salon

# Départements (mentionnables)
ROLES = {
    "🔰• Wilford Security Solutions": 1298636409166626826,
    "💵• Département des Ventes et du Développement Commercial": 1298352921871782003,
    "👥• Ressources Humaines": 1216515880922386452,
    "🛠️• Recherche et Développement •🛠️": 1216515780724658368
}

# Hiérarchie
DIRECTION = 1151179209675378698
ADJOINT_DEPUTE = 1371558060069359617
ADJOINT_DIRECTION = 1371558356145143899
EMPLOYE_SENIOR = 1352013470916415558
EMPLOYE_CONFIRME = 1352013465459359754
EMPLOYE = 1352013990649266176
EMPLOYE_JUNIOR = 1352013992347828296
APPRENTI = 1352013998572306462
STAGIAIRE = 1352013993539014726

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    bot.loop.create_task(update_effectif())

async def update_effectif():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Salon introuvable.")
        return

    while True:
        try:
            guild = channel.guild
            message = ""

            def get_departement(member):
                for _, role_id in ROLES.items():
                    role = guild.get_role(role_id)
                    if role and role in member.roles:
                        return role
                return None

            async def generer_bloc(guild, role_id, avec_departement=True):
                    bloc = f"### <@&{role_id}>\n"  # Grand titre avec la mention du rôle
                    role = guild.get_role(role_id)
                    if not role:
                        return f"Rôle introuvable : {role_id}\n"
                    total = 0
                    for member in role.members:
                        ligne = f"- {member.mention}"
                        if avec_departement:
                            departement = get_departement(member)
                            if departement:
                                ligne += f" <@&{departement.id}>"
                        bloc += ligne + "\n"
                        total += 1
                    if total == 0:
                        bloc += "N/A\n"
                    bloc += "━" * 75 + "\n"
                    return bloc


            # Bloc Direction
            message += await generer_bloc(guild, DIRECTION)
            # Bloc Adjoint du Député
            message += await generer_bloc(guild, ADJOINT_DEPUTE)
            # Bloc Adjoint de direction
    
            message += await generer_bloc(guild, ADJOINT_DIRECTION)
            # Employés
            employes = [EMPLOYE_SENIOR, EMPLOYE_CONFIRME, EMPLOYE, EMPLOYE_JUNIOR]
            for role_id in employes:
                message += await generer_bloc(guild, role_id)

            # Apprenti (pas de département)
            message += await generer_bloc(guild, APPRENTI, avec_departement=False)

            # Stagiaire (pas de département)
            message += await generer_bloc(guild, STAGIAIRE, avec_departement=False)

       
            personnel_role = channel.guild.get_role(1158798630254280855)
            personnel_count = len(personnel_role.members) if personnel_role else 0
            message += f"** Total de <@&{personnel_role.id}> : {personnel_count}**\n"
         # Commandes supplémentaires pour tester



           # Vérifier si un message existe déjà dans le salon
            async for msg in channel.history(limit=1):
                if msg.author == bot.user:  # Vérifier si c'est un message du bot
                    await msg.edit(content=message)  # Mettre à jour le message
                    print("Message mis à jour.")
                    break
            else:
                # Si aucun message du bot n'existe, en créer un nouveau
                await channel.send(message)
                print("Nouveau message envoyé.")

        except Exception as e:
            print(f"Erreur lors de la mise à jour du message : {str(e)}")

        # Attendre 60 secondes avant la prochaine mise à jour
        await asyncio.sleep(60)

# Commandes supplémentaires pour tester

@bot.command()
async def ping(ctx):
    await ctx.send("Ne vous inquiétez-vous donc pas cher maître, je suis là.")

@bot.command()
async def earl(ctx):
    await ctx.send("C'est un spécimen unique en son genre, maigre, boutonneux et binoclard. Il ne ferait même pas mal à une mouche.")

@bot.command()
async def hawk(ctx):
    await ctx.send("Ce type vit dans le passé, il se prend pour un cowboy alors que c'est un femboy.")

@bot.command()
async def edouard(ctx):
    await ctx.send("C'est l'homme le plus gros que j'ai connu. Un virage, un accident. Il a beau être gros même le Dodge Ram le subit ! ")

@bot.command()
async def gunter(ctx):
    await ctx.send("Il aime que les trombonnes soient à leur place. Recalé par l'école d'art, il commence sa carrière politique. «Nein! Nein! Nein!git status» a-t-il dit.")

@bot.command()
async def joe(ctx):
    await ctx.send("Souvent confondu avec un camionneur, ce commissaire de police est redouté pour les BL qui partent vite.")

@bot.command()
async def micheal(ctx):
    await ctx.send("Amateur professionnel de jeunes asiatiques, il les dévore comme du popcorn. Pop!")

@bot.command()
async def angus(ctx):
    await ctx.send("Cet homme est un multi-aliment, il a le nom d'une race bovine écossaise, et peut-être aussi un jus de fruit. Bon appétit!")

@bot.command()
async def vlad(ctx):
    await ctx.send("Cet homme, féru de frites, aime bien dénigrer la France, parce que pourquoi pas, et si tu oses le contredire, il te sortira un (olala).")

@bot.command()
async def thomas(ctx):
    await ctx.send("Lui c'est juste une salope qui se fait ban H24, mais il détruit tout le monde sur les points, donc en vrai pas grave, on l'excuse.") 

@bot.command()
async def tony(ctx):
    await ctx.send("Attention! Si votre véhicule est coincé ne l'appelé pas, il va vite perdre patience et tout faire péter!") 

message_dodgeram = [
    "Pas de bol ! Tu as fait un carkill massif et Gustavo était dans les parages...",
        "Tu as fait voler une voiture et Tyler a tout vu...",
        "Tu roulais à 244km/h et par chance tu n'as tué personne !"
]

@bot.command()
async def dodgeram(ctx):
    await ctx.send(random.choice(message_dodgeram))

@bot.command()
async def roll(ctx):
    await ctx.send(random.randint(1, 10))

@bot.command()
async def ntm(ctx):
     await ctx.send(f"C'est une injure très vulgaire et malpolie. Je ne peux pas vous laisser sans punition {ctx.author.mention}.")

@bot.command()
async def pileouface(ctx):
    await ctx.send(random.choice(["Pile", "Face"]))

@bot.command()
async def alex(ctx):
    await ctx.send("Vous recherchez un aspirateur ? Parfait ! Le Alex Dupont ProMax aspire tout, même les liquides ! N'hésitez plus, commandez dès maintenant !")





token = os.getenv('DISCORD_TOKEN')
keep_alive()
bot.run(token)
