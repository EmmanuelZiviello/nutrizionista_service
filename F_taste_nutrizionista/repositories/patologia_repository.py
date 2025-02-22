from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.models.patologia import PatologiaModel

class PatologiaRepository:
    
    @staticmethod
    def find_patologia(patologia_nome, session=None):
        session = session or get_session('dietitian')
        return session.query(PatologiaModel).filter_by(patologia=patologia_nome).first()
    
    @staticmethod
    def get_all_patologie(session=None):
        session = session or get_session('dietitian')
        result = []
        try:
            # Eseguiamo la query per ottenere tutte le patologie
            patologie = session.query(PatologiaModel).all()
            # Aggiungiamo il nome di ogni patologia alla lista result
            for patologia in patologie:
                result.append(patologia.patologia)
            return result
        except Exception:
            # In caso di errore, ritorniamo una lista vuota
            return []
