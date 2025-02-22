from F_taste_nutrizionista.models.paziente import PazienteModel
from F_taste_nutrizionista.models.nutrizionista import NutrizionistaModel

def check_nutrizionista(paziente : PazienteModel, nutrizionista : NutrizionistaModel):
    if paziente.fk_nutrizionista == nutrizionista.id_nutrizionista:
        return True
    return False
