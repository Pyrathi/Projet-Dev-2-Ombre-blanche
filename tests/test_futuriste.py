import unittest
import sys
import os

# Ajouter le dossier racine du projet au Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mondes.futuriste import MondeFuturiste


class FakeInterface:
    def afficher(self, message):
        pass
class FakeJeu:
    def __init__(self):
        self.interface = FakeInterface()
class TestAjouterHistorique(unittest.TestCase):
    def test_ajouter_historique_ajoute_element(self):
        # un monde futuriste avec un historique vide
        jeu = FakeJeu()
        monde = MondeFuturiste(jeu)
        monde.historique = []

        # on ajoute un élément à l'historique
        monde.ajouter_historique("1A")

        # on testel'historique contient l'élément ajouté
        self.assertEqual(len(monde.historique), 1)
        self.assertEqual(monde.historique[0], "1A")
   
    def test_fut2a_ajoute_historique(self):
        # un monde futuriste avec un historique vide
        jeu = FakeJeu()
        monde = MondeFuturiste(jeu)
        monde.historique = []

        # On remplace la méthode attente pour éviter blocage
        monde.interface.attendre_reponse = lambda f: None

        # on appelle la fonction fut2A
        monde.fut2a()

        # THEN
        self.assertIn("2A", monde.historique)

if __name__ == "__main__":
    unittest.main()
