import discord
import random

# ディスコードトークン
DISCORD_TOKEN = ''# 左の''に、あなたのディスコードトークンを記入

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

class NumberGuessingGame:
    def __init__(self):
        self.answer = random.randint(1, 100)
        self.players = []
        self.turn = 0
        self.finished = False

    def add_player(self, player):
        if len(self.players) < 2:
            self.players.append(player)
            return True
        return False

    def next_turn(self):
        self.turn = (self.turn + 1) % 2  # Alternates between 0 and 1 (player1 and player2)

    def guess(self, player, guess):
        if self.players[self.turn] == player:
            if guess < self.answer:
                return "正解は入力値より大きいです。"
            elif guess > self.answer:
                return "正解は入力値より小さいです。"
            else:
                self.finished = True
                return f"{player} が正解しました！"
        return f"{player} の順番ではありません。"

    def reset(self):
        self.finished = True  # ゲームを終了状態にする

game = None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    global game

    if message.author == client.user:
        return

    # ゲームの開始コマンド
    if message.content in ["game start", "gamestart"]:
        if game is None or game.finished:
            game = NumberGuessingGame()
            await message.channel.send("数当てゲームを開始します！1から100までの数を当ててください。\nPlayer1 と Player2 を決定します。'join' コマンドを使用して参加してください。")
        else:
            await message.channel.send("現在、進行中のゲームがあります。")

    # プレイヤーがゲームに参加する
    elif message.content == "join":
        if game is not None and len(game.players) < 2:
            if game.add_player(message.author.name):
                await message.channel.send(f"{message.author.name} がゲームに参加しました。")
                if len(game.players) == 2:
                    await message.channel.send(f"{game.players[0]} と {game.players[1]} の準備が整いました！ {game.players[0]} からスタートします。\n'guess'コマンドを使用して数を指定してください。")
            else:
                await message.channel.send("すでに2人のプレイヤーが参加しています。")
        else:
            await message.channel.send("ゲームが開始されていないか、すでにプレイヤーが満員です。")

    # プレイヤーが数字を推測する
    elif message.content.startswith("guess "):
        if game is not None and not game.finished:
            try:
                guess = int(message.content.split()[1])
                response = game.guess(message.author.name, guess)
                await message.channel.send(response)
                if not game.finished:
                    game.next_turn()
                    await message.channel.send(f"{game.players[game.turn]} の番です。")
            except ValueError:
                await message.channel.send("有効な整数を入力してください。")
        else:
            await message.channel.send("ゲームはまだ開始していないか、すでに終了しています。")

    # ゲームを強制終了するコマンド
    elif message.content == "!end":
        if game is not None:
            game.reset()
            await message.channel.send("ゲームを強制終了しました。")
            game = None  # ゲームをリセット
        else:
            await message.channel.send("現在、進行中のゲームはありません。")

client.run(DISCORD_TOKEN)
