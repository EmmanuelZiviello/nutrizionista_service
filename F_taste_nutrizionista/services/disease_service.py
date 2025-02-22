from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.utils.management_utils import check_nutrizionista
from F_taste_nutrizionista.repositories.patologia_repository import PatologiaRepository
from F_taste_nutrizionista.repositories.intolleranza_repository import IntolleranzaRepository
from F_taste_nutrizionista.repositories.allergia_repository import AllergiaRepository
from F_taste_nutrizionista.repositories.nutrizionista_repository import NutrizionistaRepository
from F_taste_nutrizionista.services.paziente_service import PazienteRepository
from F_taste_nutrizionista.repositories.disease_repository import DiseaseRepository


class DiseaseService:



    @staticmethod
    def add_disease_to_patient(nutrizionista_email, paziente_id, disease):
        session = get_session('dietitian')

        try:
            # Ottieni il paziente
            paziente = PazienteRepository.find_by_id(paziente_id, session)
            if not paziente:
                return {'message': 'Paziente non presente nel database'}, 404

            # Ottieni il nutrizionista
            nutrizionista = NutrizionistaRepository.find_by_email(nutrizionista_email, session)
            if not nutrizionista:
                return {'message': 'Email nutrizionista non presente nel database'}, 404

            # Controlla che il paziente sia associato al nutrizionista
            if not check_nutrizionista(paziente, nutrizionista):
                return {'message': 'Questo paziente non è seguito da te!'}, 403

            # Controlla se la malattia è già associata al paziente
            if DiseaseRepository.check_association(disease, paziente_id, session):
                return {'message': f'Al paziente {paziente_id} è già associata la condizione: \"{disease}\"'}, 409

            # Associa la malattia al paziente
            DiseaseRepository.associate_disease(paziente_id, disease, session)
            return {'message': 'Condizione associata con successo!'}, 200

        finally:
            session.close()

    
    @staticmethod
    def delete_disease(nutrizionista_email, paziente_id, disease):
        session = get_session('dietitian')
        try:
            # Trova il paziente
            paziente = PazienteRepository.find_by_id(paziente_id, session)
            if not paziente:
                return {'message': 'Paziente non presente nel db.'}, 404

            # Trova il nutrizionista
            nutrizionista = NutrizionistaRepository.find_by_email(nutrizionista_email, session)
            if not nutrizionista:
                return {'message': 'Email nutrizionista non presente nel db.'}, 404

            # Verifica che il nutrizionista segua il paziente
            if not check_nutrizionista(paziente, nutrizionista):
                return {'message': 'Non segui questo paziente.'}, 403

            # Verifica se la malattia è associata al paziente
            if DiseaseRepository.check_association(disease, paziente_id, session):
                # Rimuove la malattia dal paziente
                DiseaseRepository.remove_disease_from_patient(paziente_id, disease, session)
                return {'message': 'Condizione disassociata con successo!'}, 200
            else:
                return {'message': f"Il paziente non soffre di: {disease}"}, 404

        finally:
            session.close()


    @staticmethod
    def extract_data():
        """
        Recupera i dati dal database e li restituisce come tuple.
        """
        session = get_session('dietitian')
        try:
            # Estraiamo i dati dalle repository
            patologie_names = PatologiaRepository.get_all_patologie(session)
            allergie_names = AllergiaRepository.get_all_allergie(session)
            intolleranze_names = IntolleranzaRepository.get_all_intolleranze(session)
            return patologie_names, allergie_names, intolleranze_names
        finally:
            session.close()

    @staticmethod
    def process_data():
        """
        Estrae i dati e verifica se sono validi prima di costruire la struttura finale.
        """
        try:
            # Estraiamo i dati
            patologie_names, allergie_names, intolleranze_names = DiseaseService.extract_data()

            # Se uno dei tre dataset è vuoto, restituiamo None
            if not (patologie_names and allergie_names and intolleranze_names):
                return None

            # Costruiamo la struttura finale
            return DiseaseService.construct_data_structure(patologie_names, allergie_names, intolleranze_names)

        except Exception:
            return None

    @staticmethod
    def construct_data_structure(pat_list, alg_list, int_list):
        """
        Costruisce la struttura JSON finale con i dati estratti.
        """
        return {
            "patologie": DiseaseService.create_components(pat_list),
            "allergie": DiseaseService.create_components(alg_list),
            "intolleranze": DiseaseService.create_components(int_list)
        }

    @staticmethod
    def create_components(items):
        """
        Converte una lista di stringhe in un elenco di dizionari con chiave 'name'.
        """
        return [{"name": item} for item in items]
