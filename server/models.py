from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, String, Integer, Float, ForeignKey

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    price = Column(Float)
