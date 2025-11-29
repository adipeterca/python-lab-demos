import discord
from datetime import datetime
import utils



intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)
scores = {}

@client.event
async def on_ready():
    print("""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██ ▄▄▀█▄ ▄██ ▄▄▄ ██ ▄▄▀██ ▄▄▄ ██ ▄▄▀██ ▄▄▀████ ▄▄▄██ ███ █ ▄▄▀██ █████ ██ █ ▄▄▀█▄▄ ▄▄██ ▄▄▄ ██ ▄▄▀██
██ ██ ██ ███▄▄▄▀▀██ █████ ███ ██ ▀▀▄██ ██ ████ ▄▄▄███ █ ██ ▀▀ ██ █████ ██ █ ▀▀ ███ ████ ███ ██ ▀▀▄██
██ ▀▀ █▀ ▀██ ▀▀▀ ██ ▀▀▄██ ▀▀▀ ██ ██ ██ ▀▀ ████ ▀▀▀███▄▀▄██ ██ ██ ▀▀ ██▄▀▀▄█ ██ ███ ████ ▀▀▀ ██ ██ ██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")
    print(f"Started at {datetime.now().strftime('%H:%M:%S')}")

@client.event
async def on_message(msg: discord.Message):
    if msg.author == client.user:
        return

    # Safeguard to consider only private DMs
    if not isinstance(msg.channel, discord.DMChannel):
        print(f"[WARNING] '{msg.author.name}' submitted a non-private message: '{msg.content}'")
        return
    
    if len(msg.attachments) == 0:
        await msg.channel.send("No '.py' file attachment provided. Please provide one to evaluate.")
        return
    
    if len(msg.attachments) > 1:
        await msg.channel.send("You submitted too many attachments. Only 1 attachment must be send at a time.")
        return
    
    attachment = msg.attachments[0]

    if not attachment.filename.endswith(".py"):
        await msg.channel.send(f"'{attachment.filename}' is not a Python file.")
        print(f"[WARNING] '{msg.author.name}' submitted '{attachment.filename}' which is not a Python file")
        return

    guild: discord.Guild = client.get_guild(1443890088529494059)
    if guild is None:
        raise RuntimeError("Invalid guild ID provided")

    member: discord.Member = guild.get_member(msg.author.id)
    if member is None:
        raise RuntimeError("Invalid author / student ID provided")

    try:
        
        author = member.display_name
        local_filepath = utils.create_submission_path(author)

        with open(local_filepath, "w") as f:
            file_bytes = await attachment.read()
            f.write(file_bytes.decode())

    except Exception as e:
        print(f"[ERROR] Could not save file '{local_filepath}'")
        print(e)

        await msg.channel.send("I'm sorry, but I could not process your upload. Please contact your teacher.")
        return

    
    print(f"[INFO] Saved submission from '{author}' as '{local_filepath}'")
    await msg.channel.send(":white_check_mark: **Submission succesful!** Please wait for it to run ...")

    response = utils.run_submission(local_filepath)

    # Got errors, inform teacher
    if len(response["errors"]) != 0:

        # This output is unsafe from an async perspective tho
        # Maybe rewrite it?
        print("[ERROR] The submission failed in a critical point. Here's why:")
        print(*response["errors"], sep="\n")
        print("Output send to user: ")
        print(*response["test_logs"], sep="\n")

    await msg.channel.send("### Traceback: \n" + "\n- ".join(response["test_logs"]))
    await msg.channel.send(f"### Final score: {response['score']}")

    # Update the score only when necessary
    if author not in scores:
        scores[author] = 0
    elif scores[author] <= response['score']:
        scores[author] = response['score']