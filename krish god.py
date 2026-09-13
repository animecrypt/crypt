import discord
from discord.ext import commands

# ==============================
# ROLE IDs
# ==============================

ROLES = {
    "management": 1544962832184119386,

    "level 50": 1545279664082255883,
    "level 40": 1545279492912844912,
    "level 30": 1545279359231983646,
    "level 20": 1545279227236974683,
    "level 10": 1545279034680680488,
    "level 5": 1545278882616180746,

    "divas": 1545546903360512120,
    "monarchs": 1545697705345421313,
    "kitten": 1545546997090750555,
    "artist": 1544962843802345512,
    "imperial alpha": 1548537294967935078,
    "melodist": 1544962844984872980,
    "moon beam maidan": 1545546500933689454,
    "mistic warden": 1546068438475079730,
    "prettiest apsara": 1545546815707807774,
    "warriors": 1548530578343600238,
    "over seers": 1546068303296856134,
    "the sinister one": 1546068900695777290,
    "hawties": 1545546654005076059,
    "ivory": 1548537480943247430,
    "infinite resonance": 1546068248443752478,
    "spotify": 1545521005617881229,
    "scarlet witch": 1545546442939047956,
    "the luminaries": 1546068160229285909,
    "snow princess": 1545546343513325670,
    "spiderman": 1547711437693124732,
    "commander": 1546068384473550908,

    "vc help": 1546591858145235004,
    "ticket admin": 1545145899725103144,

    "hangout manager": 1548241328490414191,
    "gaming manager": 1548241961104834682,
    "singing manager": 1548240879804874752,

    "head hangout mod": 1548226719167807528,
    "head gaming mod": 1548226503949418648,
    "head singing mod": 1548225761767465000,

    "hangout mod": 1545047689329115136,
    "gaming mod": 1545046367137964125,
    "singing mod": 1544962834767675412,

    "junior hangout mod": 1548226826998906920,
    "junior gaming mod": 1548226617254354994,
    "junior singing mod": 1548226374119063562,
}


# ==============================
# WHO CAN GIVE WHICH ROLES
# ==============================

ROLE_PERMISSIONS = {

    # Management can give EVERYTHING
    "management": set(ROLES.keys()),

    # Hangout Manager
    "hangout manager": {
        "head hangout mod",
        "hangout mod",
        "junior hangout mod",
    },

    # Gaming Manager
    "gaming manager": {
        "head gaming mod",
        "gaming mod",
        "junior gaming mod",
    },

    # Singing Manager
    "singing manager": {
        "head singing mod",
        "singing mod",
        "junior singing mod",
        "artist",
        "melodist",
        "spotify",
    },

    # Head Hangout Mod
    "head hangout mod": {
        "hangout mod",
        "junior hangout mod",
    },

    # Head Gaming Mod
    "head gaming mod": {
        "gaming mod",
        "junior gaming mod",
    },

    # Head Singing Mod
    "head singing mod": {
        "singing mod",
        "junior singing mod",
        "artist",
        "melodist",
        "spotify",
    },

    # Singing Mod
    "singing mod": {
        "artist",
        "melodist",
        "spotify",
    },
}


# ==============================
# HELPER: GET STAFF AUTHORITY
# ==============================

def get_authorized_roles(member):

    authorized = []

    for role in member.roles:
        role_name = role.name.lower()

        if role_name in ROLE_PERMISSIONS:
            authorized.append(role_name)

    return authorized


# ==============================
# GIVE ROLE
# ==============================

@bot.command(name="give")
async def give_role(ctx, member: discord.Member, *, role_name: str):

    role_name = role_name.lower().strip()

    # Check whether role exists
    if role_name not in ROLES:
        await ctx.send(
            f"❌ **Role not found.**\n"
            f"`{role_name}` is not a valid role."
        )
        return

    # Find the actual Discord role
    role = ctx.guild.get_role(ROLES[role_name])

    if role is None:
        await ctx.send("❌ I couldn't find that role in this server.")
        return

    # Prevent giving @everyone
    if role.is_default():
        await ctx.send("❌ You cannot give the @everyone role.")
        return

    # Check permissions
    authorized_roles = get_authorized_roles(ctx.author)

    if not authorized_roles:
        await ctx.send(
            "❌ **You are not authorized to use this command.**"
        )
        return

    allowed = False

    for staff_role in authorized_roles:
        if role_name in ROLE_PERMISSIONS[staff_role]:
            allowed = True
            break

    if not allowed:
        await ctx.send(
            f"❌ You cannot give the **{role.name}** role."
        )
        return

    # Bot role hierarchy check
    if role >= ctx.guild.me.top_role:
        await ctx.send(
            "❌ I cannot give this role because it is higher than "
            "or equal to my highest role."
        )
        return

    # Check if user already has role
    if role in member.roles:
        await ctx.send(
            f"⚠️ {member.mention} already has **{role.name}**."
        )
        return

    # Give role
    try:
        await member.add_roles(role)

        await ctx.send(
            f"✅ **Role Given**\n"
            f"👤 Member: {member.mention}\n"
            f"🎭 Role: **{role.name}**\n"
            f"🛡️ Given by: {ctx.author.mention}"
        )

    except discord.Forbidden:
        await ctx.send(
            "❌ I don't have permission to give this role."
        )


# ==============================
# REMOVE ROLE
# ==============================

@bot.command(name="remove")
async def remove_role(ctx, member: discord.Member, *, role_name: str):

    role_name = role_name.lower().strip()

    # Check whether role exists
    if role_name not in ROLES:
        await ctx.send(
            f"❌ **Role not found.**\n"
            f"`{role_name}` is not a valid role."
        )
        return

    # Find Discord role
    role = ctx.guild.get_role(ROLES[role_name])

    if role is None:
        await ctx.send("❌ I couldn't find that role in this server.")
        return

    # Check permissions
    authorized_roles = get_authorized_roles(ctx.author)

    if not authorized_roles:
        await ctx.send(
            "❌ **You are not authorized to use this command.**"
        )
        return

    allowed = False

    for staff_role in authorized_roles:
        if role_name in ROLE_PERMISSIONS[staff_role]:
            allowed = True
            break

    if not allowed:
        await ctx.send(
            f"❌ You cannot remove the **{role.name}** role."
        )
        return

    # Bot hierarchy check
    if role >= ctx.guild.me.top_role:
        await ctx.send(
            "❌ I cannot remove this role because it is higher than "
            "or equal to my highest role."
        )
        return

    # Check if user has role
    if role not in member.roles:
        await ctx.send(
            f"⚠️ {member.mention} doesn't have **{role.name}**."
        )
        return

    # Remove role
    try:
        await member.remove_roles(role)

        await ctx.send(
            f"✅ **Role Removed**\n"
            f"👤 Member: {member.mention}\n"
            f"🎭 Role: **{role.name}**\n"
            f"🛡️ Removed by: {ctx.author.mention}"
        )

    except discord.Forbidden:
        await ctx.send(
            "❌ I don't have permission to remove this role."
        )


# ==============================
# ROLE HELP
# ==============================

@bot.command(name="rolehelp")
async def role_help(ctx):

    await ctx.send(
        "**🎭 ROLE MANAGEMENT**\n\n"
        "`!give @user Role Name`\n"
        "Give an authorized role.\n\n"
        "`!remove @user Role Name`\n"
        "Remove an authorized role.\n\n"
        "**Examples:**\n"
        "`!give @User Artist`\n"
        "`!remove @User Artist`\n"
        "`!give @User Singing Mod`\n"
        "`!remove @User Spotify`"
    )
