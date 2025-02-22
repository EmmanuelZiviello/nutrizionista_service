from F_taste_nutrizionista.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import StringEncryptedType

class IntolleranzaModel(Base):
    __tablename__ = "intolleranza"
    id_intolleranza = Column(Integer, primary_key=True)
    intolleranza =  Column(String(600), unique=True, nullable=False)

    def __repr__(self):
        return "IntolleranzaModel(intolleranza:%s)" % (self.intolleranza)

    def __json__(self):
        return { 'name': self.intolleranza}

    def __init__(self, intolleranza):
        self.intolleranza = intolleranza
