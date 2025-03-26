from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_restx import Resource, fields
from F_taste_nutrizionista.namespaces import nutrizionista_ns

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





class Paziente(Resource):
   
    
    @nutrizionista_required()
    @nutrizionista_ns.expect(modify_paziente_from_nutrizionista)
    @nutrizionista_ns.doc('modifica paziente')
    def put(self):
        s_paziente = request.get_json()
        email_nutrizionista = get_jwt_identity()
        
        if "id_paziente" not in s_paziente:
            return {"esito modifica_paziente":"id_paziente non presente"}, 404

        return PazienteService.modifica_paziente(email_nutrizionista, s_paziente)
    
    
    @nutrizionista_required()
    @nutrizionista_ns.doc('recupera paziente', params={'id_paziente': 'PAZ1234'})
    def get(self):
        patient_args = request.args
        email_nutrizionista = get_jwt_identity()
        
        if "id_paziente" not in patient_args:
            return {"esito get_paziente_info":"id_paziente non presente"}, 404

        return PazienteService.get_paziente_info(patient_args['id_paziente'], email_nutrizionista)

        