print("Booting up...")

# Imports
import discord
import asyncio
from discord.ext import commands
import os
import time
import sys

# Save the original stdout and stderr
original_stdout = sys.stdout
original_stderr = sys.stderr

# Define the path for the log file in the /storage directory

# Create/open a file to write logs
log_file_path = "console_logs.txt"
log_file = open(log_file_path, "a")
log_file.write("Logs: \n")
log_file.write("\n\nBooting up...\n"
+ f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n") 

log_file.write(f"Python version: {sys.version}\n"
+ f"System version: {sys.version_info}\n"
+ f"Discord.py version: {discord.__version__}\n"
+ f"Running on: {sys.platform}\n"
+ f"{sys.executable}\n\n") 

# Redirect
sys.stdout = log_file
sys.stderr = log_file

if os.getenv('REPL_ID') == '9600d51f-ae09-41bb-a923-5a8d3d772e07':
    raise SystemExit('You must fork this REPL in order to work.\n')

command1="ping"
command2="custom-response"
command3="embedded-text-builder"
command4="help"
command5="server-count"
command6="about-me"

f1=f"time: {time.strftime('%Y-%m-%d %H:%M:%S')}"

# Replace "TOKEN" with your actual Discord bot token
my_secret = "TOKEN"

prefix = "/"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    intents=intents,
    command_prefix=prefix,
    case_insensitive=True,
    strip_after_prefix=True,
    help_command=None
)

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        kwargs["command_prefix"] = prefix
        kwargs["intents"] = intents
        super().__init__(*args, **kwargs)
        self.synced = False

bot = Bot()

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    log_file.write(f"✅ {bot.user}\n")
    try:
        if not bot.synced:
            #Guild_id = bot.guilds[0].id
            synced = await bot.tree.sync()
            bot.synced = True
            log_file.write(f"✅ Synced {len(synced)} commands.\n")
    except Exception as e:
        log_file.write(f"❌ Failed to sync: {e}\n")
        
    log_file.write("\n")

# Shutdown event
# Restore the original stdout and stderr when the bot is about to stop
@bot.event
async def on_shutdown():
    log_file.write("\n❌ Bot is shutting down...\n")
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    log_file.close()

# Class for the modal 'Embedded Text'
class EmbeddedTextModal(discord.ui.Modal, title="Embedded Text Maker"):
    def __init__(self):
        super().__init__()

        # Components for the modal
        self.title_input = discord.ui.TextInput(placeholder="Title", custom_id="title_input", label="Title", style=discord.TextStyle.short, required=False, max_length=30, row=0)
        self.color_input = discord.ui.TextInput(placeholder="Color (hex)", custom_id="color_input", label="Color", style=discord.TextStyle.short, required=True, row=1)
        self.description_input = discord.ui.TextInput(placeholder="Description", custom_id="description_input", label="Description", style=discord.TextStyle.long, required=True, max_length=1000, row=2)
        self.thumbnail_input = discord.ui.TextInput(placeholder="Thumbnail Filename (local)", custom_id="thumbnail_input", label="Thumbnail", style=discord.TextStyle.short, required=False, row=3)
        self.add_item(self.title_input)
        self.add_item(self.color_input)
        self.add_item(self.description_input)
        self.add_item(self.thumbnail_input)
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.green, label="Confirm", custom_id="confirm_button"))

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, custom_id="confirm_button")
    async def on_confirm_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        title = self.title_input.value
        description = self.description_input.value
        color = self.color_input.value
        thumbnail_filename = self.thumbnail_input.value

        embed1 = discord.Embed(title=title, description=description, color=int(color, 16))
        embed1.set_footer(text=f"created {time.strftime('%Y-%m-%d %H:%M:%S')}")

        file = None
        if thumbnail_filename:
            thumbnail_path = f"local_images/{thumbnail_filename}"
            file = discord.File(thumbnail_path)
            embed1.set_thumbnail(url=f"attachment://{thumbnail_filename}")
        else:
            embed1.set_thumbnail(url=bot.user.avatar.url)

        self.message = None
        await interaction.response.send_message(embed=embed1, file=file)
    
    async def on_submit(self, interaction: discord.Interaction, values: dict):
        pass

# Ping command
@bot.tree.command(name=command1, description="Ping the bot!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! `{bot.latency:.2f}ms`", emphmeral=True)

# custom-response command
@bot.tree.command(name=command2, description="Make Custom-Responses (under-development)")
async def custom_response(interaction: discord.Interaction):
    await interaction.response.send_message("**Hello! I am Modot. \nAnd this is 'custom response builder' would you like to continue?** \n``[Hint: Type 1 to 'continue' or type 2 to 'cancel'.]``")

    def check(response):
        return response.author == interaction.user and response.channel == interaction.channel and response.content in ['1', '2']

    try:
        user_response = await bot.wait_for("message", check=check, timeout=30)

        if user_response.content == '1':
            await interaction.followup.send("Okay! Let's get started. \n **What would you like to do?** \n ``[Hint: Type 1 to add a new response, type 2 to edit a response, type 3 to remove a response or type 4 to cancel.]``")

            try:
                user_response = await bot.wait_for("message", check=check, timeout=30)

                if user_response.content == '1':
                    await interaction.followup.send("Okay! ")
                elif user_response.content == '2':
                    await interaction.followup.send("Okay! As your wish... ")
                elif user_response.content == '3':
                    await interaction.followup.send("Are you sure? \n``[Hint: Type 1 to say 'yes' or type 2 to say 'no'.``")

                    try:
                        user_response = await bot.wait_for("message", check=check, timeout=30)

                        if user_response.content == '1':
                            await interaction.followup.send("Okay! ")
                        elif user_response.content == '2':
                            await interaction.followup.send("Okay! ")
                            return

                        else:
                            await interaction.followup.send("Sorry, didn't understand... Try again later!")

                    except asyncio.TimeoutError:
                        await interaction.followup.send("You took too long to respond... Try again later!")

                elif user_response.content == '4':
                    await interaction.followup.send("Okay! As your wish... ")
                    return
                else:
                    await interaction.followup.send("Sorry, didn't understand... Try again!")

            except asyncio.TimeoutError:
                await interaction.followup.send("Sorry, You took too long to respond... Try again!")

        elif user_response.content == '2':
            await interaction.followup.send("Okay! As your wish... ")
            return

        else:
            await interaction.followup.send("Sorry, I didn't understand... Try again!")

    except asyncio.TimeoutError:
        await interaction.followup.send("You took too long to respond.")

# Embedded-text Maker
@bot.tree.command(name=command3, description="Make Embedded-Text")
async def embedded_text(interaction: discord.Interaction):
    embedded_text_modal = EmbeddedTextModal()
    message = await interaction.response.send_message(embed=embedded_text_modal.message.embeds[0], components=[embedded_text_modal])

  # Wait for user interaction
    interaction_data = await bot.wait_for("component_interaction", check=lambda i: i.custom_id == "confirm_button" and i.message.id == message.id and i.user.id == interaction.user.id)
    # Update the reference in the modal
    embedded_text_modal.message = message
    await interaction_data.defer(edit_origin=True)
    await interaction_data.edit_origin(embed=embedded_text_modal.message.embeds[0], components=[embedded_text_modal])
    await embedded_text_modal.on_confirm_button(interaction_data.component, interaction_data)

# Help command
@bot.tree.command(name=command4, description="Shows the Help for Commands")
async def help(interaction: discord.Interaction):
    embed2 = discord.Embed(
        title=(f"{bot.user}'s Help"), 
        description=(f"**Prefix** : ``{prefix}`` \n\n**Commands** : \n``{command1}`` - Shows the bot's latency. \n``{command2}`` - Allows you to create custom responses. \n``{command3}`` - Allows you to create embedded text. \n``{command4}`` \n``{command5}`` \n``{command6}`` \n\n**Developer** : [@aleais#2532](https://discord.com/invite/STJs8AyGg8) \n\n**Support Server** : [Click Here](https://discord.com/invite/STJs8AyGg8)"), 
        color=discord.Color.purple()
         ) 
    await interaction.response.send_message(embed=embed2)

# Server Count
@bot.tree.command(name=command5, description="Veiw the amount of servers the Bot is in")
async def server_count(interaction: discord.Interaction):
    await interaction.response.send_message(f"I am in {len(bot.guilds)} servers")

# About me commands
@bot.tree.command(name=command6, description="About me")
async def about_me(interaction: discord.Interaction):
    embed3=discord.Embed(
title="About me",
                         description=f"Hello, My name is Modot. \nI am a bot made by lone dev: [@aleais#2532](https://discord.com/invite/STJs8AyGg8). \nBut No, worries i ve frnds. You are my frnd too! \nwanna meet my other frnds? \n[server](https://discord.com/invite/STJs8AyGg8) Click this to meet my frnds. \n\n**My prefix is** ``{prefix}`` \n\n**My commands are** \n``{command1}`` - Shows the bot's latency. \n``{command2}`` - Allows you to create custom responses. \n``{command3}`` - Allows you to create embedded text. \n``{command4}`` \n``{command5}`` \n{command6} \n\n**My developer is** [@aleais#2532](https://discord.com/invite/STJs8AyGg8) \n\n**My support server is** [Click Here](https://discord.com/invite/STJs8AyGg8) \n\n**My invite link is** [Click Here](https://discord.com/api/oauth2/authorize?client_id=1179052200094351432&permissions=8&scope=bot) \n\nI am currently in {len(bot.guilds)} servers. \n\n**My ping is** {bot.latency:.2f}ms", 
                        color=discord.Color.purple()
                        ) 
    embed3.set_thumbnail(url=bot.user.avatar.url)
    embed3.set_image(url="https://media.discordapp.net/attachments/1099862600285957140/1102615552524013628/standard_1.gif")
    embed3.set_author(name=f"{bot.user}", icon_url=bot.user.avatar.url)
    embed3.set_footer(text=f"Requested by {interaction.user.name}, At {f1}", icon_url=interaction.user.avatar.url)
    await interaction.response.send_message(embed=embed3) 

# Run the Bot & Error Msg
_error_message = f"\n\nI could not find any secret named '{my_secret}' in the Secrets tab."
assert my_secret in os.environ, _error_message

bot.run(os.getenv(my_secret))