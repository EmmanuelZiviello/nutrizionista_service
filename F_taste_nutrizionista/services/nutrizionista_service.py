from flask import request
from flask_jwt_extended import get_jwt_identity
from F_taste_nutrizionista.repositories.nutrizionista_repository import NutrizionistaRepository
from flask_restx import fields
from F_taste_nutrizionista.namespaces import nutrizionista_ns
from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.schemas.paziente import PazienteSchema
from F_taste_nutrizionista.schemas.nutrizionista import NutrizionistaSchema

from F_taste_nutrizionista.utils.hashing_password import hash_pwd,check_pwd
from F_taste_nutrizionista.utils.jwt_token_factory import JWTTokenFactory


post_link_informativa = nutrizionista_ns.model('post_link_informativa', {
    'link_informativa': fields.String(required = True),
}, strict = True)

pazienti_schema = PazienteSchema(many=True, only=['id_paziente'])

nutrizionista_schema = NutrizionistaSchema()

jwt_factory = JWTTokenFactory()

class NutrizionistaService:


    @staticmethod
    def login_nutrizionista(s_nutrizionista):
        if "email" not in s_nutrizionista or "password" not in s_nutrizionista:
            return {"esito_login": "Dati mancanti"}, 400
        session=get_session('dietitian')
        email_nutrizionista = s_nutrizionista["email"]
        password = s_nutrizionista["password"]
        nutrizionista=NutrizionistaRepository.find_by_email(email_nutrizionista,session)
        if nutrizionista is None:
            session.close()
            return {"esito_login": "Nutrizionista non trovato"}, 401
        if check_pwd(password, nutrizionista.password):
            session.close()
            return {
                "esito_login": "successo",
                "access_token": jwt_factory.create_access_token(email_nutrizionista, 'dietitian'),
                "refresh_token": jwt_factory.create_refresh_token(email_nutrizionista, 'dietitian'),
                "id_paziente": nutrizionista.id_nutrizionista
            }, 200

        session.close()
        return {"esito_login": "password errata"}, 401

    
    @staticmethod
    def register_nutrizionista(s_nutrizionista):
        session=get_session('admin')
        # Validazione dati in ingresso
        validation_errors = nutrizionista_schema.validate(s_nutrizionista)
        if validation_errors:
            session.close()
            return validation_errors, 400
        # Verifica se l'email esiste già
        if NutrizionistaRepository.find_by_email(s_nutrizionista['email'], session) is not None:
            session.close()
            return {"esito_registrazione": "email già utilizzata"}, 409
         # Carica il nutrizionista nel modello
        nutrizionista = nutrizionista_schema.load(s_nutrizionista,session=session)
        nutrizionista.password = hash_pwd(s_nutrizionista['password'])
        # Aggiungi il nutrizionista al database
        NutrizionistaRepository.add(nutrizionista, session)
        session.close()
        return {'message': 'registrazione avvenuta con successo'}, 201

        
        

   

    @staticmethod
    def associate_link_informativa():
        # Recuperiamo il JSON dalla richiesta
        session=get_session('dietitian')
        json = request.get_json()

        # Validiamo il JSON
        validation_errors = post_link_informativa.validate(json)
        if validation_errors:
            session.close()
            return validation_errors, 404

        # Recuperiamo l'ID del nutrizionista
        email = get_jwt_identity()
        nutrizionista = NutrizionistaRepository.find_by_email(email)

        # Se il nutrizionista non esiste, gestiamo l'errore
        if nutrizionista is None:
            session.close()
            return {"message": "Nutrizionista non valido. Riprovare."}, 204

        # Aggiorniamo il link informativa
        NutrizionistaRepository.update_link_informativa(nutrizionista, json["link_informativa"])
        session.close()
        # Ritorniamo il messaggio di successo
        return {"message": "Associazione link informativa all'account eseguita con successo."}, 201

    @staticmethod
    def get_pazienti(email_nutrizionista):
      
        session = get_session('dietitian')
        nutrizionista = NutrizionistaRepository.find_by_email(email_nutrizionista, session)
        
        if nutrizionista is None:
            session.close()
            return {"message": "Nutrizionista non presente nel db"}, 404
        
        pazienti_data = nutrizionista.pazienti
        output_richiesta={"pazienti": pazienti_schema.dump(pazienti_data)}, 200
        session.close()
        return output_richiesta