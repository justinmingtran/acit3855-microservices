from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Item(Base):
    """ Item """

    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)


    def __init__(self, item_name):
        """ Initializes an item """
        self.item_name = item_name
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of an item"""
        dict = {}
        dict['item_id'] = self.item_id
        dict['item_name'] = self.item_name

        return dict
