from F_taste_nutrizionista.repositories.informativa_repository import InformativaRepository

class InformativaService:

    @staticmethod
    def get_privacy_policy():
        informativa = InformativaRepository.get_last_privacy_policy_by_type("nutrizionista")
        
        if informativa is None:
            return {"message": ""}, 204

        return {
            'informativa': informativa.testo_informativa,
            'link_informativa': informativa.link_inf_estesa
        }, 200
