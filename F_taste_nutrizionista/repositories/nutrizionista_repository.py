from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.models.nutrizionista import NutrizionistaModel

class NutrizionistaRepository:

  

    @staticmethod
    def find_by_id(id_nutrizionista, session=None):
        session = session or get_session('dietitian')
        return session.query(NutrizionistaModel).filter_by(id_nutrizionista=id_nutrizionista).first()

    @staticmethod
    def find_by_email(email, session=None):
        session = session or get_session('dietitian')
        return session.query(NutrizionistaModel).filter_by(email=email).first()

    @staticmethod
    def add(nutrizionista, session=None):
        session = session or get_session('dietitian')
        session.add(nutrizionista)
        session.commit()

    @staticmethod
    def delete(nutrizionista, session=None):
        session = session or get_session('dietitian')
        session.delete(nutrizionista)
        session.commit()

    @staticmethod
    def update_link_informativa(nutrizionista, link_informativa):
        session = get_session("dietitian")
        nutrizionista.link_informativa = link_informativa
        session.commit()
        
   
   