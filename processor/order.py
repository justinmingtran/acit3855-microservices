from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Order(Base):
    """ Order """

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_id = Column(String, nullable=False)
    ordered_item = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)


    def __init__(self, order_id, ordered_item, quantity):
        """ Initializes an order """
        self.order_id = order_id
        self.ordered_item = ordered_item
        self.quantity = quantity
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of an order"""
        dict = {}
        dict['id'] = self.id
        dict['order_id'] = self.order_id
        dict['ordered_item'] = self.ordered_item
        dict['quantity'] = self.quantity

        return dict
