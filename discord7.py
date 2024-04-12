import discord,asyncio
from discord import app_commands
from discord.ui import Button, View
from datetime import datetime
import rating변환test
import sqlite3
import requests
import json
import random
import graph_maker, rating_check
from database import *
from issolved import *
import button_variable
from custom_button import *
from 가입_modal import *
dbase = sqlite3.connect("user_data.db")

token = ""

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
event = asyncio.Event() # 다 풀었을 경우 종료 이벤트
userdatabase = []
global playing, log
notplaying = 1
log = False
@client.event
async def on_ready():
    await tree.sync()
    print("봇 준비 완료!")
    print(client.user)
    print("===================")

async def isnogame():
    global notplaying
    if notplaying == 1:
        return True
    else:
        return False

@tree.command(name='도움말',description='피랜디봇을 이용하기 위한 가이드 설명')
async def slash2(interaction: discord.Interaction):
    embed = discord.Embed(colour=discord.Colour.green(),title="피랜디봇 사용가이드",description="피랜디봇은 랜덤디펜스를 통한 실전 실력을 필요로 합니다.")
    embed.add_field(name="",value="랜덤디펜스를 통한 레이팅 시스템이 존재하며 레이팅 상승이 가능합니다. 레이팅은 푼문제의 난이도와 걸린시간을 이용해 계산합니다.",inline=False)
    embed.add_field(name="/내정보",value="자신의 정보를 보여줍니다.",inline=False)
    embed.add_field(name="/정보 (닉네임)",value="유저의 정보를 보여줍니다.",inline=False)
    embed.add_field(name="/도움말",value="피랜디봇 사용가이드를 설명합니다.",inline=False)
    embed.add_field(name="/랭킹 (페이지)",value="현재 레이팅 순위를 보여줍니다.",inline=False)
    embed.add_field(name="/랜디시작 (난이도:브론즈,실버,골드,플레티넘)",value="난이도의 문제 3개를 랜덤으로 뽑아 디펜스를 진행합니다.(제한시간2시간),(레이팅변동O)",inline=False)
    embed.add_field(name="/연습랜디시작 (query) (문제수) (제한시간초단위)",value="쿼리에 맞는 문제를 랜덤으로 문제수 만큼 생성하여 연습게임을 진행합니다.(레이팅변동X)",inline=False)
    embed.add_field(name="/기록 (닉네임)",value="해당유저의 랜디기록을 보여줍니다.",inline=False)

    await interaction.response.send_message(embed=embed)

    

# global calclutier,checking_button
# calclutier = 0  
# checking_button = 0



async def register(interaction : discord.Interaction):
    await interaction.channel.send(f"{interaction.user.mention} 백준 닉네임을 작성하고 5분 이내에 백준 1000번 문제에 'hello 피랜디봇'을 제출 후, 제출한 소스코드를 공유 버튼을 눌러 공유한 url주소를 입력 후 수락 버튼을 눌러주시기 바랍니다.")
    await interaction.response.send_modal(가입_modal(timeout=300))
    



async def checking():
    while button_variable.over != 1:
        await asyncio.sleep(1)
    return True

async def practice_problem_up(interaction : discord.Interaction, final_list : list, diction : dict, 제한시간초단위 : int, isranked : bool):
    global timer
    button_variable.start_user = interaction.user.id
    timer = 제한시간초단위
    channel = interaction.channel
    await channel.send("각 문제를 풀었으면 체크 버튼을 눌러주세요.")
    if isranked == True:
        embed = discord.Embed(colour=discord.Colour.red(),title=f"랜디 'Rated' ")
    else:
        embed = discord.Embed(colour=discord.Colour.red(),title=f"사용자지정 랜덤 디펜스 연습")
    await channel.send(embed=embed)
    global notplaying
    button_variable.solved_cnt = 0
    button_variable.over = 0
    global start_time
    button_variable.problem_len = len(final_list)
    button_variable.calclutier = 0
    view = View()
    button1 = 0
    button2 = 0
    for i in final_list:
        embed2 = discord.Embed(colour=discord.Colour.red(),title=f"{i}",description=diction[i], url=f"https://www.acmicpc.net/problem/{i}")
        embed2.add_field(name="",value="",inline=False)
        button = custom_button(label=f"{i}번 해결완료!",style=discord.ButtonStyle.green, custom_id=str(i))
        view = View(timeout=timer)
        view.add_item(button)
        if i == final_list[-1]:
            global start_time
            cur = datetime.now()
            start_time = cur
            button1 = custom_button(label="남은시간확인",style=discord.ButtonStyle.red, custom_id=f'time_remain {cur}')
            button2 = custom_button(label="끝내기",style=discord.ButtonStyle.red, custom_id=f'끝내기')
            view.add_item(button1)
            view.add_item(button2)
        await channel.send(embed=embed2,view=view)
    try:
        await asyncio.wait_for(checking(),timeout=timer)
    except asyncio.TimeoutError:
        await finish(channel)
    await channel.send("Worked!")
    if isranked == True:
        print(button_variable.calclutier)
        diff = datetime.now()-start_time
        if button_variable.solved_cnt > 0:
            rating = int(rating변환test.rating_check(button_variable.calclutier/button_variable.solved_cnt, int(diff.seconds)/button_variable.solved_cnt))
        else:
            rating = int(rating변환test.rating_check(button_variable.calclutier, int(diff.seconds)))
        await channel.send("레이팅을 반영중입니다!")
        await asyncio.sleep(2)
        t1 = dbase.execute(''' SELECT NAME FROM discord_user_id WHERE ID = (?)''',(interaction.user.id,))
        user_name = t1.fetchall()[0][0]
        print(user_name)
        t2 = dbase.execute(''' SELECT RATING FROM discord_user_id WHERE ID = (?)''',(interaction.user.id,))
        prev_rating = t2.fetchall()[0][0]
        print(prev_rating)
        global ans_rate
        ans_rate = 0
        ans_rate = await rating_check.check(interaction, prev_rating, rating, user_name)
        date2 = datetime.now()
        dbase.execute(f"INSERT INTO {user_name} (DATE,RATING) VALUES(?,?)",(date2.strftime("%Y-%m-%d %H:%M:%S"),ans_rate))
        dbase.commit()
        solved_list = [0,0,0]
        for i in range(0,3):
            if await issolved(user_name,final_list[i]) == 1:
                solved_list[i] = 1

        global p_DIFFICULTY
        dbase.execute(f"CREATE TABLE IF NOT EXISTS {user_name}_report(  DATE TEXT NOT NULL,PROBLEM1 INT NOT NULL,PROBLEM2 INT NOT NULL,PROBLEM3 INT NOT NULL,SOLVED1 INT NOT NULL,SOLVED2 INT NOT NULL,SOLVED3 INT NOT NULL,TIME INT NOT NULL,RATE INT NOT NULL,DIFFICULTY TEXT NOT NULL)")
        dbase.execute(f"INSERT INTO {user_name}_report(DATE,PROBLEM1,PROBLEM2,PROBLEM3,SOLVED1,SOLVED2,SOLVED3,TIME,RATE,DIFFICULTY) VALUES(?,?,?,?,?,?,?,?,?,?)",(date2.strftime("%Y-%m-%d %H:%M:%S"),final_list[0],final_list[1],final_list[2],solved_list[0],solved_list[1],solved_list[2],int(diff.seconds),int((prev_rating+rating)/2-prev_rating),p_DIFFICULTY))
        dbase.commit()
        await channel.send(f"퍼포먼스는 {rating} 입니다!")
        button_variable.calclutier = 0



    notplaying = 1
    
    # if solvedcnt == problems_len:
    #     await channel.send(f"{solvedcnt}개 문제를 다 풀으셨군요! 축하합니다!")
    # else:
    #     await channel.send(f"{solvedcnt}개 문제를 다 풀으셨군요! 축하합니다!")
    # await channel.send(f"새로운 레이팅을 반영 중 입니다...")
    # 레이팅 반영 코드
    # 레이팅 계산
        # if i == final_list[-1]:
        #     await channel.send(embed=embed2,view=view)
        # else:
        #     await channel.send(embed=embed2)


@tree.command(name='랜디시작',description='난이도(브론즈,실버,골드,플레티넘)')
async def slash3(interaction: discord.Interaction, 난이도 : str):
    data = dbase.execute(''' SELECT NAME FROM discord_user_id WHERE ID = (?)''',(interaction.user.id,))
    x = data.fetchall()
    user_name = x[0][0]
    if x == []:
        await interaction.response.send_message("'/가입' 을 통하여 계정인증을 해주시기 바랍니다.")
        return
    if await isnogame() == False:
        await interaction.response.send_message(f"{interaction.user.mention} 이미 진행중인 게임이 있습니다.")
        return
    tier = {"브론즈":"b", "실버":"s", "골드":"g", "플레티넘":"p"}
    if 난이도 not in tier.keys():
        await interaction.response.send_message(f"올바른 명령어를 입력해주세요.")
        return
    global notplaying
    notplaying = 0
    channel = interaction.channel
    await interaction.response.send_message(f"{interaction.user.mention}님이 {난이도} 랜디를 시작합니다.")
    print(user_name)
    url = f"https://solved.ac/api/v3/search/problem?query=*{tier[난이도]}+%21solved_by%3A{user_name}+solved%3A50..+%25ko&sort=random"
    cnt = requests.get(url)
    pages = int(json.loads(cnt.content.decode("utf-8")).get("count"))
    if pages < 3:
        await channel.send(f"풀 수 있는 문제수가 부족하거나 없습니다.")
        return
    pages = (pages-1) // 50 + 1
    diction = dict()
    final_list = []
    for i in range(0,3):
        page = random.randint(1,pages)
        page_url = f"{url}&page={page}"
        cnt = requests.get(page_url)
        problems = json.loads(cnt.content.decode("utf-8")).get("items")
        # problems_list.extend([pro.get("problemId")for pro in problems])
        for pro in problems:
            diction.update({int(pro.get("problemId")):pro.get("titleKo")})
    final_list = random.sample(list(diction.keys()),3)
    print(final_list)
    date2 = datetime.now()

    
    date2.strftime("%Y-%m-%d %H:%M:%S")
    global p_DIFFICULTY
    p_DIFFICULTY = 난이도
    await practice_problem_up(interaction, final_list, diction, 7200, True)


@tree.command(name='연습랜디시작',description='(query) (문제수)')
async def slash4(interaction: discord.Interaction, query : str, 문제수 : int, 제한시간초단위 : int):
    data = dbase.execute(''' SELECT NAME FROM discord_user_id WHERE ID = (?)''',(interaction.user.id,))
    x = data.fetchall()
    if x == []:
        await interaction.channel.send("'/가입' 을 통하여 계정인증을 해주시기 바랍니다.")
        return
    if await isnogame() == False:
        await interaction.channel.send(f"{interaction.user.mention} 이미 진행중인 게임이 있습니다.")
        return
    global notplaying
    notplaying = 0
    channel = interaction.channel
    cur = 0
    if 문제수 >= 1:
        await channel.send(f"{interaction.user.mention}님이 query : {query} 연습랜디를 시작합니다.")
        url = "https://solved.ac/api/v3/search/problem"

        querystring = {"query":query,"page":"1","sort":"random"}

        headers = {"Accept": "application/json"}
        print(query)
        cnt = requests.get(url, headers=headers, params=querystring)

        print(cnt.content.decode("utf-8"))

        pages = int(json.loads(cnt.content.decode("utf-8")).get("count"))
        print(pages)
        if pages < 문제수:
            await channel.send(f"풀 수 있는 문제수가 부족하거나 잘못된 쿼리 입력입니다.")
            return
        diction = dict()
        final_list = []
        pages = (pages-1) // 50 + 1
        print(query)
        for i in range(0,문제수):
            page = random.randint(1,pages)
            url = "https://solved.ac/api/v3/search/problem"
            querystring = {"query":query,"page":f"{page}","sort":"random"}
            headers = {"Accept": "application/json"}
            cnt = requests.get(url, headers=headers, params=querystring)
            problems = json.loads(cnt.content.decode("utf-8")).get("items")
            for pro in problems:
                diction.update({int(pro.get("problemId")):pro.get("titleKo")})
            # print(f"{page} 페이지")
            # print(cnt.content.decode("utf-8"))
        final_list = random.sample(list(diction.keys()),문제수)
        print(final_list)
        await practice_problem_up(interaction, final_list, diction, 제한시간초단위, False)
        
    else:
        await channel.send(f"올바른 명령어를 입력해주세요.")

@tree.command(name='가입',description='.')
async def slash5(interaction: discord.Interaction):
    data = dbase.execute(''' SELECT NAME FROM discord_user_id WHERE ID = (?)''',(interaction.user.id,))
    x = data.fetchall()
    if x != []:
        await interaction.response.send_message(f"{interaction.user.mention} 이미 가입을 하셨습니다.")
        return
                                                                                 
    if await isnogame() == False:
        await interaction.response.send_message(f"{interaction.user.mention} 이미 진행중인 게임이 있습니다.")
        return
    await register(interaction)
@tree.command(name='정보',description='(닉네임) 특정 유저의 정보를 확인합니다.')
async def slash7(interaction: discord.Interaction, 유저 : str):
    data = dbase.execute(''' SELECT NAME FROM discord_user_id WHERE ID = (?)''',(interaction.user.id,))
    x = data.fetchall()
    if x == []:
        await interaction.channel.send("'/가입' 을 통하여 계정인증을 해주시기 바랍니다.")
        return
    date2 = dbase.execute(''' SELECT ID FROM discord_user_id WHERE NAME = (?) ''',(유저,))
    x2 = date2.fetchall()
    if x2 == []:
        await interaction.channel.send(f"{유저} 유저가 가입하지 않았습니다.")
        return
    date = dbase.execute(f"SELECT DATE,RATING FROM {유저}")
    date_real = date.fetchall()
    print(date_real)
    x = [] 
    y = [] 
    for i in date_real:
        x.append(i[0])
        y.append(i[1])
    cur = 0
    xx = 0
    yy = 0
    xlabels = []
    for i in x:
        xlabels.append(i[:10])
    for i in range(0,len(x)):
        if y[i] > cur:
            cur = y[i]
            xx = x[i]
            yy = y[i]
    graph_maker.make_graph(x,y,xx,yy,xlabels)
    url = f"https://solved.ac/api/v3/user/show?handle={유저}"
    cnt = requests.get(url)
    r = json.loads(cnt.content.decode('utf-8'))
    print(r)
    tt = r["profileImageUrl"]
    backgroundId = r["backgroundId"]
    url2 = f"https://solved.ac/api/v3/background/show?backgroundId={backgroundId}"
    cnt2 = requests.get(url2)
    r2 = json.loads(cnt2.content.decode("utf-8"))
    backgroundurl = r2["backgroundImageUrl"]
    image = discord.File("test.png")

    embed = discord.Embed(
        title=f"{유저} 정보",
        description=r["bio"],
        colour=discord.Colour.green()
    )
    embed.set_image(url="attachment://test.png")
    embed.set_thumbnail(url=f"{tt}")
    embed.add_field(name="solved.ac 순위",value=r["rank"],inline=True)
    embed.add_field(name="solved.ac 레이팅",value=r["rating"],inline=True)
    embed.add_field(name="클래스",value=r["class"],inline=True)
    embed.add_field(name="푼 문제수",value=r["solvedCount"],inline=True)
    data_rating = dbase.execute(f"SELECT RATING FROM discord_user_id WHERE NAME = (?)",(유저,))
    data_rating_real = data_rating.fetchall()[0][0]
    embed.add_field(name="랜디 레이팅",value=data_rating_real,inline=True)
    ran = dbase.execute("SELECT NAME,rank() OVER (ORDER BY RATING DESC) FROM discord_user_id")
    rank = ran.fetchall()
    temp = 0
    for i in rank:
        if i[0] == 유저:
            temp = i[1]
            break
    embed.add_field(name="랜디 순위",value=temp,inline=True)
    await interaction.response.send_message(backgroundurl)
    await interaction.channel.send(file=image, embed=embed)

@tree.command(name='내정보',description='자신의 정보를 확인합니다.')
async def slash8(interaction: discord.Interaction):
    data = dbase.execute(''' SELECT NAME FROM discord_user_id WHERE ID = (?)''',(interaction.user.id,))
    data_real = data.fetchall()
    me_name = data_real[0][0]
    print(data_real[0][0])
    if data_real == []:
        await interaction.response.send_message("'/가입' 을 통하여 계정인증을 해주시기 바랍니다.")
        return
    date = dbase.execute(f"SELECT DATE,RATING FROM {data_real[0][0]}")
    date_real = date.fetchall()
    print(date_real)
    x = [] 
    y = [] 
    for i in date_real:
        x.append(i[0])
        y.append(i[1])
    cur = 0
    xx = 0
    yy = 0
    xlabels = []
    for i in x:
        xlabels.append(i[:10])
    for i in range(0,len(x)):
        if y[i] > cur:
            cur = y[i]
            xx = x[i]
            yy = y[i]
    graph_maker.make_graph(x,y,xx,yy,xlabels)
    url = f"https://solved.ac/api/v3/user/show?handle={data_real[0][0]}"
    cnt = requests.get(url)
    r = json.loads(cnt.content.decode('utf-8'))
    print(r)
    tt = r["profileImageUrl"]
    backgroundId = r["backgroundId"]
    url2 = f"https://solved.ac/api/v3/background/show?backgroundId={backgroundId}"
    cnt2 = requests.get(url2)
    r2 = json.loads(cnt2.content.decode("utf-8"))
    backgroundurl = r2["backgroundImageUrl"]
    image = discord.File("test.png")

    embed = discord.Embed(
        title=f"{data_real[0][0]} 정보",
        description=r["bio"],
        colour=discord.Colour.green()
    )
    embed.set_image(url="attachment://test.png")
    embed.set_thumbnail(url=f"{tt}")
    embed.add_field(name="solved.ac 순위",value=r["rank"],inline=True)
    embed.add_field(name="solved.ac 레이팅",value=r["rating"],inline=True)
    embed.add_field(name="클래스",value=r["class"],inline=True)
    embed.add_field(name="푼 문제수",value=r["solvedCount"],inline=True)
    data_rating = dbase.execute(f"SELECT RATING FROM discord_user_id WHERE NAME = (?)",(me_name,))
    data_rating_real = data_rating.fetchall()[0][0]
    embed.add_field(name="랜디 레이팅",value=data_rating_real,inline=True)
    ran = dbase.execute("SELECT NAME,rank() OVER (ORDER BY RATING DESC) FROM discord_user_id")
    rank = ran.fetchall()
    temp = 0
    for i in rank:
        if i[0] == me_name:
            temp = i[1]
            break
    embed.add_field(name="랜디 순위",value=temp,inline=True)
    await interaction.response.send_message(backgroundurl)
    await interaction.channel.send(file=image, embed=embed)


@tree.command(name='랭킹',description='(페이지) 유저들의 랭킹순위를 확인합니다.')
async def slash9(interaction: discord.Interaction, 페이지 : int):
    ran = dbase.execute(f"SELECT NAME,RATING, rank() OVER (ORDER BY RATING DESC) FROM discord_user_id")
    rank = ran.fetchall()
    print(rank)
    if (len(rank)-1)//50+1 < 페이지:
        await interaction.response.send_message(f"{interaction.user.mention} 페이지가 없습니다.")
        return
    page = (len(rank)-1)//50+1
    embed = discord.Embed(colour=discord.Colour.red(),title="유저랭킹순위")
    for i in range(50*페이지-50,min(50*페이지,len(rank))):
        embed.add_field(name=f"{rank[i][2]}. {rank[i][0]} 레이팅: {rank[i][1]}",value="", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name='기록',description='(유저) 유저들의 랜디기록을 확인합니다.')
async def slash10(interaction: discord.Interaction, 유저 : str, 페이지 : int):
    user_name = 유저
    data = dbase.execute(f"SELECT DATE,PROBLEM1,PROBLEM2,PROBLEM3,SOLVED1,SOLVED2,SOLVED3,TIME,RATE,DIFFICULTY FROM {user_name}_report")
    date_real = data.fetchall()
    embed = discord.Embed(title=f"{유저} 랜디기록",color=discord.Colour.green())
    pages = (len(date_real)-1) // 50+1
    if pages < 페이지:
        await interaction.response.send_message(f"{interaction.user.mention} 페이지가 없습니다.")
        return
    for i in range(50*페이지-50,min(50*페이지,len(date_real))):
        p1 = f"<:white_check_mark:1227655753779646635>" if date_real[i][4] == 1 else f"<:x:1227658231535636570>"
        p2 = f"<:white_check_mark:1227655753779646635>" if date_real[i][5] == 1 else f"<:x:1227658231535636570>"
        p3 = f"<:white_check_mark:1227655753779646635>" if date_real[i][6] == 1 else f"<:x:1227658231535636570>"
        diff = date_real[i][7]
        embed.add_field(name=f"{date_real[i][0][:10]}  {date_real[i][1]}번: {p1}   {date_real[i][2]}번: {p2}   {date_real[i][3]}번: {p3}",value=" ",inline=False)
        embed.add_field(name=f"걸린시간: {diff // 3600}시간 {(diff % 3600) // 60}분 {diff % 60}초  난이도: {date_real[i][9]}  레이팅: {date_real[i][8]}",value=" ",inline=False)
    await interaction.response.send_message(embed=embed)
    
client.run(token)