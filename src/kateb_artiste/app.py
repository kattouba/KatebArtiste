import os
import random
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
from android.media import SoundPool

class KatebArtiste(toga.App):
    def startup(self):
        # Initialiser la fenêtre principale
        self.main_window = toga.MainWindow(title="Kateb Artiste!")

        # Charger les données
        self.data = self.load_data()
        if not self.data:
            self.main_window.info_dialog("Erreur", "Aucune donnée valide trouvée dans le fichier CSV.")
            return

        self.current_painting = None
        self.score = 0
        self.question_count = 0

        # Créer les conteneurs principaux
        self.main_box = self.create_main_box()
        self.info_box = self.create_info_box()

        # Définir le contenu de la fenêtre principale
        self.main_window.content = self.main_box
        self.main_window.show()

        # Initialiser SoundPool pour les sons
        self.sound_pool = SoundPool.Builder().setMaxStreams(1).build()
        self.correct_sound = self.load_sound("correct.mp3")
        self.wrong_sound = self.load_sound("wrong.mp3")

        # Afficher la première question
        self.show_painting_question()

    def resource_path(self, filename):
        """Retourne le chemin absolu vers une ressource"""
        base_path = os.path.abspath(os.path.dirname(__file__))  # Chemin de base du fichier Python
        return os.path.join(base_path, "resources", filename)  # Accès au fichier dans le dossier resources

    def load_sound(self, filename):
        """Charge un fichier audio."""
        sound_path = self.resource_path(filename)
        if os.path.exists(sound_path):
            return self.sound_pool.load(sound_path, 1)
        else:
            print(f"Erreur de chargement du son : {filename}")
            return None

    def create_main_box(self):
        """Crée la boîte principale pour l'interface utilisateur."""
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Créer une boîte pour centrer l'image
        image_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=10))
        self.painting_image = toga.ImageView(style=Pack(height=300, width=300, alignment=CENTER))  # Définir la largeur de l'image
        image_box.add(self.painting_image)

        self.result_label = toga.Label("", style=Pack(padding=(0, 5), text_align=CENTER))

        main_box.add(image_box)  # Ajouter la boîte contenant l'image
        main_box.add(self.result_label)

        self.buttons = []
        for _ in range(4):
            button = toga.Button("Option", on_press=self.check_artist_answer, style=Pack(padding=5, flex=1))
            self.buttons.append(button)
            main_box.add(button)

        return main_box

    def create_info_box(self):
        """Crée la boîte d'information pour afficher les détails du tableau."""
        info_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.info_label = toga.MultilineTextInput(readonly=True, style=Pack(padding=10, flex=1))
        self.next_button = toga.Button("Question suivante", on_press=self.show_painting_question, style=Pack(padding=5))
        info_box.add(self.info_label)
        info_box.add(self.next_button)

        return info_box

    def load_data(self):
        """Charge les données des peintures depuis le fichier CSV."""
        data = []
        try:
            csv_path = self.resource_path("paintings.csv")
            print(f"Chemin du fichier CSV : {csv_path}")

            # Vérification si le fichier existe
            if not os.path.exists(csv_path):
                print(f"Fichier CSV non trouvé : {csv_path}")
                return data

            with open(csv_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print(f"Lignes lues : {lines}")  # Debug : Afficher les lignes lues

                headers = lines[0].strip().split(",")
                print(f"En-têtes du CSV : {headers}")  # Debug : Afficher les en-têtes

                for index, line in enumerate(lines[1:], start=1):  # Ajouter un index pour chaque ligne
                    parts = line.strip().split(",")
                    print(f"Ligne lue : {parts}")  # Debug : Afficher chaque ligne lue

                    if len(parts) == 4 and all(parts):
                        data.append({
                            "index": index,  # Ajout de l'index
                            "title": parts[0],
                            "artist": parts[1],
                            "style": parts[2],
                            "century": parts[3]
                        })
                    else:
                        print(f"Ligne ignorée : {parts}")

                print(f"Données chargées : {data}")
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
        return data

    def play_sound(self, correct=True):
        """Joue un son en fonction de la réponse."""
        if correct:
            self.sound_pool.play(self.correct_sound, 1.0, 1.0, 1, 0, 1.0)
        else:
            self.sound_pool.play(self.wrong_sound, 1.0, 1.0, 1, 0, 1.0)

    def show_painting_question(self, widget=None):
        """Affiche une nouvelle question avec une peinture aléatoire."""
        if self.question_count >= 10:
            self.main_window.info_dialog("Quiz terminé", f"Votre score final est de {self.score}/20 !")
            self.exit()
            return

        self.question_count += 1

        self.current_painting = random.choice(self.data)
        image_filename = f"{self.current_painting['index']}.jpg"
        image_path = self.resource_path(os.path.join("images", image_filename))
        print(f"Chemin de l'image : {image_path}")

        if not os.path.exists(image_path):
            self.main_window.info_dialog("Erreur", f"Image non trouvée: {image_path}")
            return

        self.painting_image.image = image_path
        self.result_label.text = "Qui est l'artiste de ce tableau ?"

        # Afficher uniquement le titre dans la réponse
        options = {self.current_painting["artist"]}  # Set pour éviter les doublons
        while len(options) < 4:
            options.add(random.choice([entry["artist"] for entry in self.data if entry["artist"] != self.current_painting["artist"]]))

        options = list(options)  # Convertir en liste pour pouvoir mélanger
        random.shuffle(options)

        for button, option in zip(self.buttons, options):
            button.text = option
            button.on_press = self.check_artist_answer
            button.enabled = True

        self.main_window.content = self.main_box

    def check_artist_answer(self, widget):
        """Vérifie la réponse de l'utilisateur concernant l'artiste."""
        if widget.text == self.current_painting["artist"]:
            self.score += 1
            self.play_sound(correct=True)
            self.result_label.text = "Bonne réponse ! Quel est le style de ce tableau ?"

            # Ajouter l'option correcte parmi les réponses possibles
            options = {self.current_painting["style"]}  # Set pour éviter les doublons
            while len(options) < 4:
                options.add(random.choice([entry["style"] for entry in self.data if entry["style"] != self.current_painting["style"]]))

            options = list(options)  # Convertir en liste pour pouvoir mélanger
            random.shuffle(options)

            for button, option in zip(self.buttons, options):
                button.text = option
                button.on_press = self.check_style_answer
                button.enabled = True
        else:
            self.play_sound(correct=False)
            self.result_label.text = f"Mauvaise réponse. L'artiste était {self.current_painting['artist']}."
            self.show_info()

    def check_style_answer(self, widget):
        """Vérifie la réponse de l'utilisateur concernant le style."""
        if widget.text == self.current_painting["style"]:
            self.score += 1
            self.play_sound(correct=True)
            self.result_label.text = "Bonne réponse !"
        else:
            self.play_sound(correct=False)
            self.result_label.text = f"Mauvaise réponse. Le style était {self.current_painting['style']}."
        
        self.show_info()

    def show_info(self):
        """Affiche les informations sur la peinture."""
        info_text = f"Artiste : {self.current_painting['artist']}\nStyle : {self.current_painting['style']}\nSiècle : {self.current_painting['century']}\nTitre : {self.current_painting['title']}"
        self.info_label.value = info_text
        self.main_window.content = self.info_box

def main():
    return KatebArtiste()
