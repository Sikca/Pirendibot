import discord,asyncio
import sqlite3
async def check(interaction : discord.Interaction, prev_rating : int, rating : int, user_name : str):
    channel = interaction.channel
    dbase = sqlite3.connect("user_data.db")
    global ans_rate
    if prev_rating < rating:
        await channel.send(f"{interaction.user.mention}님 축하합니다!")
        await channel.send(f"{user_name} 님의 레이팅이 +{(prev_rating+rating)/2-prev_rating} 상승했습니다. {prev_rating} -> {int((prev_rating+rating)/2)}")
        dbase.execute(f"UPDATE discord_user_id set RATING={int((prev_rating+rating)/2)} WHERE ID={interaction.user.id}")
        dbase.commit()
        ans_rate = int((prev_rating+rating)/2)
    elif prev_rating > rating:
        await channel.send(f"{interaction.user.mention} 아... 아쉽네요.")
        await channel.send(f"{user_name} 님의 레이팅이 -{prev_rating - (prev_rating+rating)/2} 감소했습니다. {prev_rating} -> {int((prev_rating+rating)/2)}")
        dbase.execute(f"UPDATE discord_user_id set RATING={int((prev_rating+rating)/2)} WHERE ID={interaction.user.id}")
        dbase.commit()
        ans_rate = int((prev_rating+rating)/2)
    else:
        await channel.send(f"{interaction.user.mention} 다행히 떨어지진 않았네요!")
        await channel.send(f"{user_name} 님의 레이팅이 그대로 유지됩니다. {prev_rating} -> {prev_rating}")
        ans_rate = prev_rating
    return ans_rate
