import requests
import discord,asyncio
from discord.ui import Button, View
from issolved import *
import sqlite3
from datetime import datetime
import button_variable
class custom_button(discord.ui.Button):
    def __init__(self, label, style, custom_id):
            super().__init__(label=label, style=style, custom_id=custom_id)  # set label and super init class

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        dbase = sqlite3.connect("user_data.db")
        t1 = dbase.execute(''' SELECT NAME FROM discord_user_id WHERE ID = (?)''',(interaction.user.id,))
        user_name = t1.fetchall()[0][0]
        global timer,over,checking_button,start_user
        if button_variable.checking_button == 1:
            await interaction.channel.send("다른 작업이 진행중입니다.")
            return
        if button_variable.start_user != interaction.user.id:
            await interaction.channel.send(f"{interaction.user.mention} 누군가 랜디를 진행중입니다.")
            return
        button_variable.checking_button = 1
        if button_variable.over == 1:
            await interaction.channel.send("이미 끝난 랜디입니다.") 
            return
        if interaction.data['custom_id'].startswith('time_remain'):
            # print(interaction.data['custom_id'][12:], str(datetime.now()))
            temp = interaction.data['custom_id'][12:]
            datetime_object = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
            print(datetime_object)
            print(datetime.now())
            diff = datetime.now()-datetime_object
            print(int(diff.seconds))
            await interaction.channel.send(f"남은 시간은 {(timer - int(diff.seconds)) // 3600}시간 {((timer - int(diff.seconds)) % 3600) // 60}분 {(timer - int(diff.seconds)) % 60}초 입니다.")
        elif interaction.data['custom_id'] == '끝내기':
            await finish(interaction.channel)
            self.disabled = True  # disable button  
            await interaction.message.edit(view=self.view)  # update message

        elif (await issolved(user_name, interaction.data['custom_id'])) == 1:
            cur = interaction.data['custom_id']
            self.disabled = True  # disable button  
            url7 = f"https://solved.ac/api/v3/search/problem?query=id%3A{cur}"
            cnt = requests.get(url7)
            real = json.loads(cnt.content.decode('utf-8')).get("items")
            print(real[0].get("level"))
            button_variable.calclutier += real[0].get("level")
            await interaction.message.edit(view=self.view)  # update message
            await interaction.channel.send(f"축하합니다! {cur}번 문제를 맞히셨습니다!") 
            # dbase.execute(f"INSERT INTO {user_name}_report(DATE,PROBLEM1,PROBLEM2,PROBLEM3,SOLVED1,) VALUES(?,?,?)",(ID,NAME,RATING))
            # dbase.commit()
            button_variable.solved_cnt += 1
            if button_variable.problem_len == button_variable.solved_cnt:
                await finish(interaction.channel)

        else:
            await interaction.channel.send("문제를 푼 후에 클릭해주세요.")
        button_variable.checking_button = 0