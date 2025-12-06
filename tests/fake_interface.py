class fakeInterface:
    def __init__(self):
        self.messages = []
        self.callback = None

    def afficher(self, msg):
        self.messages.append(msg)

    def afficherItalique(self, msg):
        self.messages.append(msg)

    def attendre_reponse(self, func):
        self.callback = func