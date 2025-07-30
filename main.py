import os
import asyncio
import json
import random
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

# Configuration des intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

# Création unique du bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Salon cible pour les mises à jour d’effectif
CHANNEL_ID = 1216781760155881613

# Configuration des rôles
ROLES = {
    "🔰• Wilford Security Solutions": 1298636409166626826,
    "💵• Département des Ventes et du Développement Commercial": 1298352921871782003,
    "👥• Ressources Humaines": 1216515880922386452,
    "🛠️• Recherche et Développement •🛠️": 1216515780724658368
}

# Rôles hiérarchiques
DIRECTION = 1151179209675378698
ADJOINT_DEPUTE = 1371558060069359617
ADJOINT_DIRECTION = 1371558356145143899
EMPLOYE_SENIOR = 1352013470916415558
EMPLOYE_CONFIRME = 1352013465459359754
EMPLOYE = 1352013990649266176
EMPLOYE_JUNIOR = 1352013992347828296
APPRENTI = 1352013998572306462
STAGIAIRE = 1352013993539014726
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

# =====================================================================
# CASINO : BLACKJACK, SOLDE, BONUS, ETC.
# =====================================================================

# DB
DB_PATH = "jetons.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS jetons (user_id INTEGER PRIMARY KEY, solde INTEGER DEFAULT 1000, last_bonus TEXT)''')
conn.commit()

blackjack_parties = {}
mises = {}

# Fonctions de gestion de jetons
def get_solde(user_id):
    c.execute("SELECT solde FROM jetons WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if row:
        return row[0]
    else:
        c.execute("INSERT INTO jetons (user_id, solde, last_bonus) VALUES (?, ?, ?)", (user_id, 1000, datetime.utcnow().isoformat()))
        conn.commit()
        return 1000

def update_solde(user_id, montant):
    solde = get_solde(user_id) + montant
    solde = max(0, solde)
    c.execute("UPDATE jetons SET solde = ? WHERE user_id = ?", (solde, user_id))
    conn.commit()

def get_last_bonus(user_id):
    c.execute("SELECT last_bonus FROM jetons WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if row and row[0]:
        return datetime.fromisoformat(row[0])
    return None

def set_last_bonus(user_id):
    c.execute("UPDATE jetons SET last_bonus = ? WHERE user_id = ?", (datetime.utcnow().isoformat(), user_id))
    conn.commit()

# Blackjack utils
card_emojis = {
    2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣",
    8: "8️⃣", 9: "9️⃣", 10: "🔟", 11: "🂡"
}
def tirer_carte(): return random.choice(list(card_emojis.keys()))
def calculer_total(cartes):
    total = sum(cartes)
    as_count = cartes.count(11)
    while total > 21 and as_count:
        total -= 10
        as_count -= 1
    return total
def afficher_cartes(cartes): return " ".join(card_emojis[carte] for carte in cartes)

# Blackjack Commands
@bot.command()
async def miser(ctx, montant: int):
    joueur_id = ctx.author.id
    solde = get_solde(joueur_id)
    if montant <= 0 or montant > solde:
        return await ctx.send("❌ Mise invalide ou solde insuffisant.")
    carte1, carte2 = tirer_carte(), tirer_carte()
    joueur, croupier = [carte1, carte2], [tirer_carte(), tirer_carte()]
    blackjack_parties[joueur_id] = {"joueur": joueur, "croupier": croupier, "fini": False}
    mises[joueur_id] = montant
    update_solde(joueur_id, -montant)
    await ctx.send(f"🃏 Tes cartes : {afficher_cartes(joueur)} (Total : **{calculer_total(joueur)}**)")
    await ctx.send(f"🤵 Croupier montre : {card_emojis[croupier[0]]} ❓")
    await ctx.send("Tape `!hit` pour piocher ou `!stand` pour rester.")

@bot.command()
async def hit(ctx):
    joueur_id = ctx.author.id
    partie = blackjack_parties.get(joueur_id)
    if not partie or partie["fini"]:
        return await ctx.send("❌ Pas de partie en cours.")
    carte = tirer_carte()
    partie["joueur"].append(carte)
    total = calculer_total(partie["joueur"])
    await ctx.send(f"🃏 Tu as tiré : {card_emojis[carte]} → {afficher_cartes(partie['joueur'])} (Total : **{total}**)")
    if total > 21:
        partie["fini"] = True
        await ctx.send("💥 Tu dépasses 21, tu perds ta mise.")
    elif total == 21:
        await ctx.send("🎯 Tu as 21 ! Tape `!stand`.")
    else:
        await ctx.send("Tape `!hit` ou `!stand`.")

@bot.command()
async def stand(ctx):
    joueur_id = ctx.author.id
    partie = blackjack_parties.get(joueur_id)
    if not partie or partie["fini"]:
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
        update_solde(joueur_id, gain)
        await ctx.send(f"🎉 Tu gagnes {gain} jetons !")
    elif joueur_total == croupier_total:
        update_solde(joueur_id, mise)
        await ctx.send("🤝 Égalité, tu récupères ta mise.")
    else:
        await ctx.send("💀 Le croupier gagne. Tu perds ta mise.")

@bot.command()
async def solde(ctx):
    await ctx.send(f"💰 Tu as {get_solde(ctx.author.id)} jetons.")

@bot.command()
async def topjetons(ctx):
    c.execute("SELECT user_id, solde FROM jetons ORDER BY solde DESC LIMIT 5")
    rows = c.fetchall()
    msg = "🏆 Classement des riches :\n"
    for i, (uid, solde) in enumerate(rows, start=1):
        user = await bot.fetch_user(uid)
        msg += f"{i}. {user.name} : {solde} jetons\n"
    await ctx.send(msg)

@bot.command()
async def bonus(ctx):
    uid = ctx.author.id
    dernier = get_last_bonus(uid)
    now = datetime.utcnow()
    if not dernier or now - dernier > timedelta(hours=24):
        set_last_bonus(uid)
        update_solde(uid, 200)
        await ctx.send("🎁 Bonus quotidien : +200 jetons !")
    else:
        restant = timedelta(hours=24) - (now - dernier)
        h, m = divmod(restant.seconds // 60, 60)
        await ctx.send(f"🕒 Reviens dans {h}h{m}m pour un nouveau bonus.")

@bot.command()
async def donner(ctx, membre: discord.Member, montant: int):
    if montant <= 0 or get_solde(ctx.author.id) < montant:
        return await ctx.send("❌ Solde insuffisant ou montant invalide.")
    update_solde(ctx.author.id, -montant)
    update_solde(membre.id, montant)
    await ctx.send(f"💸 Tu as donné {montant} jetons à {membre.display_name}.")

@bot.command()
async def retirer(ctx, montant: int):
    if montant <= 0 or get_solde(ctx.author.id) < montant:
        return await ctx.send("❌ Solde insuffisant ou montant invalide.")
    update_solde(ctx.author.id, -montant)
    await ctx.send(f"🪙 Tu as retiré {montant} jetons de ton compte.")

# =====================================================================
# AUTRES COMMANDES FUN
# =====================================================================

# (Les commandes "earl", "hawk", "vlad", etc. restent identiques ici, je peux aussi te les reformatter si tu veux)

# =====================================================================
# LANCEMENT DU BOT
# =====================================================================
keep_alive()
bot.run(token)
