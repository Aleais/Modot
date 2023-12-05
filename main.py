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
log_file_path = "/storage/console_logs.txt"

# Create/open a file to write logs
log_file_path = "console_logs.txt"
log_file = open(log_file_path, "w")

# Redirect stdout and stderr to the log file
sys.stdout = log_file
sys.stderr = log_file

if os.getenv('REPL_ID') == '9600d51f-ae09-41bb-a923-5a8d3d772e07':
    raise SystemExit('You must fork this REPL in order to work.\n')

developer = "aleais#2532"

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

@bot.event
async def on_ready():
    print(f"✅ {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} application (/) commands.")
    except Exception as e:
        print(e)

# Shutdown event
# Restore the original stdout and stderr when the bot is about to stop
@bot.event
async def on_shutdown():
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    log_file.close()

class EmbeddedTextModal(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Components for the modal
        self.title_input = discord.ui.TextInput(placeholder="Title", custom_id="title_input")
        self.description_input = discord.ui.TextInput(placeholder="Description", custom_id="description_input")
        self.color_input = discord.ui.TextInput(placeholder="Color (hex)", custom_id="color_input")
        self.image_input = discord.ui.TextInput(placeholder="Image Filename (local)", custom_id="image_input")
        self.thumbnail_input = discord.ui.TextInput(placeholder="Thumbnail Filename (local)", custom_id="thumbnail_input")
        self.channel_input = discord.ui.TextInput(placeholder="Channel ID (optional)", custom_id="channel_input")

        self.add_item(self.title_input)
        self.add_item(self.description_input)
        self.add_item(self.color_input)
        self.add_item(self.image_input)
        self.add_item(self.thumbnail_input)
        self.add_item(self.channel_input)
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.green, label="Confirm", custom_id="confirm_button"))

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, custom_id="confirm_button")
    async def on_confirm_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        title = self.title_input.value
        description = self.description_input.value
        color = self.color_input.value
        image_filename = self.image_input.value
        thumbnail_filename = self.thumbnail_input.value
        channel = self.channel_input.value

        embed1 = discord.Embed(title=title, description=description, color=int(color, 16))
        embed1.set_footer(text=f"created {time.strftime('%Y-%m-%d %H:%M:%S')}")

        file = None
        if image_filename:
            image_path = f"local_images/{image_filename}"
            file = discord.File(image_path)
            embed1.set_image(url=f"attachment://{image_filename}")

        if thumbnail_filename:
            thumbnail_path = f"local_images/{thumbnail_filename}"
            thumbnail_file = discord.File(thumbnail_path)
            embed1.set_thumbnail(url=f"attachment://{thumbnail_filename}")

        target_channel = bot.get_channel(int(channel)) if channel else interaction.channel
        await target_channel.send(embed=embed1, file=file)
        await interaction.response.send_message(f"Embed sent successfully in {target_channel.mention}.")

# Ping command
@bot.tree.command(name="ping", description="Ping the bot!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! `{bot.latency:.2f}ms`")

# custom-response command
@bot.tree.command(name="custom-response", description="Make Custom-Responses (under-development)")
async def custom_response(interaction: discord.Interaction, custom: str):
    await interaction.response.send_message("**Hello! I am Modot. \nAnd this is 'custom response builder' would you like to continue?** \n``[Hint: Type 1 to 'continue' or type 2 to 'cancel'.]``")

    def check(response):
        return response.author == interaction.user and response.channel == interaction.channel and response.content in ['1', '2']

    try:
        user_response = await bot.wait_for("message", check=check, timeout=30)

        if user_response.content == '1':
            await interaction.response.send("Okay! Let's get started. \n **What would you like to do?** \n ``[Hint: Type 1 to add a new response, type 2 to edit a response, type 3 to remove a response or type 4 to cancel.]``")

            try:
                user_response = await bot.wait_for("message", check=check, timeout=30)

                if user_response.content == '1':
                    await interaction.response.send("Okay! ")
                elif user_response.content == '2':
                    await interaction.response.send("Okay! As your wish... ")
                elif user_response.content == '3':
                    await interaction.response.send("Are you sure? \n``[Hint: Type 1 to say 'yes' or type 2 to say 'no'.``")

                    try:
                        user_response = await bot.wait_for("message", check=check, timeout=30)

                        if user_response.content == '1':
                            await interaction.response.send("Okay! ")
                        elif user_response.content == '2':
                            await interaction.response.send("Okay! ")
                            return

                        else:
                            await interaction.response.send("Sorry, didn't understand... Try again later!")

                    except asyncio.TimeoutError:
                        await interaction.response.send("You took too long to respond... Try again later!")

                elif user_response.content == '4':
                    await interaction.response.send("Okay! As your wish... ")
                    return
                else:
                    await interaction.response.send("Sorry, didn't understand... Try again!")

            except asyncio.TimeoutError:
                await interaction.response.send("Sorry, You took too long to respond... Try again!")

        elif user_response.content == '2':
            await interaction.response.send("Okay! As your wish... ")
            return

        else:
            await interaction.response.send("Sorry, I didn't understand... Try again!")

    except asyncio.TimeoutError:
        await interaction.response.send("You took too long to respond.")

# Embedded-text Maker
@bot.tree.command(name='embedded-text', description="Make Embedded-Text")
async def embedded_text(interaction: discord.Interaction):
    view = EmbeddedTextModal()
    await interaction.response.send_modal(view)

# Help command
@bot.tree.command(name="help", description="Shows the Help for Commands")
async def help(interaction: discord.Interaction):
    embed2 = discord.Embed(
        title=(f"{bot.user}'s Help"), 
        description=(f"**Prefix** : ``{prefix}`` \n\n**Commands** : \n``ping`` - Shows the bot's latency. \n``custom-response`` - Allows you to create custom responses. \n``embedded-text`` - Allows you to create embedded text. \n\n**Developer** : <@{developer}> \n\n**Support Server** : [Click Here](https://discord.com/invite/STJs8AyGg8)"), 
        color=discord.Color.purple()
    ) 
    await interaction.response.send_message(embed=embed2)

_error_message = f"\n\nI could not find any secret named '{my_secret}' in the Secrets tab."
assert my_secret in os.environ, _error_message

bot.run(os.getenv(my_secret))