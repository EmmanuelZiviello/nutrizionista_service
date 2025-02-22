from F_taste_nutrizionista.db import Base
from sqlalchemy import Column, Integer, String
class PatologiaModel(Base):
    __tablename__ = "patologia"
    id_patologia = Column(Integer, primary_key=True)
    patologia = Column(String(600), unique=True, nullable=False)

    def __init__(self, patologia):
        self.patologia = patologia

    def __repr__(self):
        return "PatologiaModel(patologia:%s)" % (self.patologia)

    def __json__(self):
        return { 'name': self.patologia }

