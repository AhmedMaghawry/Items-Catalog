import os
import sys
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Catalog(Base):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class CItem(Base):
    __tablename__ = 'citem'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
	    'cat_id': self.catalog_id,
        }

engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
