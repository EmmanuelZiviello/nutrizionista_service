from F_taste_nutrizionista.ma import ma
from F_taste_nutrizionista.models.intolleranza import IntolleranzaModel

class IntolleranzaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IntolleranzaModel
        load_instance = True
        include_fk = True