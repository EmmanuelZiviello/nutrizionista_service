from F_taste_nutrizionista.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey

class IntolleranzaPaziente(Base):
    
    __tablename__ = "intolleranza_paziente"
    paziente_id = Column('paziente_id', String(7), ForeignKey("paziente.id_paziente"), primary_key=True)
    intolleranza_id = Column('intolleranza_id', Integer, ForeignKey("intolleranza.id_intolleranza"), primary_key=True)
    
    