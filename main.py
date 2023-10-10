import sqlalchemy
import sqlalchemy as sq
import psycopg2
import requests
import pprint

from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale
DSN = open("dsn").read()

engine = sqlalchemy.create_engine(DSN)
# create_tables(engine)
#
#
# #url = "https://github.com/netology-code/py-homeworks-db/blob/SQLPY-76/06-orm/fixtures/tests_data.json"
# url = "https://github.com/netology-code/py-homeworks-db/raw/SQLPY-76/06-orm/fixtures/tests_data.json"
# resp = requests.get(url)
# # print(resp.status_code)
# data_for_db = resp.json()
# #pprint.pprint(data_for_db[0])
Session = sessionmaker(bind=engine)
session = Session()
# for el in data_for_db:
#     pprint.pprint(el)
#     # pprint.pprint(el['model'])
#     if el['model'] == 'publisher':
#         pb = Publisher(name = el['fields']['name'])
#         session.add(pb)
#     elif el['model'] == 'book':
#         b = Book(id_publisher = el['fields']['id_publisher'], title = el['fields']['title'])
#         session.add(b)
#     elif el['model'] == 'shop':
#         sh = Shop(name_shop = el['fields']['name'])
#         session.add(sh)
#     elif el['model'] == 'stock':
#         st = Stock(count = el['fields']['count'],id_book = el['fields']['id_book'], id_shop = el['fields']['id_shop'])
#         session.add(st)
#     elif el['model'] ==  'sale':
#         s = Sale(price = el['fields']['price'], date_sale = el['fields']['date_sale'], id_stock = el['fields']['id_stock'], count = el['fields']['count'])
#         session.add(s)
# session.commit()

#
publ = input("Введите название автора/издателя, по которому необходимо вывести продажи его книг? ")

q = session.query(Book.title, Shop.name_shop, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name.like(publ))

for b in q.all():
    print(f"{b[0]} | {b[1]} | {b[2]} | {b[3]}")
session.close()
