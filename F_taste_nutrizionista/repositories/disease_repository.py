from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.models.paziente import PazienteModel
from F_taste_nutrizionista.models.patologia import PatologiaModel
from F_taste_nutrizionista.models.allergia import AllergiaModel
from F_taste_nutrizionista.models.intolleranza import IntolleranzaModel


class DiseaseRepository:

    @staticmethod
    def check_association(disease, paziente_id, session=None):
        session=session or get_session('dietitian')
        paziente = session.query(PazienteModel).filter_by(id=paziente_id).first()
        if not paziente:
            return False

        return any(patologia.nome == disease for patologia in paziente.patologie) or \
               any(allergia.nome == disease for allergia in paziente.allergie) or \
               any(intolleranza.nome == disease for intolleranza in paziente.intolleranze)

    @staticmethod
    def associate_disease(paziente_id, disease, session=None):
        session=session or get_session('dietitian')
        paziente = session.query(PazienteModel).filter_by(id=paziente_id).first()
        if not paziente:
            raise ValueError("Paziente non trovato")

        disease_model = DiseaseRepository.find_disease_model(disease, session)
        if not disease_model:
            raise ValueError(f"Condizione non trovata: {disease}")

        if isinstance(disease_model, PatologiaModel):
            paziente.patologie.append(disease_model)
        elif isinstance(disease_model, AllergiaModel):
            paziente.allergie.append(disease_model)
        elif isinstance(disease_model, IntolleranzaModel):
            paziente.intolleranze.append(disease_model)
        
        session.commit()

    @staticmethod
    def find_disease_model(disease, session=None):
        session=session or get_session('dietitian')
        return (
            session.query(PatologiaModel).filter_by(nome=disease).first() or
            session.query(AllergiaModel).filter_by(nome=disease).first() or
            session.query(IntolleranzaModel).filter_by(nome=disease).first()
        )


    @staticmethod
    def remove_disease_from_patient(paziente_id, disease, session=None):
        session = session or get_session('dietitian')
        paziente = session.query(PazienteModel).filter_by(id=paziente_id).first()
        if not paziente:
            raise ValueError("Paziente non trovato")

        disease_model = DiseaseRepository.find_disease_model(disease, session)
        if not disease_model:
            raise ValueError(f"Condizione non trovata: {disease}")

        if isinstance(disease_model, PatologiaModel):
            if disease_model in paziente.patologie:
                paziente.patologie.remove(disease_model)
                session.commit()
                
        elif isinstance(disease_model, AllergiaModel):
            if disease_model in paziente.allergie:
                paziente.allergie.remove(disease_model)
                session.commit()
                
        elif isinstance(disease_model, IntolleranzaModel):
            if disease_model in paziente.intolleranze:
                paziente.intolleranze.remove(disease_model)
                session.commit()
                

    
