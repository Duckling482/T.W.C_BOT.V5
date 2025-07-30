import os
import asyncio
import json
from dotenv import load_dotenv
import random
import discord
from discord.ext import commands
from keep_alive import keep_alive
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

# Charger les variables d’environnement
load_dotenv()
token = os.getenv('DISCORD_TOKEN')



CHANNEL_ID = 1216781760155881613  # ID du salon

@bot.command()
async def bonjour(ctx):
    await ctx.send(f"Bonjour {ctx.author.mention} !")

CHANNEL_ID = 1216781760155881613  # ID du salon

# Configuration complète des intents
# Configuration des intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

# Création unique du bot
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1216781760155881613  # Remplace par l'ID de ton salon
# Salon cible pour les mises à jour d’effectif
CHANNEL_ID = 1216781760155881613

# Départements (mentionnables)
# Configuration des rôles
ROLES = {
    "🔰• Wilford Security Solutions": 1298636409166626826,
    "💵• Département des Ventes et du Développement Commercial": 1298352921871782003,
    "👥• Ressources Humaines": 1216515880922386452,
    "🛠️• Recherche et Développement •🛠️": 1216515780724658368
}

# Hiérarchie
# Rôles hiérarchiques
DIRECTION = 1151179209675378698
ADJOINT_DEPUTE = 1371558060069359617
ADJOINT_DIRECTION = 1371558356145143899
@@ -52,108 +44,97 @@ async def bonjour(ctx):
EMPLOYE_JUNIOR = 1352013992347828296
APPRENTI = 1352013998572306462
STAGIAIRE = 1352013993539014726
ABSENT_ROLE_ID = 1371559532378980352  # ID du rôle "Absent"
ABSENT_ROLE_ID = 1371559532378980352

# =====================================================================
# EVENEMENT DE DEMARRAGE
# =====================================================================
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    bot.loop.create_task(update_effectif())

# =====================================================================
# COMMANDE SIMPLE EXEMPLE
# =====================================================================
@bot.command()
async def bonjour(ctx):
    await ctx.send(f"Bonjour {ctx.author.mention} !")

# =====================================================================
# FONCTION DE MISE À JOUR DES EFFECTIFS
# =====================================================================
async def update_effectif():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Salon introuvable.")
        return

    def get_departement(member):
        for _, role_id in ROLES.items():
            role = channel.guild.get_role(role_id)
            if role and role in member.roles:
                return role
        return None

    async def generer_bloc(guild, role_id, avec_departement=True):
        bloc = f"### <@&{role_id}>\n"
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
            if guild.get_role(ABSENT_ROLE_ID) in member.roles:
                ligne += f" <@&{ABSENT_ROLE_ID}>"
            bloc += ligne + "\n"
            total += 1

        if total == 0:
            bloc += "N/A\n"

        bloc += "━" * 75 + "\n"
        return bloc

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
        
                    # Ajouter le rôle "Absent" s'il est présent
                    absent_role = guild.get_role(ABSENT_ROLE_ID)
                    if absent_role and absent_role in member.roles:
                        ligne += f" <@&{ABSENT_ROLE_ID}>"
        
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
            for role_id in [EMPLOYE_SENIOR, EMPLOYE_CONFIRME, EMPLOYE, EMPLOYE_JUNIOR]:
                message += await generer_bloc(guild, role_id)

            # Apprenti (pas de département)
            message += await generer_bloc(guild, APPRENTI, avec_departement=False)

            # Stagiaire (pas de département)
            message += await generer_bloc(guild, STAGIAIRE, avec_departement=False)

       
            personnel_role = channel.guild.get_role(1158798630254280855)
            personnel_count = len(personnel_role.members) if personnel_role else 0
            message += f"** Total de <@&{personnel_role.id}> : {personnel_count}**\n"
    
           # Vérifier si un message existe déjà dans le salon
            
            count = len(personnel_role.members) if personnel_role else 0
            message += f"** Total de <@&{personnel_role.id}> : {count}**\n"

            async for msg in channel.history(limit=1):
                if msg.author == bot.user:  # Vérifier si c'est un message du bot
                    await msg.edit(content=message)  # Mettre à jour le message
                    print("Message mis à jour.")
                if msg.author == bot.user:
                    await msg.edit(content=message)
                    break
            else:
                # Si aucun message du bot n'existe, en créer un nouveau
                await channel.send(message)
                print("Nouveau message envoyé.")

        except Exception as e:
            print(f"Erreur lors de la mise à jour du message : {str(e)}")
            print(f"Erreur de mise à jour : {e}")

        # Attendre 60 secondes avant la prochaine mise à jour
        await asyncio.sleep(60)
# ----------------------------------------------------------- CASINO -------------------------------------------------------------

bot = commands.Bot(command_prefix="!")
# =====================================================================
# CASINO : BLACKJACK, SOLDE, BONUS, ETC.
# =====================================================================

# DB
DB_PATH = "jetons.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
@@ -163,6 +144,7 @@ async def generer_bloc(guild, role_id, avec_departement=True):
blackjack_parties = {}
mises = {}

# Fonctions de gestion de jetons
def get_solde(user_id):
    c.execute("SELECT solde FROM jetons WHERE user_id = ?", (user_id,))
    row = c.fetchone()
@@ -190,45 +172,33 @@ def set_last_bonus(user_id):
    c.execute("UPDATE jetons SET last_bonus = ? WHERE user_id = ?", (datetime.utcnow().isoformat(), user_id))
    conn.commit()

# Blackjack utils
card_emojis = {
    2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣",
    8: "8️⃣", 9: "9️⃣", 10: "🔟", 11: "🂡"
}

def tirer_carte():
    return random.choice(list(card_emojis.keys()))

def tirer_carte(): return random.choice(list(card_emojis.keys()))
def calculer_total(cartes):
    total = sum(cartes)
    as_count = cartes.count(11)
    while total > 21 and as_count:
        total -= 10
        as_count -= 1
    return total
def afficher_cartes(cartes): return " ".join(card_emojis[carte] for carte in cartes)

def afficher_cartes(cartes):
    return " ".join(card_emojis[carte] for carte in cartes)

# Blackjack Commands
@bot.command()
async def miser(ctx, montant: int):
    joueur_id = ctx.author.id
    solde = get_solde(joueur_id)
    if montant <= 0 or montant > solde:
        await ctx.send("❌ Mise invalide ou solde insuffisant.")
        return

        return await ctx.send("❌ Mise invalide ou solde insuffisant.")
    carte1, carte2 = tirer_carte(), tirer_carte()
    joueur = [carte1, carte2]
    croupier = [tirer_carte(), tirer_carte()]

    blackjack_parties[joueur_id] = {
        "joueur": joueur,
        "croupier": croupier,
        "fini": False
    }
    joueur, croupier = [carte1, carte2], [tirer_carte(), tirer_carte()]
    blackjack_parties[joueur_id] = {"joueur": joueur, "croupier": croupier, "fini": False}
    mises[joueur_id] = montant
    update_solde(joueur_id, -montant)

    await ctx.send(f"🃏 Tes cartes : {afficher_cartes(joueur)} (Total : **{calculer_total(joueur)}**)")
    await ctx.send(f"🤵 Croupier montre : {card_emojis[croupier[0]]} ❓")
    await ctx.send("Tape `!hit` pour piocher ou `!stand` pour rester.")
@@ -238,14 +208,11 @@ async def hit(ctx):
    joueur_id = ctx.author.id
    partie = blackjack_parties.get(joueur_id)
    if not partie or partie["fini"]:
        await ctx.send("❌ Pas de partie en cours.")
        return

        return await ctx.send("❌ Pas de partie en cours.")
    carte = tirer_carte()
    partie["joueur"].append(carte)
    total = calculer_total(partie["joueur"])
    await ctx.send(f"🃏 Tu as tiré : {card_emojis[carte]} → {afficher_cartes(partie['joueur'])} (Total : **{total}**)")

    if total > 21:
        partie["fini"] = True
        await ctx.send("💥 Tu dépasses 21, tu perds ta mise.")
@@ -259,21 +226,17 @@ async def stand(ctx):
    joueur_id = ctx.author.id
    partie = blackjack_parties.get(joueur_id)
    if not partie or partie["fini"]:
        await ctx.send("❌ Pas de partie en cours.")
        return

        return await ctx.send("❌ Pas de partie en cours.")
    partie["fini"] = True
    joueur_total = calculer_total(partie["joueur"])
    croupier = partie["croupier"]
    croupier_total = calculer_total(croupier)

    await ctx.send(f"🤵 Le croupier avait : {afficher_cartes(croupier)} (Total : **{croupier_total}**)")
    while croupier_total < 17:
        carte = tirer_carte()
        croupier.append(carte)
        croupier_total = calculer_total(croupier)
        await ctx.send(f"🤵 Il tire : {card_emojis[carte]} → {afficher_cartes(croupier)} (Total : **{croupier_total}**)")

    mise = mises.pop(joueur_id, 0)
    if croupier_total > 21 or joueur_total > croupier_total:
        gain = mise * 2
@@ -287,131 +250,55 @@ async def stand(ctx):

@bot.command()
async def solde(ctx):
    solde = get_solde(ctx.author.id)
    await ctx.send(f"💰 Tu as {solde} jetons.")
    await ctx.send(f"💰 Tu as {get_solde(ctx.author.id)} jetons.")

@bot.command()
async def topjetons(ctx):
    c.execute("SELECT user_id, solde FROM jetons ORDER BY solde DESC LIMIT 5")
    rows = c.fetchall()
    message = "🏆 Classement des riches :\n"
    for i, (user_id, solde) in enumerate(rows, start=1):
        user = await bot.fetch_user(user_id)
        message += f"{i}. {user.name} : {solde} jetons\n"
    await ctx.send(message)
    msg = "🏆 Classement des riches :\n"
    for i, (uid, solde) in enumerate(rows, start=1):
        user = await bot.fetch_user(uid)
        msg += f"{i}. {user.name} : {solde} jetons\n"
    await ctx.send(msg)

@bot.command()
async def bonus(ctx):
    user_id = ctx.author.id
    dernier = get_last_bonus(user_id)
    maintenant = datetime.utcnow()

    if not dernier or maintenant - dernier > timedelta(hours=24):
        set_last_bonus(user_id)
        update_solde(user_id, 200)
    uid = ctx.author.id
    dernier = get_last_bonus(uid)
    now = datetime.utcnow()
    if not dernier or now - dernier > timedelta(hours=24):
        set_last_bonus(uid)
        update_solde(uid, 200)
        await ctx.send("🎁 Bonus quotidien : +200 jetons !")
    else:
        restant = timedelta(hours=24) - (maintenant - dernier)
        await ctx.send(f"🕒 Reviens dans {restant.seconds // 3600}h{(restant.seconds // 60) % 60}m pour un nouveau bonus.")
        restant = timedelta(hours=24) - (now - dernier)
        h, m = divmod(restant.seconds // 60, 60)
        await ctx.send(f"🕒 Reviens dans {h}h{m}m pour un nouveau bonus.")

@bot.command()
async def donner(ctx, membre: discord.Member, montant: int):
    auteur_id = ctx.author.id
    if get_solde(auteur_id) < montant or montant <= 0:
        await ctx.send("❌ Solde insuffisant ou montant invalide.")
        return
    update_solde(auteur_id, -montant)
    if montant <= 0 or get_solde(ctx.author.id) < montant:
        return await ctx.send("❌ Solde insuffisant ou montant invalide.")
    update_solde(ctx.author.id, -montant)
    update_solde(membre.id, montant)
    await ctx.send(f"💸 Tu as donné {montant} jetons à {membre.display_name}.")

@bot.command()
async def retirer(ctx, montant: int):
    auteur_id = ctx.author.id
    if get_solde(auteur_id) < montant or montant <= 0:
        await ctx.send("❌ Solde insuffisant ou montant invalide.")
        return
    update_solde(auteur_id, -montant)
    if montant <= 0 or get_solde(ctx.author.id) < montant:
        return await ctx.send("❌ Solde insuffisant ou montant invalide.")
    update_solde(ctx.author.id, -montant)
    await ctx.send(f"🪙 Tu as retiré {montant} jetons de ton compte.")

# =====================================================================
# AUTRES COMMANDES FUN
# =====================================================================

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
# (Les commandes "earl", "hawk", "vlad", etc. restent identiques ici, je peux aussi te les reformatter si tu veux)

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

@bot.command()
async def patrice(ctx):
    await ctx.send("Mangeur d'orteils à temps partiel, buveur de pinard professionnel à plein temps.")





token = os.getenv('DISCORD_TOKEN')
# =====================================================================
# LANCEMENT DU BOT
# =====================================================================
keep_alive()
bot.run(token)
