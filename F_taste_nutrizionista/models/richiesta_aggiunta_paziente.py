from datetime import datetime
from F_taste_nutrizionista.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship



class RichiestaAggiuntaPazienteModel(Base):
    __tablename__ = "richiesta_aggiunta_paziente"

    id_richiesta = Column(Integer, primary_key=True)
    accettata = Column(Boolean, default = False)
    data_richiesta = Column(TIMESTAMP, nullable = False)
    data_accettazione = Column(TIMESTAMP, nullable = True)
    fk_nutrizionista = Column(Integer, 
                            ForeignKey("nutrizionista.id_nutrizionista"), 
                            nullable=False)
    fk_paziente = Column(String(10), 
                            ForeignKey("paziente.id_paziente"), 
                            nullable=False)
    nutrizionista = relationship("NutrizionistaModel", back_populates='richieste_aggiunta_paziente', lazy=True)
    paziente = relationship("PazienteModel", back_populates='richieste_aggiunta_paziente', lazy=True)
    __table_args__ = (UniqueConstraint(fk_paziente, fk_nutrizionista, name="one_request_for_each_patient_by_a_nutritionist"),)
    


    def __repr__(self):
        return "RichiestaAggiuntaPazienteModel(fk_paziente:%s, fk_nutrizionista:%s, accettata:%s, data_richiesta:%s, data_accettazione:%s)" % (self.fk_paziente, self.fk_nutrizionista, self.accettata, self.data_richiesta,self.data_accettazione)
    
    def __json__(self):
        return { 'fk_paziente': self.fk_paziente, 
                'fk_nutrizionista': self.fk_nutrizionista, 
                'accettata': self.accettata, 
                'data_richiesta': self.data_richiesta,
                'data_accettazione': self.data_accettazione }

    def __init__(self, fk_paziente, fk_nutrizionista):
        self.fk_paziente = fk_paziente
        self.fk_nutrizionista = fk_nutrizionista
        self.accettata = False
        self.data_richiesta = datetime.now()    

