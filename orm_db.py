from flask import jsonify
import os

from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)

class MenuItem(Base):
    __tablename__ = 'menuitem'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)
    description = Column(String)
    price = Column(String(8))
    course = Column(String)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    """ delete,all used for cascade deletion"""
    restaurant = relationship(Restaurant,
                                backref = backref('menuitem',
                                                uselist=True,
                                                cascade = 'delete,all'))
    @property
    def serialize(self):
        return {
        'name' : self.name,
        'description' : self.description,
        'id' : self.id,
        'price' : self.price,
        'course' : self.course,
        }

engine = create_engine('sqlite:///restaurant.db')

Session  = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

session = Session()


#append to page HTML
def getData(table):
    session = Session()
    data = session.query(Base.metadata.tables[table]).all()
    return data


def getDataById(idd):
    session = Session()
    menuitem = Base.metadata.tables['menuitem']
    restaurant = Base.metadata.tables['restaurant']
    menuitemId = menuitem.c.restaurant_id
    restaurantId = restaurant.c.id
    data = session.query(menuitem,restaurant).filter(menuitemId == idd, menuitemId == restaurantId).all()
    #data = session.execute(menuitem.select().where(id == restaurantId)).fetchall()
    return data

def getJsonData(idd):
    restaurant = session.query(Restaurant).filter_by(id=idd).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=idd).all()
    return jsonify(MenuItems=[i.serialize for i in items])

def createData(table,datas,id):
    session = Session()
    data = Base.metadata.tables[table]
    session.execute(data.insert(),{'name':datas, 'restaurant_id': id})
    session.commit()
    return

def getOneData(idNumber,idRes):
    session = Session()
    menuitem = Base.metadata.tables['menuitem']
    menuitemId = menuitem.c.id
    restaurantId = menuitem.c.restaurant_id
    data = session.query(menuitem).filter(menuitemId == int(idNumber), restaurantId == int(idRes)).one()
    return data


def delData(idNumber,idRes):
    session = Session()
    data = Base.metadata.tables['menuitem']
    menuitemId = data.c.id
    restaurantId = data.c.restaurant_id
    del_st = data.delete().where(menuitemId == int(idNumber)).where(restaurantId == int(idRes))
    session.execute(del_st)
    print del_st
    #d = session.query(data).filter(menuitemId == idNumber,restaurantId == idRes)
    #session.delete(d)
    session.commit()
    return

def updateData(table,idNumber,datas):
    session = Session()
    data = Base.metadata.tables[table]
    name = data.c.name
    id = data.c.id
    session.execute(data.update().where(id==int(idNumber)).values(name=datas))
    session.commit()
    return
