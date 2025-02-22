from flask import request
from flask_jwt_extended import get_jwt_identity
from F_taste_nutrizionista.repositories.nutrizionista_repository import NutrizionistaRepository
from flask_restx import fields
from F_taste_nutrizionista.namespaces import nutrizionista_ns
from F_taste_nutrizionista.db import get_session
from F_taste_nutrizionista.schemas.paziente import PazienteSchema

post_link_informativa = nutrizionista_ns.model('post_link_informativa', {
    'link_informativa': fields.String(required = True),
}, strict = True)

pazienti_schema = PazienteSchema(many=True, only=['id_paziente'])

class NutrizionistaService:

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