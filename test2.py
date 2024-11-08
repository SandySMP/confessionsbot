import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intents if needed

bot = commands.Bot(command_prefix="!", intents=intents)

# Channel IDs for confessions and logs
CONFESSIONS_CHANNEL_ID = 1304457041586159626  # Replace with your confessions channel ID
LOGS_CHANNEL_ID = 1304526058749694063        # Replace with your log channel ID for moderators

# You can adjust the embed color here
EMBED_COLOR = discord.Color.green()  # Customize the color for the confession embed

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f'Logged in as {bot.user} - {bot.user.id}')
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {synced}")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Slash command to submit a confession
@bot.tree.command(name="confess", description="Send an anonymous confession")
async def confess(interaction: discord.Interaction, message: str):
    # Locate the designated channels
    confessions_channel = bot.get_channel(CONFESSIONS_CHANNEL_ID)
    logs_channel = bot.get_channel(LOGS_CHANNEL_ID)

    # Check if the confession channel exists
    if confessions_channel is None:
        await interaction.response.send_message("The confessions channel is not found.", ephemeral=True)
        return

    # Create the embed for the public confession
    confession_embed = discord.Embed(
        title="Anonymous Confession",
        description=message,
        color=EMBED_COLOR  # Use the customizable embed color
    )
    confession_embed.set_footer(text="Confessions Bot")
    confession_embed.timestamp = discord.utils.utcnow()

    # Send the confession to the designated confessions channel as an embed
    await confessions_channel.send(embed=confession_embed)

    # Send a confirmation to the user, visible only to them
    await interaction.response.send_message("Your confession has been sent anonymously!", ephemeral=True)

    # Send a log message with user info to the logs channel if it exists
    if logs_channel is not None:
        log_embed = discord.Embed(
            title="Confession Log",
            description=f"**User:** {interaction.user} ({interaction.user.id})\n**Confession:** {message}",
            color=discord.Color.red()  # Choose a different color for the log embed
        )
        log_embed.set_footer(text="Confession Log")
        log_embed.timestamp = discord.utils.utcnow()

        # Send the log to the logs channel
        await logs_channel.send(embed=log_embed)
    else:
        print("Logs channel is not found. Ensure LOGS_CHANNEL_ID is set correctly.")

# Run the bot with your token
bot.run("MTMwNDQ1Njg5NzI5MzcxMzUyOA.GOfkUf.mt4x0ULXvnSvNZ1L8TiMgWdqnBpa90iBANuG1Q")
