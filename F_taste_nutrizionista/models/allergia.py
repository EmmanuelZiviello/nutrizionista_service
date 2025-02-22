from F_taste_nutrizionista.db import Base
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class AllergiaModel(Base):
    __tablename__ = "allergia"
    id_allergia = Column(Integer, primary_key=True)
    allergia = Column(String(600), unique=True, nullable=False)

    def __repr__(self):
        return "AllergiaModel(allergia:%s)" % (self.allergia)

    def __json__(self):
        return { 'name': self.allergia}

    def __init__(self, allergia):
        self.allergia = allergia

   