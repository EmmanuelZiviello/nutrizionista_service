from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.repositories.paziente_repository import PazienteRepository
from F_taste_nutrizionista.repositories.nutrizionista_repository import NutrizionistaRepository
from F_taste_nutrizionista.utils.management_utils import check_nutrizionista
from F_taste_nutrizionista.repositories.richiesta_aggiunta_paziente_repository import RichiestaAggiuntaPazienteRepository
from F_taste_nutrizionista.schemas.paziente import PazienteSchema
from flask import request
from flask_jwt_extended import get_jwt_identity


paziente_schema_for_dump = PazienteSchema(only=['id_paziente', 'sesso', 'data_nascita'])
paziente_schema_put = PazienteSchema(exclude=['email','password'], partial=['fk_nutrizionista'])

class PazienteService:

    @staticmethod
    def get_conditions(id_paziente, email_nutrizionista):
        session=get_session('dietitian')
        paziente = PazienteRepository.find_by_id(id_paziente,session)
        if paziente is None:
            session.close()
            return {'message': 'paziente non presente nel db'}, 404

        nutrizionista = NutrizionistaRepository.find_by_email(email_nutrizionista)
        if nutrizionista is None:
            session.close()
            return {'message': 'email nutrizionista non presente nel db'}, 404

        if check_nutrizionista(paziente, nutrizionista):
            session.close()
            return {
                "patologie": [p.__json__() for p in paziente.patologie],
                "allergie": [a.__json__() for a in paziente.allergie],
                "intolleranze": [i.__json__() for i in paziente.intolleranze]
            }, 200
        session.close()
        return {'message': 'non segui questo paziente'}, 403
    


    @staticmethod
    def get_paziente_by_id(id_paziente):
        session = get_session('dietitian')
        # Recupero del paziente dal repository
        try:
            paziente=PazienteRepository.find_by_id(id_paziente,session)
            if not paziente:
                 return {"message":"Paziente non trovato"},400
            return paziente_schema_for_dump.dump(paziente), 200
        except Exception as e:
            # Log dell'errore per debugging
            print(f"Errore durante la ricerca del paziente: {e}")
            return None 
        finally:
            session.close()



    @staticmethod
    def aggiungi_paziente():
        session=get_session('dietitian')
        # Recuperiamo il JSON dalla richiesta
        request_dict = request.get_json()

        # Validiamo i dati
        validation_schema = PazienteSchema(only=['id_paziente'])
        validation_errors = validation_schema.validate(request_dict)
        if validation_errors:
            return validation_errors, 400

        # Recuperiamo il nutrizionista dal token JWT
        email_nutrizionista = get_jwt_identity()
        nutrizionista = PazienteRepository.find_by_email(email_nutrizionista,session)
        if nutrizionista is None:
            session.close()
            return {"message": "nutrizionista non presente nel database"}, 404

        # Recuperiamo il paziente
        paziente = PazienteRepository.find_by_id(request_dict['id_paziente'],session)
        if paziente is None:
            session.close()
            return {"message": "paziente non presente nel database"}, 404

        # Controlliamo se il paziente è già seguito
        if paziente.fk_nutrizionista is not None:
            if paziente.fk_nutrizionista == nutrizionista.id_nutrizionista:
                session.close()
                return {"message": "segui già questo paziente"}, 304
            else:
                session.close()
                return {"message": "Paziente seguito da un altro nutrizionista"}, 403

        # Controlliamo se esiste già una richiesta pendente
        check_existing_request = RichiestaAggiuntaPazienteRepository.find_by_id_paziente_and_id_nutrizionista(paziente.id_paziente, nutrizionista.id_nutrizionista,session)
        if check_existing_request is not None:
            session.close()
            return {"message": "richiesta già presente"}, 403

        # Creiamo una nuova richiesta di aggiunta
        RichiestaAggiuntaPazienteRepository.add_richiesta(paziente.id_paziente, nutrizionista.id_nutrizionista, nutrizionista,session)
        session.close()
        return {"message": "richiesta aggiunta a propria lista pazienti inviata con successo"}, 200
    



    @staticmethod
    def rimuovi_paziente(request_dict, email_nutrizionista):
        session=get_session('dietitian')
        validation_schema = PazienteSchema(only=['id_paziente'])
        validation_errors = validation_schema.validate(request_dict)

        if validation_errors:
            session.close()
            return validation_errors, 400

        nutrizionista = NutrizionistaRepository.find_by_email(email_nutrizionista, session)
        if nutrizionista is None:
            session.close()
            return {"message": "nutrizionista non trovato nel database"}, 404

        paziente = PazienteRepository.find_by_id(request_dict['id_paziente'], session)
        if paziente is None:
            session.close()
            return {"message": "paziente non presente nel database"}, 404

        if paziente.fk_nutrizionista != nutrizionista.id_nutrizionista:
            session.close()
            return {"message": "non segui questo paziente"}, 403

        
        paziente=PazienteRepository.revoca_nutrizionista(paziente, session)
        if paziente is None:
            session.close()
            return {"message":"Errore revoca paziente del  nutrizionista"},400
        return {"message": "non segui più questo paziente"}, 200
    


    @staticmethod
    def check_chiavi(dizionario):
        chiavi_ammesse = {'id_paziente', 'sesso', 'data_nascita'}
        chiavi_dizionario = set(dizionario.keys())
        return chiavi_dizionario.issubset(chiavi_ammesse) and len(chiavi_dizionario) <= 3

    @staticmethod
    def modifica_paziente(email_nutrizionista, s_paziente):
        session = get_session('dietitian')
        nutrizionista = NutrizionistaRepository.find_by_email(email_nutrizionista, session)
        
        if nutrizionista is None:
            session.close()
            return {'message': 'Nutrizionista non presente nel Database'}, 404

        paziente = PazienteRepository.find_by_id(s_paziente['id_paziente'],session)
        if paziente is None:
            session.close()
            return {'message': 'Paziente non presente nel Database'}, 404
        
        if paziente.fk_nutrizionista is None:
            session.close()
            return {'message': 'Paziente non seguito da un nutrizionista'}, 403
        
        if paziente.fk_nutrizionista != nutrizionista.id_nutrizionista:
            session.close()
            return {'message': 'Paziente seguito da un altro nutrizionista'}, 403

        if not PazienteService.check_chiavi(s_paziente):
            return {"message": "Campi per la richiesta non validi"}, 404

        if "data_nascita" not in s_paziente and "sesso" not in s_paziente:
            return {"message": "Serve almeno un campo tra sesso e data_nascita"}, 404

        #invia tramite kafka la richiesta al servizio paziente di modificare un paziente e riceve i nuovi dati del paziente
        #paziente = PazienteRepository.update_paziente(session, paziente, s_paziente.get("data_nascita"), s_paziente.get("sesso"))
        #quindi riceve tramite kafka il nuovo paziente con lo stesso id e nuovi dati e lo restituisce con dump
        session.close()
        return paziente_schema_put.dump(paziente), 200
    






    @staticmethod
    def get_paziente_info(id_paziente, email_nutrizionista):
        session = get_session('dietitian')
        try:
            nutrizionista = NutrizionistaRepository.find_by_email(email_nutrizionista, session)
            if nutrizionista is None:
                return { 'message': 'nutrizionista non presente nel db' }, 404

            patient = PazienteRepository.find_by_id(id_paziente, session)
            if patient is None:
                return { "message": "Paziente non trovato" }, 404

            if patient.fk_nutrizionista != nutrizionista.id_nutrizionista:
                return { "message": "paziente seguito da un altro nutrizionista" }, 403

            #tramite kafka richiede l'ultima misurazione medico del paziente
            #e modifica peso altezza e menopausa del paziente nei suoi dati(nel servizio paziente,quindi questo servizio manda solo un kafka)
            #quindi:kafka richiesta misurazione , kafka di aggiornare il paziente con i dati 
            #ultima_misurazione_medico = PazienteRepository.get_last_misurazione_medico(patient.id_paziente, session)
            pazienteSchema = PazienteSchema(only=['id_paziente', 'sesso', 'data_nascita'])
            

            return pazienteSchema.dump(patient), 200
        finally:
            session.close()