from tests.fake_interface import fakeInterface
from mondes.medieval import MondeMedieval
class FakeJeu:
    def __init__(self):
        self.interface = fakeInterface()
        self.nom = "Test"
        self.inventaire = []
        self.sort=[]
        self.pnj_allie = []
        self.marche = iter(["Un bruit de pas...", "Le vent souffle...", "Rien à signaler."])


def test_ajout_epee_dans_inventaire():
    
    jeu = FakeJeu()
    monde = MondeMedieval(jeu)
    monde.quete_loup()  
    assert "epee" in jeu.inventaire, "L'épée devrait être ajoutée à l'inventaire"

def test_ajout_cle_inventaire():
    jeu =FakeJeu()
    monde=MondeMedieval(jeu)
    monde.combat_loup2()
    assert "cle" in jeu.inventaire, "La clé devrait être ajoutée à l'inventaire"

def test_ajout_soin_sort():
    jeu=FakeJeu()
    monde=MondeMedieval(jeu)
    monde.porte_ouverte()
    assert "soin" in jeu.sort, "Le sort de soin devrait être ajouté à la panoplie"