import os
from email.message import EmailMessage
from smtplib import SMTP
import requests
from bs4 import BeautifulSoup

rank_list = []
title_list = []
link_list = []
article_list_info = []
score_list = []
for i in range(1, 28):
    soup = BeautifulSoup(requests.get(f"https://news.ycombinator.com/?p={i}").text, 'html.parser')
    for rank in soup.select('.rank'):
        rank_list.append(rank.text)
    for title_class in soup.select('.titleline'):
        link_list.append(title_class.select_one('a')['href'])
        title_list.append(title_class.text)
    for article_info in soup.select(selector='.subtext'):
        article_list_info.append(article_info.text)
        if article_info.select_one(".score") is None:
            score_list.append(0)
        else:
            score_list.append(int(article_info.text.split()[0]))
    print("Page # ", i)

max_score_index = score_list.index(max(score_list))
best_article_info = f"ARTICLE# {rank_list[max_score_index]} (Page#{(int(rank_list[max_score_index].split('.')[0]))//30 + 1})" \
                  f"\nTITLE: {title_list[max_score_index]}\nARTICLE_INFO: {article_list_info[max_score_index][1:-1]}" \
                  f"\nARTICLE LINK: {link_list[max_score_index]}"


message = EmailMessage()
message["Subject"] = "BEST ARTICLE ON Y COMBINATOR"
message["From"] = os.environ['SENDER_MAIL']
message["To"] = os.environ["RECEIVER_MAIL"]
message.set_content(best_article_info)

with SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=os.environ['SENDER_MAIL'], password=os.environ['PASSWORD'])
    connection.send_message(message)
