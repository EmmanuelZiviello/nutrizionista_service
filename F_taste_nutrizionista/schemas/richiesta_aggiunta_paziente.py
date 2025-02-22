from F_taste_nutrizionista.ma import ma
from F_taste_nutrizionista.models.richiesta_aggiunta_paziente import RichiestaAggiuntaPazienteModel
from marshmallow import fields
from F_taste_nutrizionista.schemas.nutrizionista import NutrizionistaSchema

class RichiestaAggiuntaPazienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RichiestaAggiuntaPazienteModel
        load_instance = True
        # sqla_session = db.session
        include_relationship = True
        

    nutrizionista = fields.Nested(NutrizionistaSchema, only=['id_nutrizionista', 'nome', 'cognome', 'email', 'link_informativa'], dump_only=True)