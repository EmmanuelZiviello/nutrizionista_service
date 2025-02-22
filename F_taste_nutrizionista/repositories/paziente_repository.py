from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.models.paziente import PazienteModel
from F_taste_nutrizionista.models.nutrizionista import NutrizionistaModel
from sqlalchemy.exc import SQLAlchemyError

class PazienteRepository:

    @staticmethod
    def find_by_email(email, session=None):
        session = session or get_session('dietitian')
        return session.query(PazienteModel).filter_by(email=email).first()

    @staticmethod
    def find_by_id(id_paziente, session=None):
        session = session or get_session('dietitian')
        return session.query(PazienteModel).filter_by(id_paziente=id_paziente).first()

    @staticmethod
    def add(paziente, session=None):
        session = session or get_session('dietitian')
        session.add(paziente)
        session.add(paziente.consensi_utente)#forse necessario dato che viene creato insieme al paziente
        session.commit()

    @staticmethod
    def delete(paziente, session=None):
        session = session or get_session('dietitian')
        session.delete(paziente)
        session.commit()


    @staticmethod
    def update_by_id(paziente, updated_data, session=None):
        session = session or get_session('dietitian')
        try:
            if paziente:
                for key, value in updated_data.items():
                    setattr(paziente, key, value)
                session.commit()
                return paziente
            return None
        except SQLAlchemyError:
            session.rollback()
            return None  
       

    @staticmethod
    def delete_by_id(id_paziente, session=None):
        session = session or get_session('dietitian')
        try:
            paziente = session.query(PazienteModel).filter_by(id_paziente=id_paziente).first()
            if paziente:
                session.delete(paziente)
                session.commit()
                return True
            return False
        except SQLAlchemyError:
            session.rollback()
            return False
        


    @staticmethod
    def aggiorna_nutrizionista(paziente, id_nutrizionista, nutrizionista,session=None):
        session=session or get_session('dietitian')
        paziente.fk_nutrizionista = id_nutrizionista
        paziente.nutrizionista =nutrizionista
        session.add(paziente)
        session.commit()
        return paziente
    

    @staticmethod
    def revoca_nutrizionista(paziente, session=None):
        session=session or get_session('dietitian')
        paziente.fk_nutrizionista =None
        paziente.nutrizionista =None
        session.add(paziente)
        session.commit()
        return paziente

