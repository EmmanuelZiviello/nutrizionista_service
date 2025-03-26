from flask_restx import Resource, fields
from F_taste_nutrizionista.namespaces import nutrizionista_ns
from F_taste_nutrizionista.services.nutrizionista_service import NutrizionistaService
from F_taste_nutrizionista.services.paziente_service import PazienteService
from F_taste_nutrizionista.utils.jwt_custom_decorators import nutrizionista_required
from flask_jwt_extended import  get_jwt_identity
from flask import request


get_paziente = nutrizionista_ns.model('paziente da visualizzare', {
    'id_paziente': fields.String('id paziente', required=True),
}, strict = True)

class Pazienti(Resource):
    @nutrizionista_required()
    @nutrizionista_ns.doc('ricevi tutti i pazienti del nutrizionista')
    def get(self):
        email_nutrizionista = get_jwt_identity()
        return NutrizionistaService.get_pazienti(email_nutrizionista)
    
    @nutrizionista_required()
    @nutrizionista_ns.expect(get_paziente)
    @nutrizionista_ns.doc('rimuove il paziente dalla lista del nutrizionista')
    def delete(self):
        patient_json = request.get_json()
        email_nutrizionista = get_jwt_identity()
        return  PazienteService.rimuovi_paziente(patient_json, email_nutrizionista)
    
    @nutrizionista_required()
    @nutrizionista_ns.expect(get_paziente, validate=True)
    @nutrizionista_ns.doc('aggiungi paziente al nutrizionista')
    def post(self):
        patient_json=request.get_json()
        email_nutrizionista = get_jwt_identity()
        return PazienteService.aggiungi_paziente(patient_json,email_nutrizionista)