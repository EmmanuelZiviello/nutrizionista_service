from F_taste_nutrizionista.ma import ma
from F_taste_nutrizionista.models.patologia_paziente import PatologiaPaziente
from marshmallow import fields

class PazientePatologiaSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        meta = PatologiaPaziente
        load_instance = True

    id_patologia = fields.Integer(required=True)
    id_paziente = fields.String(required=True)


