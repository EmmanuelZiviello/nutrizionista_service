from flask_restx import Resource
from F_taste_nutrizionista.namespaces import nutrizionista_ns
from F_taste_nutrizionista.services.nutrizionista_service import NutrizionistaService
from F_taste_nutrizionista.utils.jwt_custom_decorators import nutrizionista_required
from flask_jwt_extended import  get_jwt_identity
from flask import request



class Pazienti(Resource):
    @nutrizionista_required()
    @nutrizionista_ns.doc('ricevi tutti i pazienti del nutrizionista')
    def get(self):
        email_nutrizionista = get_jwt_identity()
        return NutrizionistaService.get_pazienti(email_nutrizionista)