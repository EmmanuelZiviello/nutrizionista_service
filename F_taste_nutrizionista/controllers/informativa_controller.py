from flask_restx import Resource
from F_taste_nutrizionista.namespaces import nutrizionista_ns
from F_taste_nutrizionista.services.informativa_service import InformativaService
from F_taste_nutrizionista.services.nutrizionista_service import NutrizionistaService
from F_taste_nutrizionista.utils.jwt_custom_decorators import nutrizionista_required

class InformativaPrivacy(Resource):

    @nutrizionista_ns.doc(description="This GET method returns the privacy policy for the Nutritionists")
    def get(self):
        return InformativaService.get_privacy_policy()


    @nutrizionista_required()
    @nutrizionista_ns.doc(description="This POST method associates a privacy policy link with the Nutritionist's account")
    def post(self):
        return NutrizionistaService.associate_link_informativa()