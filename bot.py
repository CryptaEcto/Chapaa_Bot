import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Track the current party message
active_party_message = None

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online and ready to raise Chapaas!")

@bot.command(name="startparty")
@commands.has_permissions(manage_guild=True)
async def start_party(ctx):
    global active_party_message

    # Check for an existing party
    if active_party_message:
        await ctx.send("There is already an active party! Please join that one before creating a new one.")
        return

    # Create a new party request message
    embed = discord.Embed(
        title="A New Party is Forming!",
        description="Click below to join the adventure! We need 4 Chapaas to start.",
        color=discord.Color.blue()
    )
    message = await ctx.send(embed=embed, view=PartyJoinButtons(bot))

    active_party_message = message
    await message.pin()

# Button view class for joining party
class PartyJoinButtons(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.joined_users = []

    @discord.ui.button(label="Join Party", style=discord.ButtonStyle.green)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.joined_users:
            await interaction.response.send_message("You’re already in the party!", ephemeral=True)
            return

        self.joined_users.append(interaction.user.id)
        await interaction.response.send_message(f"{interaction.user.display_name} has joined the party!", ephemeral=True)

        if len(self.joined_users) >= 4:
            await self.party_full(interaction)

    async def party_full(self, interaction):
        global active_party_message

        # Handle pin and delete
        try:
            await active_party_message.unpin()
            await active_party_message.delete()
        except Exception as e:
            print(f"Error cleaning up party message: {e}")

        await interaction.channel.send("The party is full! Time to begin your adventure!")
        active_party_message = None

# Run the bot with your token
bot.run("YOUR_BOT_TOKEN")

