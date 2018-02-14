import requests
from bs4 import BeautifulSoup
import pandas
import sqlite3




def connect():
    conn=sqlite3.connect("forecast_web.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS forecast (id INTEGER PRIMARY KEY, dates text, times text, waves text, degree text)")
    conn.commit()
    conn.close()
connect()

def insert(dates,times,waves,degree):
    conn = sqlite3.connect("forecast_web.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO forecast VALUES(NULL,?,?,?,?)",(dates,times,waves,degree))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("forecast_web.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM forecast")
    rows = cur.fetchall()
    return rows


def update(dates,times,waves,degree,id):
    conn = sqlite3.connect("forecast_web.db")
    cur = conn.cursor()
    cur.execute("UPDATE forecast SET dates = ?,times = ?, waves = ?,degree = ? WHERE id = ?",(dates,times,waves,degree,id))
    conn.commit()
    conn.close()


def delete(id):
    conn = sqlite3.connect("forecast_web.db")
    cur = conn.cursor()
    cur.execute("DELETE  FROM forecast WHERE  id> ? ",(id,))
    conn.commit()
    conn.close()



areas = {"ΑΓ.ΚΩΝ/ΝΟΣ - ΣΚΙΑΘΟΣ":"22","ΑΡΓΟΛΙΚΟΣ ΚΟΛΠΟΣ":"23","ΒΟΡ.ΑΝΑΤΟΛΙΚΟ ΑΙΓΑΙΟ":"4","ΒΟΡΕΙΟ ΙΟΝΙΟ":"15","ΗΓΟΥΜΕΝΙΤΣΑ - ΚΕΡΚΥΡΑ":"21","ΘΑΛΑΣΣΑ ΚΥΘΗΡΩΝ":"9"
,"ΘΑΛΑΣΣΑ ΡΟΔΟΥ":"13","ΘΡΑΚΙΚΟ ΠΕΛΑΓΟΣ":"1","ΚΑΡΠΑΘΙΟ":"12","ΚΕΡΑΜΩΤΗ - ΘΑΣΟΣ":"20","Ν. ΕΥΒΟΪΚΟΣ":"24","ΝΟΤΙΟ ΙΟΝΙΟ":"16","ΡΙΟ - ΑΝΤΙΡΡΙΟ":"19","ΑΝΑΤΟΛΙΚΟ ΚΡΗΤΙΚΟ":"11"
,"Β. ΕΥΒΟΪΚΟΣ":"25","ΒΟΡΕΙΟ ΑΙΓΑΙΟ":"3","ΔΥΤΙΚΟ ΚΡΗΤΙΚΟ":"10","ΘΑΛΑΣΣΑ ΚΑΣΤΕΛΟΡΙΖΟΥ":"14","ΘΑΛΑΣΣΑ ΚΩ":"8","ΘΕΡΜΑΪΚΟΣ ΚΟΛΠΟΣ":"2","ΚΑΒΟ ΝΤΟΡΟ":"26"
,"ΚΕΝΤΡΙΚΟ ΑΙΓΑΙΟ":"5","ΚΟΡΙΝΘΙΑΚΟΣ ΚΟΛΠΟΣ":"18","ΝΟΤ.ΑΝΑΤΟΛΙΚΟ ΑΙΓΑΙΟ":"7","ΝΟΤΙΟΔΥΤΙΚΟ ΑΙΓΑΙΟ":"6","ΣΑΡΩΝΙΚΟΣ ΚΟΛΠΟΣ":"17"}
choose_area = areas.get("ΑΓ.ΚΩΝ/ΝΟΣ - ΣΚΙΑΘΟΣ")
def select_area(x):
    global choose_area
    choose_area = areas.get(x)


    r = requests.get("http://www.meteo.gr/meteoplus/waves.cfm?Sea_id="+choose_area)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    all = soup.find_all("div",{"class":"wavesInfo"})


    l = []
    for item in all:
        for i in range(0,len(item.find_all("tr",{"class":"mod1"}))+len(item.find_all("tr",{"class":"mod0"}))):
            d = {}
            if i%2 ==0:
                w = "1"
                mod_1 = item.find_all("tr",{"class":"mod"+w})[int(i/2)]
                d["Waves"] = mod_1.find_all("td",{"class":"innerTableCell"})[3].text[0:3]
                d["Degrees"] = (mod_1.find_all("td",{"class":"innerTableCell"})[4].text)[0:3]
                d["Time"] = mod_1.find_all("td",{"class":"innerTableCell"})[1].text
                d["date"] = mod_1.find("span",{"class":"HeadG"}).text
                l.append(d)
                df = pandas.DataFrame(l)
                insert(d["date"],d["Time"],d["Waves"],d["Degrees"])
                update(d["date"],d["Time"],d["Waves"],d["Degrees"],i+1)


            else:
                w = "0"
                mod_2 = item.find_all("tr",{"class":"mod"+w})[int((i-1)/2)]
                d["Waves"] = mod_2.find_all("td",{"class":"innerTableCell"})[3].text[0:3]
                d["Degrees"] = mod_2.find_all("td",{"class":"innerTableCell"})[4].text[0:3]
                d["Time"] = mod_2.find_all("td",{"class":"innerTableCell"})[1].text
                d["date"] = mod_2.find("span",{"class":"HeadG"}).text
                l.append(d)
                df = pandas.DataFrame(l)
                insert(d["date"],d["Time"],d["Waves"],d["Degrees"])
                update(d["date"],d["Time"],d["Waves"],d["Degrees"],i+1)
            global data
            data = df





    delete(len(item.find_all("tr",{"class":"mod1"}))+len(item.find_all("tr",{"class":"mod0"})))


def export():
    data.to_csv("forecast.csv")
