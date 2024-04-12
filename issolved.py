import discord
import requests
import json
import button_variable
async def issolved(name : str, problem : int):
    url = f"https://solved.ac/api/v3/search/problem?query=id%3A{problem}+solved_by%3A{name}"
    cnt = requests.get(url)
    pages = int(json.loads(cnt.content.decode("utf-8")).get("count"))
    if pages > 0:
        return 1
    else:
        return 0
    

async def finish_confirm():
    return 1
async def finish(channel : discord.Interaction.channel):
    button_variable.over = 1
    await channel.send(f"랜디가 종료되었습니다!")
    if button_variable.problem_len == button_variable.solved_cnt:
        await channel.send(f"{button_variable.solved_cnt}개 문제를 다 풀으셨군요! 축하합니다!")
        # await channel.send(f"새로운 레이팅을 반영 중 입니다...")
    else:
        await channel.send(f"{button_variable.solved_cnt}개 문제를 풀으셨군요! 축하합니다!")
    
    return await finish_confirm()