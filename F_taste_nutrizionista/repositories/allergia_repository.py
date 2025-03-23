from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.models.allergia import AllergiaModel

class AllergiaRepository:
    
    @staticmethod
    def find_allergia(allergia_nome, session=None):
        session = session or get_session('dietitian')
        return session.query(AllergiaModel).filter_by(allergia=allergia_nome).first()


    @staticmethod
    def get_all_allergie(session=None):
        session = session or get_session('dietitian')
        try:
            # Eseguiamo la query per ottenere tutte le patologie
            allergie = session.query(AllergiaModel).all()
            # Aggiungiamo il nome di ogni patologia alla lista result
            return [allergia.allergia for allergia in allergie]
        except Exception:
            # In caso di errore, ritorniamo una lista vuota
            return []