from F_taste_nutrizionista.ma import ma
from F_taste_nutrizionista.models.nutrizionista import NutrizionistaModel
from marshmallow import fields

class NutrizionistaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NutrizionistaModel
        load_instance = True
    
    email = fields.Email(required=True)