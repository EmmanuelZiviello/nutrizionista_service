from F_taste_nutrizionista.ma import ma
from F_taste_nutrizionista.models.patologia import PatologiaModel


class PatologiaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatologiaModel
        load_instance = True
        include_fk = False