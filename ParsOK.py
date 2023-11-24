from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import date
from datetime import datetime
import requests
import sqlite3



#Создаём СУБД
conn = sqlite3.connect("okDBSM.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    link TEXT,
    name TEXT
    )""")
conn.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY,
    link TEXT,
    date TEXT,
    text TEXT,
    cnt_comments INTEGER,
    cnt_likes INTEGER,
    id_group INTEGER,
    FOREIGN KEY (id_group) REFERENCES groups (id)
    )""")
conn.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    link TEXT,
    name TEXT
    )""")
conn.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS comments(
    id INTEGER PRIMARY KEY,
    date DATE,
    text TEXT,
    id_post INTEGER,
    id_user INTEGER,
    FOREIGN KEY (id_post) REFERENCES posts (id),
    FOREIGN KEY (id_user) REFERENCES users (id)
    )""")
conn.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS media(
    id INTEGER PRIMARY KEY,
    file_link TEXT,
    file_type TEXT,
    id_post INTEGER,
    FOREIGN KEY (id_post) REFERENCES posts (id)
    )""")
conn.commit()



#Функции, записывающие данные по столбцам таблиц СУБД
def insert_groups(id, link, name):
    cur.execute("INSERT INTO groups VALUES (?,?,?)", (id,link,name))
    conn.commit()

def insert_posts(id, link, date, text_post, cnt_comments, cnt_likes, id_group):
    cur.execute("INSERT INTO posts VALUES (?,?,?,?,?,?,?)", (id, link, date, text_post, cnt_comments, cnt_likes, id_group))
    conn.commit()

def insert_users(id, link, name):
    cur.execute("INSERT INTO users VALUES (?,?,?)", (id, link, name))
    conn.commit()

def insert_comments(id, date, text, id_post, id_user):
    cur.execute("INSERT INTO comments VALUES (?,?,?,?,?)", (id,date,text,id_post,id_user))
    conn.commit()

def insert_media(id,file_link,file_type,id_post):
    cur.execute("INSERT INTO media VALUES (?,?,?,?)", (id,file_link,file_type,id_post))
    conn.commit()


#Эту функция для даты поста
def postDate(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    meta_tag = soup.find("meta", {"itemprop": "datePublished"})

    if meta_tag:
        date_string = meta_tag["content"]
        #print (date_string)
        if len(date_string) == 29:
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
        elif len(date_string) == 25:
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
        else:
            return("DateError")
        formatted_date = date.strftime("%d.%m.%Y %H:%M:%S")
        return(formatted_date)
    else:
        return("DateError")

#Эта функция для даты комментария
def date_format(date_):
    s = date_.split()
    if len(s) == 1 or (len(s) == 2 and (s[0] == "вчера" or s[0] == "yesterday")):
        return date.today()
    else:
        day = int(s[0])
        months = {
            "янв": 1,
            "Jan": 1,
            "фев": 2,
            "Feb": 2,
            "марта": 3,
            "March": 3,
            "апр": 4,
            "Apr": 4,
            "мая": 5,
            "May": 5,
            "июн": 6,
            "Jun": 6,
            "июл": 7,
            "Jul": 7,
            "авг": 8,
            "Aug": 8,
            "сен": 9,
            "Sept": 9,
            "окт": 10,
            "Oct": 10,
            "ноя": 11,
            "Nov": 11,
            "дек": 12,
            "Dec": 12
        }
        month = months[s[1]]
        if len(s) == 2:
            year = date.today().year
        else:
            year = int(s[2])

        return date(year, month, day)

if __name__ == '__main__':
    post = int(input("Введите количество собранных постов с группы: "))


    #Через selenium определяем на каком сайте будем работать
    browser = wd.Chrome()
    browser.maximize_window()
    browser.get("https://ok.ru/dk?st.cmd=anonymMain&st.layer.cmd=PopLayerClose")
    time.sleep(1)

    #Через selenium авторизовываемся в аккаунт OK
    browser.find_element(By.NAME, "st.email").send_keys("login")
    browser.find_element(By.NAME,"st.password").send_keys("password")
    browser.find_element(By.NAME, "st.password").send_keys(Keys.ENTER)
    time.sleep(1)

    id_post = 1
    id_comment = 1
    id_media = 1
    id_user = 1
    
    allGroupsLink = ["","https://ok.ru/infomoscow24","https://ok.ru/vesti","https://ok.ru/spbsobakaru","https://ok.ru/buzuluksam","https://ok.ru/love.avto","https://ok.ru/glavdoroga","https://ok.ru/esports","https://ok.ru/dotaru","https://ok.ru/scinet","https://ok.ru/tinkoffbank"]
    allGroupsName = ["","Москва 24","ВЕСТИ","Собака.ru","Бузулук. Всё самое интересное.","Автолюбители","Главная Дорога","Киберспорт ОК","Dota 2","IT — Наука и техника","Тинькофф"]
    startPostsURL= ["","https://ok.ru/infomoscow24/topic/156297871069322","https://ok.ru/vesti/topic/156795562550671","https://ok.ru/spbsobakaru/topic/155699664257279","https://ok.ru/buzuluksam/topic/156827734797264","https://ok.ru/love.avto/topic/154699179326452","https://ok.ru/glavdoroga/topic/156525869111440","https://ok.ru/esports/topic/156286028897196","https://ok.ru/dotaru/topic/155460464413456","https://ok.ru/scinet/topic/156335930712217","https://ok.ru/tinkoffbank/topic/156509070443793"]
    for id_group in range (1,11):

        cnt_post=1
        browser.get(startPostsURL[id_group])
        time.sleep(1)
        insert_groups(id_group, allGroupsLink[id_group], allGroupsName[id_group])
        while cnt_post<=post:
            page_post = BeautifulSoup(browser.page_source, 'lxml')
            link_post = browser.current_url
            date_post = postDate(link_post)



            text_post = ""
            text_blocks = page_post.find("div", class_="media-layer_c").find_all("div", class_="media-text_cnt_tx")
            for block in text_blocks:
                text_post = text_post + block.text.strip() + "\n"

            try:
                cnt_likes = int(
                    page_post.find("div", class_="mlr_bot").find("span", class_="feed_info_sm_a").text.split()[0])
            except:
                cnt_likes = 0

            comments = page_post.find("div", class_="comments_lst").find_all("div", class_="comments_current")
            cnt_comments = len(comments)

            insert_posts(id_post, link_post, date_post, text_post, cnt_comments, cnt_likes, id_group)

            for item in comments:
                user_name_element = item.find("a", class_="comments_author-name")
                if user_name_element:
                    user_name = user_name_element.find("span").text.strip()
                else:
                    user_name = "Unknown User"
                user_link_element = item.find("a", class_="comments_author-name")
                if user_link_element:
                    link_user = user_link_element.get("href")
                else:
                    link_user = "Unknown Link"

                comment_text_element = item.find("span", class_="js-text-full")
                if comment_text_element:
                    comment_text = comment_text_element.text.strip()
                else:
                    comment_text = "No Text Found"

                comment_date_element = item.find("span", class_="comments_current__footer__main__date")
                if comment_date_element:
                    comment_date = date_format(comment_date_element.text.strip())
                else:
                    comment_date = "Unknown Date"

                insert_users(id_user, "https://ok.ru" + link_user, user_name)
                insert_comments(id_comment, comment_date, comment_text, id_post, id_user)
                id_user += 1
                id_comment += 1

            photos = page_post.find("div", class_="mlr_cnt").find_all("div", class_="media-photos_photo")
            videos = page_post.find("div", class_="mlr_cnt").find_all("div", class_="media-video")
            audios = page_post.find("div", class_="mlr_cnt").find_all("div", class_="track-with-cover")
            cnt_media = len(photos) + len(videos) + len(audios)

            for item in photos:
                try:
                    file_link = item.find("a").get("href")
                    file_type = "photo"
                    insert_media(id_media,file_link,file_type,id_post)
                    id_media += 1

                except:
                    None

            for item in videos:
                try:
                    file_link = item.find("a").get("href")
                    file_type = "video"
                    insert_media(id_media, file_link, file_type, id_post)
                    id_media += 1

                except:
                    None

            for item in audios:
                try:
                    file_link = item.find("a", class_="track-with-cover_name").get("href")
                    file_type = "audio"
                    insert_media(id_media, file_link, file_type, id_post)
                    id_media += 1

                except:
                    None


            try:
                browser.find_element(By.CLASS_NAME, "arw__next").click()
                id_post += 1
                cnt_post += 1
            except:
                print("except")
                id_post += 1
                cnt_post += 1
                break
            while browser.current_url == link_post:
                time.sleep(0.1)
