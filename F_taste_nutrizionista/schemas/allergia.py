from F_taste_nutrizionista.ma import ma
from F_taste_nutrizionista.models.allergia import AllergiaModel

class AllergiaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllergiaModel
        load_instance = True
        include_fk = True