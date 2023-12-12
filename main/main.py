print("Booting up...")

# Imports
import discord
import asyncio
from discord.ext import commands
import os
import time
import datetime
import sys
from keep_alive import keep_alive

# Save the original stdout and stderr
original_stdout = sys.stdout
original_stderr = sys.stderr

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
command7="feedback"
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
    
# Ping command
@bot.tree.command(name=command1, description="Ping the bot!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! `{bot.latency:.2f}ms`", ephemeral=True)

# custom-response command
@bot.tree.command(name=command2, description="Make Custom-Responses (under-development)")
async def custom_response(interaction: discord.Interaction):
    await interaction.response.send_message("**Hello! I am Modot. \nAnd this is 'custom response builder' would you like to continue?** \n``[Hint: Type 1 to 'continue' or type 2 to 'cancel'.]``", ephemeral=True)

    def check(response):
        return response.author == interaction.user and response.channel == interaction.channel and response.content in ['1', '2']

    try:
        user_response = await bot.wait_for("message", check=check, timeout=30)

        if user_response.content == '1':
            await interaction.followup.send("Okay! Let's get started. \n **What would you like to do?** \n ``[Hint: Type 1 to add a new response, type 2 to edit a response, type 3 to remove a response or type 4 to cancel.]``", ephemeral=True)

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
 await interaction.response.send_message("**Hello! I am Modot. \nAnd this is 'Embedded text builder' would you like to continue?** \n``[Hint: Type 1 to 'continue' or type 2 to 'cancel'.]``", ephemeral=True)

 def check(response):
    return response.author == interaction.user and response.channel == interaction.channel and response.content in ['1', '2']

 try:
    user_response = await bot.wait_for("message", check=check, timeout=30)

    if user_response.content == '1':
      await interaction.followup.send("Okay! Let's get started. \n**Type down your Embed's Title.** \n``[You've 5 minutes to answer.]``", ephemeral=True)
      def check(response):
        return response.author == interaction.user and response.channel == interaction.channel

      try:
        user_response = await bot.wait_for("message", check=check, timeout=60 * 5)
        title = user_response.content

        await interaction.followup.send("**Type down your Embed's Description.** \n``[You've 5 minutes to answer.]``", ephemeral=True)

        def check(response):
          return response.author == interaction.user and response.channel == interaction.channel

        try:
          user_response = await bot.wait_for("message", check=check, timeout=60 * 5)
          description = user_response.content

          await interaction.followup.send("**Type down your Embed's Color.** \n``[You've 5 minutes to answer.Type 'skip' to skip.]``", ephemeral=True)
          def check(response):
           return response.author == interaction.user and response.channel == interaction.channel
          try:
           user_response = await bot.wait_for("message", check=check, timeout=60 * 5)
           color = user_response.content
           if color.lower() == "skip":
             color = discord.Color.default()
           elif color.lower() == "red":
             color = discord.Color.red()
           elif color.lower() == "green":
             color = discord.Color.green()
           elif color.lower() == "blue":
             color = discord.Color.blue()
           elif color.lower() == "yellow":
             color = discord.Color.yellow()
           elif color.lower() == "orange":
             color = discord.Color.orange()
           elif color.lower() == "purple":
             color = discord.Color.purple()
           elif color.lower() == "teal":
             color = discord.Color.teal()
           elif color.lower() == "magenta":
             color = discord.Color.magenta()
           elif color.lower() == "gold":
             color = discord.Color.gold()
           elif color.lower() == "dark_gold":
             color = discord.Color.dark_gold()
           elif color.lower() == "dark_orange":
             color = discord.Color.dark_orange()
           elif color.lower() == "dark_red":
             color = discord.Color.dark_red()
           elif color.lower() == "dark_teal":
             color = discord.Color.dark_teal()
           elif color.lower() == "dark_purple":
             color = discord.Color.dark_purple()
           elif color.lower() == "dark_magenta":
             color = discord.Color.dark_magenta()
           elif color.lower() == "dark_grey":
             color = discord.Color.dark_grey()
           elif color.lower() == "light_grey":
             color = discord.Color.light_grey()
           elif color.lower() == "darker_grey":
             color = discord.Color.darker_grey()
           elif color.lower() == "not_quite_black":
             color = discord.Color.not_quite_black()
           elif color.lower() == "blanched_almond":
             color = discord.Color.blanched_almond()
           elif color.lower() == "bisque":
             color = discord.Color.bisque()
           elif color.lower() == "coral":
             color = discord.Color.coral()
           elif color.lower() == "dark_salmon":
             color = discord.Color.dark_salmon()
           elif color.lower() == "light_salmon":
             color = discord.Color.light_salmon()
           elif color.lower() == "light_coral":
             color = discord.Color.light_coral()
           elif color.lower() == "pale_violet_red":
             color = discord.Color.pale_violet_red()
           elif color.lower() == "pale_golden_red":
             color = discord.Color.pale_golden_red()
           elif color.lower() == "pale_turquoise":
             color = discord.Color.pale_turquoise()
           elif color.lower() == "pale_green":
             color = discord.Color.pale_green()
           elif color.lower() == "pale_turquoise_green":
             color = discord.Color.pale_turquoise_green()
           elif color.lower() == "pale_cyan":
             color = discord.Color.pale_cyan()
           elif color.lower() == "pale_light_blue":
             color = discord.Color.pale_light_blue()
           elif color.lower() == "pale_blue":
             color = discord.Color.pale_blue()
           elif color.lower() == "pale_blue_violet":
             color = discord.Color.pale_blue_violet()
           elif color.lower() == "pale_indigo":
             color = discord.Color.pale_indigo()
           elif color.lower() == "dark_seagreen":
             color = discord.Color.dark_seagreen()
           elif color.lower() == "dark_slate_blue":
             color = discord.Color.dark_slate_blue()
           elif color.lower() == "dark_cyan":
             color = discord.Color.dark_cyan()
           elif color.lower() == "dark_turquoise":
             color = discord.Color.dark_turquoise()
           elif color.lower() == "dark_violet":
             color = discord.Color.dark_violet()
           elif color.lower() == "black":
             color = discord.Color.black()
           elif color.lower() == "white":
             color = discord.Color.white()
           elif color.lower() == "grey":
             color = discord.Color.grey()
           else:
             await interaction.followup.send("Sorry, I didn't understand... Try again!", ephemeral=True)
           embed1 = discord.Embed(title=title, description=description, color=color, timestamp=datetime.datetime.utcnow())
           await interaction.followup.send(embed=embed1)
          except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to respond... Try again!", ephemeral=True)
        except asyncio.TimeoutError:
          await interaction.followup.send("You took too long to respond... Try again!", ephemeral=True)
      except asyncio.TimeoutError:
        await interaction.followup.send("You took too long to respond... Try again!", ephemeral=True)

    elif user_response.content == '2':
      await interaction.followup.send("Okay! As your wish... ", ephemeral=True)
      return

    else:
      await interaction.followup.send("Sorry, I didn't understand... Try again!", ephemeral=True)

 except asyncio.TimeoutError:
    await interaction.followup.send("You took too long to respond.", ephemeral=True)

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

# Feedback command
@bot.tree.command(name=command7, description="Give feedback to the developer")
async def feedback(interaction: discord.Interaction):
    feedback_log_path = "feedback_logs.txt"
    feedback_log = open(feedback_log_path, "a")
    await interaction.response.send_message("**Hello! I am Modot. \nAnd this is 'Feedback picker' would you like to continue?** \n``[Hint: Type 1 to 'continue' or type 2 to 'cancel'.]``", ephemeral=True)

    def check(response):
        return response.author == interaction.user and response.channel == interaction.channel and response.content in ['1', '2']
    
    try:
        user_response = await bot.wait_for("message", check=check, timeout=60)
        if user_response.content == '1':
            sys.stdout = feedback_log
            sys.stderr = feedback_log
            await interaction.followup.send("Okay! Now please type down your feedback's description. \n\n[You've 15 min to type down your feedback]", ephemeral=True)

            def check(response):
                return response.author == interaction.user and response.channel == interaction.channel

            try:
                user_response = await bot.wait_for("message", check=check, timeout=60 * 15)  # 15 minutes
                feedback_title = interaction.user.name
                feedback_description = user_response.content
                feedback_log.write(f"Feedback from {feedback_title}: {feedback_description} \nAt {f1} \n")
                feedback_log.write(f"User: {interaction.user.name}, Guild: {interaction.guild.name}\n")
                feedback_log.write(f"Title: {feedback_title}\nDescription: {feedback_description}\n\n")
              
                main_guild_id = int(os.environ['GUILD_ID'])
                main_guild = bot.get_guild(main_guild_id)
                feedback_channel_id = int(os.environ['CHANNEL_ID'])
                feedback_channel = main_guild.get_channel(int(feedback_channel_id))

                if feedback_channel:
                    await feedback_channel.send(f"New feedback from {interaction.user.name} in {interaction.guild.name}:\n\nTitle: {feedback_title}\nDescription: {feedback_description}")

                await interaction.followup.send("Okay! Thank you for your feedback. \n\n**Feedback** \n"
                                               f"Title : `{feedback_title}` \nDescription : `{feedback_description}`", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("You took too long to respond... Please try again!", ephemeral=True)
            sys.stdout = original_stdout
            sys.stderr = original_stderr

        elif user_response.content == '2':
            await interaction.followup.send("Okay! As your wish... ", ephemeral=True)
        else:
            await interaction.user.send("Sorry, I didn't understand... Please try again!", ephemeral=True)

    except asyncio.TimeoutError:
        await interaction.user.send("You took too long to respond... Please try again!", ephemeral=True)
    feedback_log.close()

# Run the Bot & Error Msg
_error_message = f"\n\nI could not find any secret named '{my_secret}' in the Secrets tab."
assert my_secret in os.environ, _error_message

bot.run(os.getenv(my_secret))
keep_alive()