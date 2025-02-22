from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.models.intolleranza import IntolleranzaModel

class IntolleranzaRepository:
    
    @staticmethod
    def find_intolleranza(intolleranza_nome, session=None):
        session = session or get_session('dietitian')
        return session.query(IntolleranzaModel).filter_by(intolleranza=intolleranza_nome).first()

    @staticmethod
    def get_all_intolleranze(session=None):
        session = session or get_session('dietitian')
        result = []
        try:
            # Eseguiamo la query per ottenere tutte le patologie
            intolleranze = session.query(IntolleranzaModel).all()
            # Aggiungiamo il nome di ogni patologia alla lista result
            for intolleranza in intolleranze:
                result.append(intolleranza.intolleranza)
            return result
        except Exception:
            # In caso di errore, ritorniamo una lista vuota
            return []