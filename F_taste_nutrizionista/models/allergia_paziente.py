from F_taste_nutrizionista.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey

class AllergiaPaziente(Base):
    
    __tablename__ = "allergia_paziente"
    paziente_id = Column('paziente_id', String(7), ForeignKey("paziente.id_paziente"), primary_key=True)
    allergia_id = Column('allergia_id', Integer, ForeignKey("allergia.id_allergia"), primary_key=True)
    
    