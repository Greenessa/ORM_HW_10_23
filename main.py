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

url = "https://github.com/netology-code/py-homeworks-db/raw/SQLPY-76/06-orm/fixtures/tests_data.json"
resp = requests.get(url)
# print(resp.status_code)
data_for_db = resp.json()
#pprint.pprint(data_for_db[0])

Session = sessionmaker(bind=engine)
session = Session()

for el in data_for_db:
    pprint.pprint(el)
    # pprint.pprint(el['model'])
    if el['model'] == 'publisher':
        pb = Publisher(name = el['fields']['name'])
        session.add(pb)
    elif el['model'] == 'book':
        b = Book(id_publisher = el['fields']['id_publisher'], title = el['fields']['title'])
        session.add(b)
    elif el['model'] == 'shop':
        sh = Shop(name_shop = el['fields']['name'])
        session.add(sh)
    elif el['model'] == 'stock':
        st = Stock(count = el['fields']['count'],id_book = el['fields']['id_book'], id_shop = el['fields']['id_shop'])
        session.add(st)
    elif el['model'] ==  'sale':
        s = Sale(price = el['fields']['price'], date_sale = el['fields']['date_sale'], id_stock = el['fields']['id_stock'], count = el['fields']['count'])
        session.add(s)
session.commit()


def get_shops(pub):
    q = session.query(Book.title, Shop.name_shop, Sale.price, Sale.date_sale ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)

    if pub.isdigit(): #Проверяем переданные данные в функцию на то, что строка состоит только из чисел
        q2 = q.filter(Publisher.id == pub).all() #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где айди публициста равно переданным данным в функцию, и сохраняем в переменную
    else:
        q2 = q.filter(Publisher.name == pub).all() #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где имя публициста равно переданным данным в функцию, и сохраняем в переменную

    for title, name_shop, price, date_sale in q2: #Проходим в цикле по переменой, в которой сохранянен результат фильтрации, и при каждой итерации получаем кортеж и распаковываем значения в 4 переменные
        print(f"{title: <40} | {name_shop: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}") #Передаем в форматированную строку переменные, которые содержат имя книги, название магазина, стоимость продажи и дату продажи


if __name__ == '__main__':
    pb = input("Введите название автора/издателя, по которому необходимо вывести продажи его книг, или его id? ") #Просим клиента ввести имя или айди публициста и данные сохраняем в переменную
    get_shops(pb) #Вызываем функцию получения данных из базы, передавая в функцию данные, которые ввел пользователь строкой выше

session.close()