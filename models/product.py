from . import DeclarativeBase
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float


class Product(DeclarativeBase):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    url = Column(String)
    name = Column(String)
    price = Column(String)
    description = Column(String)
    parser_id = Column(Integer)
    is_send = Column(Boolean, default=False)

    def __init__(self, url, description, parser_id, name, price):
        self.url = url
        self.parser_id = parser_id
        self.description = description
        self.price = price
        self.name = name

    def to_telegram_str(self) -> str:
        message = f"{self.name} \n{self.price} \n \n{self.description} \n \n{self.url}"
        return message
