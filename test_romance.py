import unittest
from main import Jeu   

class FakeInterface:
    def afficher(self, message):
        pass

    def attendre_reponse(self, callback):
        pass

class TestRomance(unittest.TestCase):

    def setUp(self):
        self.jeu = Jeu(FakeInterface())
        self.jeu.a_demande_si_ca_va = False
        self.jeu.affection.valeur = 0
#Test vérifiant que le choix 1 est refusé lorsque la variable self.a_demande_si_ca_va est False dans la fonction romance_S2bis_reponse()
    def test_choix_1_indisponible(self):
        try:
            result = self.jeu.romance_S2bis_reponse(1)
        except Exception as e:
            self.fail(f"Erreur détectée : {e}")

        self.assertEqual(self.jeu.affection.valeur, 0,
            "Le choix 1 interdit ne doit pas augmenter l'affection")
        self.assertIsNone(result, "Le choix 1 interdit doit renvoyer None")

#Test vérifiant que le choix 1 est accepté lorsque la variable self.a_demande_si_ca_va est True romance_S2bis_reponse()
    def test_choix_1_disponible(self):
        self.jeu.a_demande_si_ca_va = True
        result = self.jeu.romance_S2bis_reponse(1)
        self.assertEqual(self.jeu.affection.valeur, 10)
        self.assertIsNone(result)

# Test que le choix 2 dans S2bis diminue correctement l'affection et ne renvoie rien
    def test_choix_2(self):
        self.jeu.affection.valeur = 10
        result = self.jeu.romance_S2bis_reponse(2)
        self.assertEqual(self.jeu.affection.valeur, 5)
        self.assertIsNone(result)


