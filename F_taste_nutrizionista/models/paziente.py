from F_taste_nutrizionista.db import Base
from sqlalchemy import Column, String, Date, ForeignKey, Integer, LargeBinary, Boolean
from sqlalchemy.orm import relationship, backref


class PazienteModel(Base):
    __tablename__ = 'paziente'

    id_paziente = Column(String(7), primary_key=True)
    data_nascita = Column(Date)
    email = Column(String(45), nullable=False, unique = True)
    password = Column(LargeBinary, nullable=False)
    sesso = Column(Boolean)
    fk_nutrizionista = Column(Integer, ForeignKey('nutrizionista.id_nutrizionista', onupdate="CASCADE"), nullable=True)
    nutrizionista = relationship("NutrizionistaModel", back_populates='pazienti', lazy=True)
    #misurazioni_medico = relationship("MisurazioneMedicoModel", back_populates='paziente', lazy=True, cascade='delete')
    dieta_paziente = relationship("DietaModel",  back_populates='paziente' , lazy=True, cascade='delete')
    
    # Relazione verso la tabella di transizione per le patologie
    patologie = relationship('PatologiaModel', secondary='patologia_paziente', backref=backref('pazienti', lazy=True))
    # Relazione verso la tabella di tranzizione per le allergie
    allergie = relationship('AllergiaModel', secondary='allergia_paziente', backref=backref('pazienti', lazy=True))
    # Relazione verso la tabella di transizione per le intolleranze
    intolleranze = relationship('IntolleranzaModel', secondary='intolleranza_paziente', backref=backref('pazienti', lazy=True))
    
    richieste_aggiunta_paziente = relationship("RichiestaAggiuntaPazienteModel", lazy=True, cascade='all, delete')
    richieste_revocate = relationship("RichiestaRevocataModel", lazy=True, cascade='all, delete-orphan')

    def __init__(self, id_paziente, email, password, data_nascita=None, sesso=None, fk_nutrizionista=None):
        self.id_paziente = id_paziente
        self.data_nascita = data_nascita
        self.email = email
        self.password = password
        self.fk_nutrizionista = fk_nutrizionista
        self.sesso = sesso


    def __repr__(self):
        patologie_str = ', '.join([patologia.patologia for patologia in self.patologie])
        return "PazienteModel(email=%s, id_paziente=%s, password=%s, data_nascita=%s, sesso=%s, patologie=[%s])" % ( self.email, self.id_paziente, self.password, self.data_nascita, self.sesso, patologie_str)
    
    def __json__(self):
        return { 'id_paziente': self.id_paziente, 'data_nascita': self.data_nascita, 'sesso': self.sesso }
        