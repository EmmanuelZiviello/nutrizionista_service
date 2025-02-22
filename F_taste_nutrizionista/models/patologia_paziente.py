from F_taste_nutrizionista.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey

class PatologiaPaziente(Base):
    
    __tablename__ = "patologia_paziente"
    paziente_id = Column('paziente_id', String(7), ForeignKey("paziente.id_paziente"), primary_key=True)
    patologia_id = Column('patologia_id', Integer, ForeignKey("patologia.id_patologia"), primary_key=True)
    
    