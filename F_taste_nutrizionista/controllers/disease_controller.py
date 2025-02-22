from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import get_jwt_identity
from F_taste_nutrizionista.namespaces import nutrizionista_ns
from F_taste_nutrizionista.utils.jwt_custom_decorators import nutrizionista_required
from F_taste_nutrizionista.services.disease_service import DiseaseService

disease_request_model = nutrizionista_ns.model('disease', {
    "disease": fields.String(description="Patologia del paziente", example="Diabete tipo II", required=True),
    "fk_paziente": fields.String(description="ID paziente", example="PAZ1234", required=True)
}, strict=True)


class DiseaseController(Resource):

    @nutrizionista_required()
    @nutrizionista_ns.expect(disease_request_model)
    @nutrizionista_ns.doc('Inserisci una condizione al paziente')
    def post(self):
        data = request.get_json()
        user_email = get_jwt_identity()

        return DiseaseService.add_disease_to_patient(user_email, data['fk_paziente'], data['disease'])

    
    @nutrizionista_required()
    @nutrizionista_ns.doc('Elimina una patologia al paziente', params={'fk_paziente': 'PAZ1234', 'patologia': 'una_patologia'})
    def delete(self):
        data = request.args
        validation_errors = disease_request_model.validate(data)
        if validation_errors:
            return validation_errors, 400

        return DiseaseService.delete_disease(
            nutrizionista_email=get_jwt_identity(),
            paziente_id=data['fk_paziente'],
            disease=data['disease']
        )

class AllDiseaseController(Resource):
  

    @nutrizionista_required()
    @nutrizionista_ns.doc('Ottieni tutte le patologie')
    def get(self):
        

        try:
            # Usiamo il service per ottenere i dati elaborati
            data = DiseaseService.process_data()

            # Se i dati sono validi, restituiamo la risposta con codice 200
            if data:
                return data, 200

            # Altrimenti restituiamo una lista vuota
            return [], 200

        except Exception:
            return {"message": "Internal Server Error"}, 500
