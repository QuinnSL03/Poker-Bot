import discord
from discord.ext import commands
import random
import asyncio
import handeval
import userfunc as uf

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="$",intents=intents)
top = "<:blankbacktop:714565166070759454>"
bot = "<:blankbackbot:714565093798576455>"
channel = client.get_channel("732386342402785418")
leaderboard_channel = client.get_channel("732386342402785410")
active_players = []
betting_time = 1
min_players = 2
game_start_time = 10
message_start = None
game_start = False
game = None

class Player: 

    def __init__(self, player_obj, hand, bal):
        self.bet = 0
        self.bal = bal
        self.hand = hand
        self.player_obj = player_obj

    def __str__(self):
        return self.hand

class Pot:

    def __init__(self, amount, players):
        self.amount = amount
        self.players = players

    def find_winner(self):
        winner = self.players[0]
        win_condition = ""
        if len(self.players) == 1:
            return [winner, "N/A"]
        a = game.reformat_card(self.players[0].hand[0])
        b = game.reformat_card(self.players[0].hand[1])
        max = [a,b] + game.formatted_table 
        player_winner = self.players[0]
        for i in range(len(self.players)):
            a = game.reformat_card(self.players[i].hand[0])
            b = game.reformat_card(self.players[i].hand[1])
            next = [a,b] + game.formatted_table
            
            result = handeval.compare_hands(max,next)
            print(i,a,b)
            if result[0] == "left":
                winner = max  
            else:
                winner = next
                max = next
                player_winner = self.players[i]
            win_condition = result[1]
        return [player_winner, win_condition]
        
class Poker:

    # I didn't read through everything so I'm not sure if I missed something, but you already defined top and bot global variables
    back_card_top = ":blankbacktop:714565166070759454" 
    back_card_bottom = ":blankbackbot:714565093798576455"
    
    #pots = []
    #current_bet = 0
    #round = 1
    #players = []
    #current_player = None
    #table_cards = []
    #done = False
    #bet = False
    #turns_left = []
    #formatted_table = []
    #main_pot = None
    #i = 0
    deck = ["bAc", "bAs", "rAh", "rAd", 
    "b2c", "b2s", "r2h", "r2d", 
    "b3c", "b3s", "r3h", "r3d", 
    "b4c", "b4s", "r4h", "r4d",
    "b5c", "b5s", "r5h", "r5d",
    "b6c", "b6s", "r6h", "r6d",
    "b7c", "b7s", "r7h", "r7d",
    "b8c", "b8s", "r8h", "r8d",
    "b9c", "b9s", "r9h", "r9d",
    "b10c", "b10s", "r10h", "r10d",
    "bJc", "bJs", "rJh", "rJd",
    "bQc", "bQs", "rQh", "rQd",
    "bKc", "bKs", "rKh", "rKd"]
    
    def __init__(self, players, blind, buy_in, channel):
        self.active_deck = self.deck.copy()
        self.players = []
        for player in players:
            self.players.append(Player(player,[], buy_in))
        self.current_player = self.players[0]
        self.channel = channel
        self.main_pot = Pot(0, self.players)
        self.pots = []
        self.players_in = self.players.copy()
        self.current_bet = 0
        self.round = 1
        self.current_player = None
        self.table_cards = []
        self.done = False
        self.bet = False
        self.turns_left = []
        self.formatted_table = []
        self.i = 0
        
    def find_card_emoji(self, card):
        a = card[:2]
        b = card[2:]
        if card[2:3] == "0":
            a = card[:3]
            b = card[3:]
        print(card[:2], card[2:])
        suit = ""
        if b == "c":
            suit = "eclubs"
        elif b == "s":
            suit = "espades"
        elif b == "h":
            suit = "ehearts"
        else:
            suit = "ediamonds"
        return [str(discord.utils.get(client.emojis, name=a)), str(discord.utils.get(client.emojis, name=suit))]
         
    def deal(self): 
        card = str(random.choice(self.active_deck))
        self.active_deck.remove(card)
        print(card)
        return card

    def call(self):
        self.current_player.bal -= self.current_bet
        self.current_player.bet == self.current_bet
        self.done = True
        self.turns_left.remove(self.current_player)
        return

    def raise_call(self, amount):
        self.current_bet += amount
        self.current_player.bal -= self.current_bet
        self.current_player.bet = self.current_bet
        self.turns_left = self.players_in.copy()
        
        self.i = self.turns_left.index(self.current_player)
        self.turns_left.remove(self.current_player)
        if self.i == len(self.turns_left) and len(self.turns_left) > 0:
            self.i = 0
        self.done = True
        return
    
    def check(self):
        self.done = True
        self.turns_left.remove(self.current_player)
        return

    def fold(self):
        print(type(self.players_in))
        self.players_in.remove(self.current_player)
        self.done = True
        self.turns_left.remove(self.current_player)
        return

    def deal_players(self):
        for player in self.players:
            print("dealt")
            player.hand = [self.deal(), self.deal()]
        self.players_in = self.players.copy()
        
    def reformat_card(self, card):
        card = card[1:]
        if card[:2] == "1":
            card = "T" + card[2:]
        print(type(card))
        return card

    async def start_round(self, channel):
        round = self.round
        while True:
            if not(self.bet):
                break
        if round == 1:
            #pre-flop
            a = ['Qd', 'Kd', '9d', 'Jd', 'Td', '4h', '5c'] 
            b = ['Qd', 'Kd', '9d', 'Jd', 'Td', 'Ad', '5c'] 
            print("start 1")
            await channel.send(handeval.compare_hands(a,b) + "\nThe Pre-Flop: \n" + top + "\t" + top + "\t" + top + "\t" + top + "\t" + top + "\n"
            + bot + "\t" + bot + "\t" + bot + "\t" + bot + "\t" + bot)
            await asyncio.sleep(.1)
            await run_menu()
            await self.betting()
        elif round == 2:
            print("start 2")
            self.table_cards.append(self.deal())
            self.table_cards.append(self.deal())
            self.table_cards.append(self.deal())
            table_card1 = self.find_card_emoji(self.table_cards[0])
            table_card2 = self.find_card_emoji(self.table_cards[1])
            table_card3 = self.find_card_emoji(self.table_cards[2])
            await channel.send("The Flop:\n" + table_card1[0] + "\t" + table_card2[0] + "\t" + table_card3[0] + "\t" + top + "\t" + top + "\n"
            + table_card1[1] + "\t" + table_card2[1] + "\t" + table_card3[1] + "\t" + bot + "\t" + bot)
            await asyncio.sleep(.1)
            await run_menu()
            await self.betting()
            #flop
        elif round == 3:
            self.table_cards.append(self.deal())
            table_card1 = self.find_card_emoji(self.table_cards[0])
            table_card2 = self.find_card_emoji(self.table_cards[1])
            table_card3 = self.find_card_emoji(self.table_cards[2])
            table_card4 = self.find_card_emoji(self.table_cards[3])
            await channel.send("The Turn:\n" + table_card1[0] + "\t" + table_card2[0] + "\t" + table_card3[0] + "\t" + table_card4[0] + "\t" + top + "\n"
            + table_card1[1] + "\t" + table_card2[1] + "\t" + table_card3[1] + "\t" + table_card4[1] + "\t" + bot)
            await asyncio.sleep(.1)
            await run_menu()
            await self.betting()
            #turn
        elif round == 4:
            self.table_cards.append(self.deal())
            table_card1 = self.find_card_emoji(self.table_cards[0])
            table_card2 = self.find_card_emoji(self.table_cards[1])
            table_card3 = self.find_card_emoji(self.table_cards[2])
            table_card4 = self.find_card_emoji(self.table_cards[3])
            table_card5 = self.find_card_emoji(self.table_cards[4])
        
            await channel.send("The River:\n" + table_card1[0] + "\t" + table_card2[0] + "\t" + table_card3[0] + "\t" + table_card4[0] + "\t" + table_card5[0] + "\n"
            + table_card1[1] + "\t" + table_card2[1] + "\t" + table_card3[1] + "\t" + table_card4[1] + "\t" + table_card5[1])
            await asyncio.sleep(.1)
            await run_menu()
            await self.betting()
            #river
        else:
            for card in self.table_cards:
                self.formatted_table.append(self.reformat_card(card))
            winner = self.main_pot.find_winner() # why not use winner variable for line below?
            winner_card1 = self.find_card_emoji(winner[0].hand[0])
            winner_card2 = self.find_card_emoji(winner[0].hand[1])
            await channel.send(self.main_pot.find_winner() + "\n" + self.main_pot.players + "\n" + winner[0].player_obj.display_name + "\n" + winner[1] + "\nWinning Hand:\n" + winner_card1[0] + "\t" + winner_card2[0] + "\n" + winner_card1[1] + "\t" + winner_card2[1])
            global game
            game = None
            
            #find winner

    async def betting(self):
        self.turns_left = self.players_in.copy()
        self.bet = True
        self.current_player = self.turns_left[0]
        self.current_bet = 0
        while True:
            print("betting loop")
            print("turns: " + str(len(self.turns_left)))
            await channel.send(self.current_player.player_obj.display_name + "'s turn\nAuto fold/check in 10 seconds")
            await asyncio.sleep(betting_time) 
            if not(self.done):
                if self.current_player.bet >= self.current_bet or self.current_player.bal == 0:
                    await channel.send(self.current_player.player_obj.display_name + " auto checked")
                    self.check()
                else:
                    await channel.send(self.current_player.player_obj.display_name + " auto folded")
                    self.fold()
            
            if len(self.turns_left) > 0:
                self.i += 1
                self.current_player = self.turns_left[(self.i)%len(self.turns_left)]
                self.done = False
            else:
                break

        self.done = False
        self.bet = False                  
        self.round += 1
        
        await self.start_round(channel)

@client.command()
async def load(ctx):
    users_data = ""
    for member in channel.guild.members: 
        check = uf.get_balance(member.id)
        await asyncio.sleep(1)
        if check == -1:
            users_data += str(member.id) + ":" + "1000-" + "\n"
            #await channel.send("Writing " + str(member.id) + " with $1000")
        else:
            print("already contains" + str(member.id)) 
            #await channel.send("already contains " + str(member.id))
    uf.write_new_users(users_data)
       
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def create_game(players):
    global game
    game = Poker(players, 1, 100, channel)
    print(game)
    await run_game(game)
    return

async def run_menu():
    view = Menu()
    await channel.send("",view=view)

class JoinMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Join Table", style = discord.ButtonStyle.green)
    async def call(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in active_players:
            active_players.append(interaction.user)
            await interaction.response.send_message(str(interaction.user.display_name) + " joined the table! \n" + str(len(active_players)) + "/" + str(min_players))
        else:
            await interaction.response.send_message(str(interaction.user.display_name) + " already joined")

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    @discord.ui.button(label="View Hand", style = discord.ButtonStyle.blurple)
    async def get_hand(self, interaction: discord.Interaction, button: discord.ui.Button):
        for i in range(len(game.players)):
            if game.players[i].player_obj.id == interaction.user.id:
                card1 = game.find_card_emoji(game.players[i].hand[0])
                card2 = game.find_card_emoji(game.players[i].hand[1])
                await interaction.response.send_message("\n" + card1[0] + "\t" + card2[0] + "\n" + card1[1] + "\t" + card2[1], ephemeral=True)

    @discord.ui.button(label="Call", style = discord.ButtonStyle.green)
    async def call(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("called")
        if interaction.user == game.current_player.player_obj and game.bet and not(game.done):
            game.call()
            await interaction.response.send_message(interaction.user.display_name +" called for " + str(game.current_bet))
        else:
            await interaction.response.send_message("Not your turn" + str(game.bet) + str(game.done), ephemeral=True)
        
    @discord.ui.button(label="Raise", style = discord.ButtonStyle.red)
    async def raise_call(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == game.current_player.player_obj and game.bet and not(game.done):
            game.raise_call(1)
            await interaction.response.send_message("Raised for " + str(game.current_bet))
        else:
            await interaction.response.send_message("Not your turn", ephemeral=True)

    @discord.ui.button(label="Check", style = discord.ButtonStyle.gray)
    async def check(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == game.current_player.player_obj and game.bet and not(game.done):
            game.check()
            await interaction.response.send_message("Checked")
        else:
            await interaction.response.send_message("Not your turn", ephemeral=True)
    @discord.ui.button(label="Fold", style = discord.ButtonStyle.grey)
    async def fold(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == game.current_player.player_obj and game.bet and not(game.done):
            game.fold()
            await interaction.response.send_message("Folded")
        else:
            await interaction.response.send_message("Not your turn", ephemeral=True)

@client.event
async def on_message(message):
    if message.channel.id == 732386342402785418:
        if message.content.startswith('hi'):
            await message.channel.send("hi")
        if message.content.startswith('hello'):
            await message.channel.send("hi")
        if message.content.startswith('aidan'):
            aidan = "aidan " * 300
            await message.channel.send(aidan)

        if message.author == client.user:
            return

        if not message.content.startswith('$p'):
            return

        global channel
        channel = message.channel
        print(type(game))
        if game is not None:
            print(game.table_cards)
        await lobby(message)

        if message.content.startswith('$bal'):
            await message.channel.send(message.author.display_name + "'s balance: " + uf.get_balance(message.author.id))
        if message.content.startswith("$ls"):
            uf.sort_bals()
            data = uf.return_board()
            board = ""
            for user in data:
                board += "* " + client.get_user(int(user[0])).display_name + ": " + user[1] + "\n"
            await message.channel.send(board) 
        if message.content.startswith("$help"):
            await message.channel.send("* $p - starts game\n* $bal - returns your balance\n* $ls - leaderboard of users in the server")
       await client.process_commands(message)
            
async def lobby(message_start):
    ##ex = discord.utils.get(client.emojis, name='rQ')
    active_players.clear()
    view = JoinMenu()
    await message_start.channel.send(view=view)
  
    await asyncio.sleep(game_start_time)

    if len(active_players) >= min_players:
        await message_start.channel.send("Starting game in 5 seconds")
        await asyncio.sleep(5)
        print(type(game))
        await create_game(active_players)
    else:
        await message_start.channel.send("Game Expired")
    

async def run_game(game):
    print("dealing")
    game.deal_players()
    await game.start_round(channel)

token = os.getenv('poker_bot_key')
client.run(token)
