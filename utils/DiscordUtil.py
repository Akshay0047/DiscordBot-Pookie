import configs.DefaultConfig as defaultConfig

def is_me(ctx):
    return ctx.author.id == int(defaultConfig.DISCORD_OWNER_ID)
