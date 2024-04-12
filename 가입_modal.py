import discord,requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
from database import *

class 가입_modal(discord.ui.Modal, title="계정 확인"):
    username = discord.ui.TextInput(label="백준 닉네임", placeholder="닉네임을 입력하세요.",required=True,max_length=200,style=discord.TextStyle.short)
    sourcecode_url = discord.ui.TextInput(label="소스코드 주소", placeholder="사이트 주소를 입력해주세요.",required=True,max_length=200,style=discord.TextStyle.short)
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
    async def on_submit(self, interaction: discord.Interaction):
        dbase = sqlite3.connect("user_data.db")
        url = f"{self.sourcecode_url}"
        discord_id = interaction.user.id
        url2 = f"https://www.acmicpc.net/status?problem_id=1000&user_id={self.username}"
        cnt = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
        cnt2 = requests.get(url2,headers={"User-Agent":"Mozilla/5.0"})
        # print(cnt.content.decode('utf-8'))
        soup = BeautifulSoup(cnt.text, "lxml")
        soup2 = BeautifulSoup(cnt2.text,"lxml")
        # print(soup.find('h1',attrs={"class":"pull-left"}).a.attrs['href'][9:])
        time = soup2.find('a',attrs={"class":"real-time-update show-date"}).attrs["title"]
        print(time)
        datetime_object = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        diff = datetime.now()-datetime_object
        # print(time)
        cur = int(soup.find('h1',attrs={"class":"pull-left"}).a.attrs['href'][9:])
        username = soup.find('ul',attrs={"class":"pull-right breadcrumb"}).get_text()
        print(int(diff.seconds))
        username = username.strip()
        self.username = str(self.username).strip()
        # print(soup.textarea.get_text())
        # print(cur)
        # print(len(username))
        # print(len(self.username))
        if cur == 1000 and soup.textarea.get_text() == "hello 피랜디봇" and username == self.username and int(diff.seconds) <= 300:
            if find_Data(username) == False:
                insert_record(discord_id,username,800)
                dbase.execute(''' CREATE TABLE IF NOT EXISTS discord_user_id(  
                    ID INT PRIMARY KEY NOT NULL,
                    NAME TEXT NOT NULL,
                    RATING INT NOT NULL) ''')

                pp = username
                dbase.execute(f"CREATE TABLE IF NOT EXISTS {pp} (  DATE TEXT NOT NULL, RATING INT NOT NULL)")
                date2 = datetime.now()
                dbase.execute(f"INSERT INTO {pp} (DATE,RATING) VALUES(?,?)",(date2.strftime("%Y-%m-%d %H:%M:%S"),800))
                dbase.execute(f"SELECT * , rowid AS rowid FROM {pp};")
                dbase.commit()
                await interaction.response.send_message(f"{interaction.user.mention} 인증이 완료되었습니다.")
            else:
                await interaction.response.send_message(f"{interaction.user.mention} 이미 가입된 상태입니다.")
            
        else:
            await interaction.response.send_message(f"{interaction.user.mention} 인증에 실패했습니다.")
        
        await interaction.channel.send(f"소스코드 주소: {self.sourcecode_url}")

    async def on_timeout(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} 시간이 초과되었습니다.")

