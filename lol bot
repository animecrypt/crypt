import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# ============================================================
# SETUP
# ============================================================

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN is missing. Create a .env file containing:\n"
        "DISCORD_TOKEN=YOUR_BOT_TOKEN"
    )

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# ============================================================
# ROLE IDs
# ============================================================

ROLES = {
    "management": 1544962832184119386,
    "level_50": 1545279664082255883,
    "level_40": 1545279492912844912,
    "level_30": 1545279359231983646,
    "level_20": 1545279227236974683,
    "level_10": 1545279034680680488,
    "level_5": 1545278882616180746,
    "divas": 1545546903360512120,
    "monarchs": 1545697705345421313,
    "kitten": 1545546997090750555,
    "artist": 1544962843802345512,
    "imperial_alpha": 1548537294967935078,
    "melodist": 1544962844984872980,
    "moon_beam_maidan": 1545546500933689454,
    "mistic_warden": 1546068438475079730,
    "prettiest_apsara": 1545546815707807774,
    "warriors": 1548530578343600238,
    "over_seers": 1546068303296856134,
    "the_sinister_one": 1546068900695777290,
    "hawties": 1545546654005076059,
    "ivory": 1548537480943247430,
    "infinite_resonance": 1546068248443752478,
    "spotify": 1545521005617881229,
    "scarlet_witch": 1545546442939047956,
    "the_luminaries": 1546068160229285909,
    "snow_princess": 1545546343513325670,
    "spiderman": 1547711437693124732,
    "commander": 1546068384473550908,
    "vc_help": 1546591858145235004,
    "ticket_admin": 1545145899725103144,
    "hangout_manager": 1548241328490414191,
    "gaming_manager": 1548241961104834682,
    "singing_manager": 1548240879804874752,
    "head_hangout_mod": 1548226719167807528,
    "head_gaming_mod": 1548226503949418648,
    "head_singing_mod": 1548225761767465000,
    "hangout_mod": 1545047689329115136,
    "gaming_mod": 1545046367137964125,
    "singing_mod": 1544962834767675412,
    "junior_hangout_mod": 1548226826998906920,
    "junior_gaming_mod": 1548226617254354994,
    "junior_singing_mod": 1548226374119063562,
}


# ============================================================
# PERMISSIONS
# ============================================================

# Management can manage all configured roles except Management itself.
# This prevents the bot from granting/removing the Management role.
MANAGEMENT_TARGETS = set(ROLES.values()) - {ROLES["management"]}

PERMISSIONS = {
    # Management
    ROLES["management"]: MANAGEMENT_TARGETS,

    # Hangout
    ROLES["hangout_manager"]: {
        ROLES["head_hangout_mod"],
        ROLES["hangout_mod"],
        ROLES["junior_hangout_mod"],
    },

    # Gaming
    ROLES["gaming_manager"]: {
        ROLES["head_gaming_mod"],
        ROLES["gaming_mod"],
        ROLES["junior_gaming_mod"],
    },

    # Singing
    ROLES["singing_manager"]: {
        ROLES["head_singing_mod"],
        ROLES["singing_mod"],
        ROLES["junior_singing_mod"],
        ROLES["artist"],
        ROLES["melodist"],
        ROLES["spotify"],
    },

    # Head Hangout Mod
    ROLES["head_hangout_mod"]: {
        ROLES["hangout_mod"],
        ROLES["junior_hangout_mod"],
    },

    # Head Gaming Mod
    ROLES["head_gaming_mod"]: {
        ROLES["gaming_mod"],
        ROLES["junior_gaming_mod"],
    },

    # Head Singing Mod
    ROLES["head_singing_mod"]: {
        ROLES["singing_mod"],
        ROLES["junior_singing_mod"],
        ROLES["artist"],
        ROLES["melodist"],
        ROLES["spotify"],
    },

    # Singing Mod
    ROLES["singing_mod"]: {
        ROLES["artist"],
        ROLES["melodist"],
        ROLES["spotify"],
    },
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_manager_roles(member: discord.Member):
    """Return configured management roles held by a member."""
    member_role_ids = {role.id for role in member.roles}

    return [
        manager_role_id
        for manager_role_id in PERMISSIONS
        if manager_role_id in member_role_ids
    ]


def can_manage(member: discord.Member, target_role_id: int) -> bool:
    """Check whether a member is authorized to manage a target role."""
    for manager_role_id in get_manager_roles(member):
        if target_role_id in PERMISSIONS[manager_role_id]:
            return True

    return False


def hierarchy_check(
    guild: discord.Guild,
    issuer: discord.Member,
    target_role: discord.Role,
):
    """
    Check Discord role hierarchy for the bot and command issuer.
    Returns (True, "") when allowed, otherwise (False, reason).
    """

    bot_member = guild.me

    if bot_member is None:
        return False, "I could not determine my role in this server."

    # Bot cannot manage roles at or above its highest role.
    if target_role >= bot_member.top_role:
        return (
            False,
            "I cannot manage this role because it is above or equal "
            "to my highest role. Move my bot role above it."
        )

    # Server owner is not restricted by member role hierarchy.
    if issuer.id != guild.owner_id:

        if target_role >= issuer.top_role:
            return (
                False,
                "You cannot manage a role that is above or equal "
                "to your highest role."
            )

    return True, ""


# ============================================================
# EVENTS
# ============================================================

@bot.event
async def on_ready():
    print("----------------------------------------")
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as error:
        print(f"Slash command sync error: {error}")

    print("----------------------------------------")


# ============================================================
# /giverole
# ============================================================

@bot.tree.command(
    name="giverole",
    description="Give an authorized role to a member."
)
@app_commands.describe(
    member="Member who should receive the role",
    role="Role to give"
)
async def giverole(
    interaction: discord.Interaction,
    member: discord.Member,
    role: discord.Role,
):

    if not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message(
            "❌ This command can only be used inside a server.",
            ephemeral=True,
        )
        return

    issuer = interaction.user

    if role.is_default():
        await interaction.response.send_message(
            "❌ You cannot assign @everyone.",
            ephemeral=True,
        )
        return

    if not can_manage(issuer, role.id):
        await interaction.response.send_message(
            "❌ You are not authorized to give this role.",
            ephemeral=True,
        )
        return

    allowed, reason = hierarchy_check(
        interaction.guild,
        issuer,
        role,
    )

    if not allowed:
        await interaction.response.send_message(
            f"❌ {reason}",
            ephemeral=True,
        )
        return

    if role in member.roles:
        await interaction.response.send_message(
            f"⚠️ {member.mention} already has {role.mention}.",
            ephemeral=True,
        )
        return

    try:
        await member.add_roles(
            role,
            reason=f"Authorized role assignment by {issuer}"
        )

        await interaction.response.send_message(
            f"✅ {role.mention} has been given to {member.mention}."
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Discord rejected the role change. "
            "Make sure I have **Manage Roles** permission and "
            "my bot role is above the target role.",
            ephemeral=True,
        )

    except discord.HTTPException as error:
        await interaction.response.send_message(
            f"❌ Discord error: `{error}`",
            ephemeral=True,
        )


# ============================================================
# /removerole
# ============================================================

@bot.tree.command(
    name="removerole",
    description="Remove an authorized role from a member."
)
@app_commands.describe(
    member="Member who should lose the role",
    role="Role to remove"
)
async def removerole(
    interaction: discord.Interaction,
    member: discord.Member,
    role: discord.Role,
):

    if not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message(
            "❌ This command can only be used inside a server.",
            ephemeral=True,
        )
        return

    issuer = interaction.user

    if role.is_default():
        await interaction.response.send_message(
            "❌ You cannot remove @everyone.",
            ephemeral=True,
        )
        return

    if not can_manage(issuer, role.id):
        await interaction.response.send_message(
            "❌ You are not authorized to remove this role.",
            ephemeral=True,
        )
        return

    allowed, reason = hierarchy_check(
        interaction.guild,
        issuer,
        role,
    )

    if not allowed:
        await interaction.response.send_message(
            f"❌ {reason}",
            ephemeral=True,
        )
        return

    if role not in member.roles:
        await interaction.response.send_message(
            f"⚠️ {member.mention} does not have {role.mention}.",
            ephemeral=True,
        )
        return

    try:
        await member.remove_roles(
            role,
            reason=f"Authorized role removal by {issuer}"
        )

        await interaction.response.send_message(
            f"✅ {role.mention} has been removed from {member.mention}."
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Discord rejected the role change. "
            "Check Manage Roles and the role hierarchy.",
            ephemeral=True,
        )

    except discord.HTTPException as error:
        await interaction.response.send_message(
            f"❌ Discord error: `{error}`",
            ephemeral=True,
        )


# ============================================================
# /mypermissions
# ============================================================

@bot.tree.command(
    name="mypermissions",
    description="Show which roles you are allowed to manage."
)
async def mypermissions(interaction: discord.Interaction):

    if not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message(
            "❌ Use this command inside the server.",
            ephemeral=True,
        )
        return

    allowed_roles = set()

    for manager_role_id in get_manager_roles(interaction.user):
        allowed_roles.update(
            PERMISSIONS[manager_role_id]
        )

    if not allowed_roles:
        await interaction.response.send_message(
            "❌ You do not have a configured management role.",
            ephemeral=True,
        )
        return

    role_mentions = []

    for role_id in sorted(allowed_roles):
        role = interaction.guild.get_role(role_id)

        if role:
            role_mentions.append(role.mention)

    embed = discord.Embed(
        title="Your Role Permissions",
        description=(
            "\n".join(f"• {role}" for role in role_mentions)
            if role_mentions
            else "No configured roles were found."
        ),
        color=discord.Color.blurple(),
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True,
    )


# ============================================================
# /roleinfo
# ============================================================

@bot.tree.command(
    name="roleinfo",
    description="Show which management roles can manage a role."
)
@app_commands.describe(
    role="Role to inspect"
)
async def roleinfo(
    interaction: discord.Interaction,
    role: discord.Role,
):

    managers = []

    for manager_role_id, target_roles in PERMISSIONS.items():

        if role.id in target_roles:

            manager_role = interaction.guild.get_role(
                manager_role_id
            )

            if manager_role:
                managers.append(
                    manager_role.mention
                )

    if managers:
        description = (
            "The following management roles can manage this role:\n\n"
            + "\n".join(
                f"• {manager}"
                for manager in managers
            )
        )
    else:
        description = (
            "No configured management role can manage this role."
        )

    embed = discord.Embed(
        title=f"Role Information — {role.name}",
        description=description,
        color=discord.Color.blurple(),
    )

    embed.add_field(
        name="Role ID",
        value=str(role.id),
        inline=False,
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True,
    )


# ============================================================
# START BOT
# ============================================================

bot.run(TOKEN)
