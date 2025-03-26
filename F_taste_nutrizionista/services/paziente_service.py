from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.repositories.nutrizionista_repository import NutrizionistaRepository
from flask import request
from flask_jwt_extended import get_jwt_identity
from F_taste_nutrizionista.kafka.kafka_producer import send_kafka_message
from F_taste_nutrizionista.utils.kafka_helpers import wait_for_kafka_response

class PazienteService:

   




    @staticmethod
    def aggiungi_paziente(s_paziente,email_nutrizionista):
        if "id_paziente" not in s_paziente:
            return {"message": "ID paziente richiesto"}, 400  # HTTP 400 Bad Request
        id_paziente=s_paziente["id_paziente"]
        session=get_session('dietitian')
        nutrizionista=NutrizionistaRepository.find_by_email(email_nutrizionista,session)
        if nutrizionista is None:
            session.close()
            return {"message": "Nutrizionista non presente nel database"}, 404
        id_nutrizionista=nutrizionista.id_nutrizionista
        session.close()
        message={"id_paziente":id_paziente,"id_nutrizionista":id_nutrizionista}
        send_kafka_message("patient.addDietitian.request",message)
        response=wait_for_kafka_response(["patient.addDietitian.success", "patient.addDietitian.failed"])
        return response

   

    @staticmethod
    def rimuovi_paziente(s_paziente,email_nutrizionista):
        id_paziente=s_paziente["id_paziente"]
        session=get_session('dietitian')
        nutrizionista=NutrizionistaRepository.find_by_email(email_nutrizionista,session)
        if nutrizionista is None:
            session.close()
            return {"message": "Nutrizionista non presente nel database"}, 404
        id_nutrizionista=nutrizionista.id_nutrizionista#serve salvarlo per mandarlo con kafka
        session.close()
        message={"id_paziente":id_paziente,"id_nutrizionista":id_nutrizionista}
        send_kafka_message("dietitian.removeFk.request",message)
        response=wait_for_kafka_response(["dietitian.removeFk.success", "dietitian.removeFk.failed"])
        return response



    @staticmethod
    def check_chiavi(dizionario):
        chiavi_ammesse = {'id_paziente', 'sesso', 'data_nascita'}
        chiavi_dizionario = set(dizionario.keys())
        return chiavi_dizionario.issubset(chiavi_ammesse) and len(chiavi_dizionario) <= 3

    @staticmethod
    def modifica_paziente(email_nutrizionista,s_paziente):
        session=get_session('dietitian')
        nutrizionista=NutrizionistaRepository.find_by_email(email_nutrizionista,session)
        if nutrizionista is None:
            session.close()
            return {'message': 'Nutrizionista non presente nel Database' }, 404
        id_nutrizionista=nutrizionista.id_nutrizionista
        id_paziente=s_paziente["id_paziente"]
        session.close()
          # Cotrollo dinamico sulla sicurezza del dizionario inviato
        if not PazienteService.check_chiavi(s_paziente):
            return {"messsage" : "Campi per la richiesta non validi"}, 404
        # Se nella richiesta non sono presenti i campi sesso e data di nascita viene segnalato un errore
        if "data_nascita" not in s_paziente and "sesso" not in s_paziente:
            return {"message" : "Serve almeno un campo tra sesso e data_nascita"}, 404
        # Variabili per data_nascita e sesso
        data_nascita = s_paziente.get("data_nascita")
        sesso = s_paziente.get("sesso")
         # Creazione del messaggio con i dati disponibili
        message = {"id_paziente": id_paziente,"id_nutrizionista":id_nutrizionista}
        if data_nascita is not None:
            message["data_nascita"] = data_nascita
        if sesso is not None:
            message["sesso"] = sesso
        send_kafka_message("patient.update.request",message)
        response=wait_for_kafka_response(["patient.update.success", "patient.update.failed"])
        return response
        
        
   


    @staticmethod
    def get_paziente_info(id_paziente,email_nutrizionista):
        session=get_session('dietitian')
        nutrizionista=NutrizionistaRepository.find_by_email(email_nutrizionista,session)
        if nutrizionista is None:
            session.close()
            return {"message": "Nutrizionista non presente nel database"}, 404
        id_nutrizionista=nutrizionista.id_nutrizionista#serve salvarlo per mandarlo con kafka
        session.close()
        message={"id_paziente":id_paziente,"id_nutrizionista":id_nutrizionista}
        send_kafka_message("dietitian.getPaziente.request",message)
        response=wait_for_kafka_response(["dietitian.getPaziente.success", "dietitian.getPaziente.failed"])
        return response
        


   