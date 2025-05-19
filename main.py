import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
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



            # Envoi ou mise à jour
            async for msg in channel.history(limit=1):
                if msg.author == bot.user:
                    await msg.edit(content=message)
                    break
            else:
                await channel.send(message)

        except Exception as e:
            print(f"Erreur : {e}")

        await asyncio.sleep(60)  # toutes les secondes

token = os.getenv("DISCORD_TOKEN")
keep_alive()
bot.run(token)


