from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_restx import Resource, fields
from F_taste_nutrizionista.namespaces import nutrizionista_ns
from F_taste_nutrizionista.schemas.paziente import PazienteSchema
from F_taste_nutrizionista.utils.jwt_custom_decorators import nutrizionista_required
from F_taste_nutrizionista.services.paziente_service import PazienteService

get_allergie_request = nutrizionista_ns.model('request allergie paziente', {
    "id_paziente": fields.String(description="id paziente", example="PAZ1234"),
}, strict=True)

get_paziente = nutrizionista_ns.model('paziente da visualizzare', {
    'id_paziente': fields.String('id paziente', required=True),
}, strict = True)

modify_paziente_from_nutrizionista = nutrizionista_ns.model('paziente da modificare', {
    'id_paziente': fields.String('id paziente da modificare', required=True)
})

paziente_schema_put = PazienteSchema(exclude=['email','password'], partial=['fk_nutrizionista'])

paziente_schema_get = PazienteSchema(only=['id_paziente'])

class DiseaseDelPazienteController(Resource):

    @nutrizionista_required()
    @nutrizionista_ns.doc("ricevi le condizioni associate ad un paziente", params={'id_paziente': 'PAZ1234'})
    def get(self):
        request_args = request.args
        email_nutrizionista = get_jwt_identity()

        paziente_schema_validate = PazienteSchema(only=['id_paziente'])
        validation_errors = paziente_schema_validate.validate(request_args)

        if validation_errors:
            return validation_errors, 400

        return PazienteService.get_conditions(request_args["id_paziente"], email_nutrizionista)

class Paziente(Resource):
    @nutrizionista_required()
    @nutrizionista_ns.expect(get_paziente, validate=True)
    @nutrizionista_ns.doc('aggiungi paziente al nutrizionista')
    def post(self):
        return PazienteService.aggiungi_paziente()
    


    @nutrizionista_required()
    @nutrizionista_ns.expect(get_paziente)
    @nutrizionista_ns.doc('rimuove il paziente dalla lista del nutrizionista')
    def delete(self):
        request_dict = request.get_json()
        email_nutrizionista = get_jwt_identity()

        return  PazienteService.rimuovi_paziente(request_dict, email_nutrizionista)
    


    @nutrizionista_required()
    @nutrizionista_ns.expect(modify_paziente_from_nutrizionista)
    @nutrizionista_ns.doc('modifica paziente')
    def put(self):
        s_paziente = request.get_json()
        email_nutrizionista = get_jwt_identity()
        
        validation_errors = paziente_schema_put.validate(s_paziente)
        if validation_errors:
            return validation_errors, 400

        return PazienteService.modifica_paziente(email_nutrizionista, s_paziente)
    

    @nutrizionista_required()
    @nutrizionista_ns.doc('recupera paziente', params={'id_paziente': 'PAZ1234'})
    def get(self):
        patient_args = request.args
        email_nutrizionista = get_jwt_identity()

        validation_errors = paziente_schema_get.validate(patient_args)
        if validation_errors:
            return validation_errors, 400

        return PazienteService.get_paziente_info(patient_args['id_paziente'], email_nutrizionista)

        