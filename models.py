import sqlalchemy
import psycopg2
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    def __str__(self):
        return f"{self.id}: {self.name} "
    # homeworks = relationship("Homework", back_populates="course")


class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="book")
    def __str__(self):
        return f"{self.id}: {self.title} {self.id_publisher}  "

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name_shop = sq.Column(sq.String(length=60), unique=True)


class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")


class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL(10, 2), nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer)
    stock = relationship(Stock, backref="sale")
    def __str__(self):
        return f"{self.id}: {self.price} {self.date_sale} {self.id_stock} {self.count} "

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

