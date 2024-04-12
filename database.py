import sqlite3

def insert_record(ID, NAME, RATING):
    dbase = sqlite3.connect("user_data.db")
    dbase.execute(''' INSERT INTO discord_user_id(ID,NAME,RATING) 
            VALUES(?,?,?) ''',(ID,NAME,RATING))
    dbase.commit()

def find_Data(find):
    dbase = sqlite3.connect("user_data.db")
    data = dbase.execute(''' SELECT ID FROM discord_user_id WHERE NAME = (?) ''',(find,))
    x = data.fetchall()
    print(x)
    if x == []:
        return False
    else:
        return True
def read_Data():
    dbase = sqlite3.connect("user_data.db")
    data = dbase.execute(''' SELECT ID, NAME FROM employee_records ''')
    for record in data:
        print(f"ID:{record[0]} NAME:{record[1]} DIVISION:{record[2]} STARS:{record[3]}")

# read_Data()

def update_record():
    dbase = sqlite3.connect("user_data.db")
    dbase.execute(''' UPDATE discord_user_id set DIVISION='eletronics' WHERE ID=1 ''')
    dbase.commit()
# update_record()

def delete_record():
    dbase = sqlite3.connect("user_data.db")
    dbase.execute(''' DELETE from discord_user_id WHERE ID = 1 ''')
    dbase.commit()