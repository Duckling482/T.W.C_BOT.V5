import os
import asyncio
import json
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
ABSENT_ROLE_ID = 1371559532378980352  # ID du rôle "Absent"

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
                message += await generer_bloc(guild, role_id)

            # Apprenti (pas de département)
            message += await generer_bloc(guild, APPRENTI, avec_departement=False)

            # Stagiaire (pas de département)
            message += await generer_bloc(guild, STAGIAIRE, avec_departement=False)

       
            personnel_role = channel.guild.get_role(1158798630254280855)
            personnel_count = len(personnel_role.members) if personnel_role else 0
            message += f"** Total de <@&{personnel_role.id}> : {personnel_count}**\n"
    
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
# ----------------------------------------------------------- CASINO -------------------------------------------------------------

# ----- Chemin vers le fichier de sauvegarde -----
FICHIER_JETONS = "jetons.json"

# ----- Chargement ou création du fichier de jetons -----
if os.path.exists(FICHIER_JETONS):
    with open(FICHIER_JETONS, "r") as f:
        jetons = json.load(f)
else:
    jetons = {}

# ----- Sauvegarde des jetons -----
def sauvegarder_jetons():
    with open(FICHIER_JETONS, "w") as f:
        json.dump(jetons, f)

# ----- Cartes en emojis -----
EMOJIS_CARTES = {
    2: "2", 3: "3", 4: "4", 5: "5", 6: "6",
    7: "7", 8: "8", 9: "9", 10: "🔟", 11: "🂡"
}

# ----- Parties de blackjack -----
blackjack_parties = {}

# ----- Initialisation des jetons -----
def get_solde(user_id):
    if str(user_id) not in jetons:
        jetons[str(user_id)] = 1000
        sauvegarder_jetons()
    return jetons[str(user_id)]

# ----- Tirage d'une carte -----
def tirer_carte():
    return random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])

# ----- Calcul du total -----
def calculer_total(cartes):
    total = sum(cartes)
    as_count = cartes.count(11)
    while total > 21 and as_count:
        total -= 10
        as_count -= 1
    return total

# ----- Affichage joli des cartes -----
def afficher_cartes(cartes):
    return " ".join(EMOJIS_CARTES.get(c, str(c)) for c in cartes)

# ----- Commande !solde -----
@bot.command()
async def solde(ctx):
    solde_actuel = get_solde(ctx.author.id)
    await ctx.send(f"💰 Tu as **{solde_actuel}** jetons.")

# ----- Commande !topjetons -----
@bot.command()
async def topjetons(ctx):
    top = sorted(jetons.items(), key=lambda x: x[1], reverse=True)[:5]
    msg = "📊 **Top 5 des riches**\n"
    for i, (user_id, amount) in enumerate(top, 1):
        user = await bot.fetch_user(int(user_id))
        msg += f"{i}. {user.name} — {amount} jetons\n"
    await ctx.send(msg)

# ----- Commande !miser [montant] -----
@bot.command()
async def miser(ctx, montant: int):
    joueur_id = str(ctx.author.id)

    if montant <= 0:
        await ctx.send("❌ Mise invalide.")
        return

    if get_solde(joueur_id) < montant:
        await ctx.send("❌ Tu n'as pas assez de jetons.")
        return

    carte1, carte2 = tirer_carte(), tirer_carte()
    joueur = [carte1, carte2]
    croupier = [tirer_carte(), tirer_carte()]

    blackjack_parties[joueur_id] = {
        "joueur": joueur,
        "croupier": croupier,
        "mise": montant,
        "fini": False
    }

    await ctx.send(f"🃏 Tes cartes : {afficher_cartes(joueur)} (Total : **{calculer_total(joueur)}**)")
    await ctx.send(f"🤵 Croupier montre : {EMOJIS_CARTES[croupier[0]]} ?")
    await ctx.send("Tape `!hit` pour piocher ou `!stand` pour rester.")

# ----- Commande !hit -----
@bot.command()
async def hit(ctx):
    joueur_id = str(ctx.author.id)
    partie = blackjack_parties.get(joueur_id)

    if not partie or partie["fini"]:
        await ctx.send("❌ Aucune partie en cours. Tape `!miser montant`.")
        return

    carte = tirer_carte()
    partie["joueur"].append(carte)
    total = calculer_total(partie["joueur"])

    await ctx.send(f"🃏 Tu tires : {EMOJIS_CARTES.get(carte, carte)} → {afficher_cartes(partie['joueur'])} (Total : **{total}**)")

    if total > 21:
        partie["fini"] = True
        jetons[joueur_id] -= partie["mise"]
        sauvegarder_jetons()
        await ctx.send(f"💥 Tu dépasses 21 ! Tu perds **{partie['mise']}** jetons.")

# ----- Commande !stand -----
@bot.command()
async def stand(ctx):
    joueur_id = str(ctx.author.id)
    partie = blackjack_parties.get(joueur_id)

    if not partie or partie["fini"]:
        await ctx.send("❌ Aucune partie en cours.")
        return

    partie["fini"] = True
    joueur_total = calculer_total(partie["joueur"])
    croupier = partie["croupier"]

    await ctx.send(f"🤵 Le croupier a : {afficher_cartes(croupier)} (Total : **{calculer_total(croupier)}**)")

    while calculer_total(croupier) < 17:
        carte = tirer_carte()
        croupier.append(carte)
        await ctx.send(f"🤵 Le croupier tire : {EMOJIS_CARTES.get(carte, carte)} → {afficher_cartes(croupier)} (Total : **{calculer_total(croupier)}**)")

    croupier_total = calculer_total(croupier)
    mise = partie["mise"]

    if croupier_total > 21 or joueur_total > croupier_total:
        jetons[joueur_id] += mise
        await ctx.send(f"🎉 Tu gagnes **{mise}** jetons ! 💰 Nouveau solde : {jetons[joueur_id]}")
    elif joueur_total == croupier_total:
        await ctx.send("🤝 Égalité. Tu récupères ta mise.")
    else:
        jetons[joueur_id] -= mise
        await ctx.send(f"💀 Tu perds **{mise}** jetons. Nouveau solde : {jetons[joueur_id]}")

    sauvegarder_jetons()


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

@bot.command()
async def patrice(ctx):
    await ctx.send("Mangeur d'orteils à temps partiel, buveur de pinard professionnel à plein temps.")





token = os.getenv('DISCORD_TOKEN')
keep_alive()
bot.run(token)
