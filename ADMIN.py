from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

class HomeScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        
        self.add_widget(Image(source="ECC.jpg"))

        student_button = Button(text="Élève",size_hint=(0.5,0.2))
        student_button.bind(on_press=self.on_student_click)
        self.add_widget(student_button)
        student_button.pos_hint={'center_x': 0.5, 'center_y': 0.5}


        teacher_button = Button(text="Enseignant",size_hint=(0.5,0.2))
        teacher_button.bind(on_press=self.on_teacher_click)
        self.add_widget(teacher_button)
        teacher_button.pos_hint={'center_x': 0.5, 'center_y': 0.5}


    def on_student_click(self, instance):
        self.clear_widgets()
        self.add_widget(StudentScreen())

    def on_teacher_click(self, instance):
        self.clear_widgets()
        self.add_widget(TeacherScreen())


class StudentScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(StudentScreen, self).__init__(**kwargs)
        self.orientation = "vertical"

        add_button = Button(text="Ajouter")
        add_button.bind(on_press=self.open_add_window)
        self.add_widget(add_button)

        modify_button = Button(text="Modifier")
        modify_button.bind(on_press=self.open_modify_window)
        self.add_widget(modify_button)

        self.liste_eleves = self.charger_liste_eleves()

        search_button = Button(text="Chercher")
        search_button.bind(on_press=self.open_search_window)
        self.add_widget(search_button)

        
        

        create_account_button = Button(text="Créer un compte élève")
        create_account_button.bind(on_press=self.open_create_account_window)
        self.add_widget(create_account_button)

        GoBack_button = Button(text="retour",size_hint=(0.5, 0.2))
        GoBack_button.bind(on_press=self.GoBack_click)
        self.add_widget(GoBack_button)
        GoBack_button.pos_hint={'center_x': 0.5, 'center_y': 0.5}

    def open_add_window(self, instance):
        self.clear_widgets()
        self.add_widget(GestionEleves())


    def charger_liste_eleves(self):
        try:
            with open("liste_eleves.txt", "r") as file:
                eleves = []
                for line in file.readlines():
                    nom, prenom, niveau = line.strip().split(',')
                    eleve = {'Nom': nom, 'Prénom': prenom, 'niveau': niveau}
                    eleves.append(eleve)
                return eleves
        except FileNotFoundError:
            print("Fichier introuvable. La liste d'élèves est vide.")
            return []

    def enregistrer_liste_eleves(self):
        with open("liste_eleves.txt", "w") as file:
            for eleve in self.liste_eleves:
                file.write(f"{eleve['Nom']},{eleve['Prénom']},{eleve['niveau']}\n")

    def open_modify_window(self, instance):
        content = BoxLayout(orientation='vertical')
        self.popup = Popup(title="Modifier Élève", content=content, size_hint=(None, None), size=(500, 400))

        self.label_nom = Label(text="Nom de l'élève à modifier:")
        self.input_nom = TextInput(multiline=False)

        self.label_nnom = Label(text="Nouveau Nom:")
        self.input_nnom = TextInput(multiline=False)

        self.label_prenom = Label(text="Prénom de l'élève à modifier:")
        self.input_prenom = TextInput(multiline=False)

        self.label_nprenom = Label(text="Nouveau Prénom:")
        self.input_nprenom = TextInput(multiline=False)

        self.label_niveau = Label(text="Nouveau niveau :")
        self.input_niveau = TextInput(multiline=False)

        modify_button = Button(text="Modifier")
        modify_button.bind(on_press=self.modifier_eleve)

        content.add_widget(self.label_nom)
        content.add_widget(self.input_nom)
        content.add_widget(self.label_nnom)
        content.add_widget(self.input_nnom)
        content.add_widget(self.label_prenom)
        content.add_widget(self.input_prenom)
        content.add_widget(self.label_nprenom)
        content.add_widget(self.input_nprenom)
        content.add_widget(self.label_niveau)
        content.add_widget(self.input_niveau)
        content.add_widget(modify_button)

        self.popup.open()

    def modifier_eleve(self, instance):
        nom_a_modifier = self.input_nom.text
        prenom_a_modifier = self.input_prenom.text
        nouveau_niveau = self.input_niveau.text
        

        for eleve in self.liste_eleves:
            if eleve['Nom'] == nom_a_modifier and eleve['Prénom'] == prenom_a_modifier:
                eleve['niveau'] = nouveau_niveau
                eleve['Nom'] = self.input_nnom.text  # Mise à jour du nom
                eleve['Prénom'] = self.input_nprenom.text  # Mise à jour du prénom
                self.enregistrer_liste_eleves()  # Mettre à jour le fichier après la modification
                print(f"Données de l'élève {nom_a_modifier} {prenom_a_modifier} modifiées.")
                self.popup.dismiss()
                break



    def open_search_window(self, instance):
        content = BoxLayout(orientation='vertical')
        self.popup = Popup(title="Chercher Élève", content=content, size_hint=(None, None), size=(300, 250))

        self.label = Label(text="Entrez le nom de l'élève à rechercher:")
        self.input_nom = TextInput(multiline=False)
        chercher_button = Button(text="Chercher")
        chercher_button.bind(on_press=self.chercher_eleve)

        content.add_widget(self.label)
        content.add_widget(self.input_nom)
        content.add_widget(chercher_button)

        self.popup.open()

    def chercher_eleve(self, instance):
        nom_recherche = self.input_nom.text
        try:
            with open("liste_eleves.txt", "r") as file:
                lignes = file.readlines()
                eleve_trouve = False

                for ligne in lignes:
                    infos_eleve = ligne.strip().split(",")
                    if infos_eleve[0].lower() == nom_recherche.lower():
                        self.popup.dismiss()
                        popup = Popup(title="Résultat de la recherche", content=Label(text=f"Élève trouvé : {infos_eleve[1]} {infos_eleve[0]}, niveau : {infos_eleve[2]}"), size_hint=(None, None), size=(400, 200))
                    
                        btn_supprimer = Button(text="Supprimer", size_hint=(None, None), size=(100, 50))
                        btn_supprimer.bind(on_press=lambda instance, nom=infos_eleve[0], prenom=infos_eleve[1]: self.supprimer_eleve(nom, prenom))

                        layout = BoxLayout(orientation='vertical')
                        layout.add_widget(Label(text=f"Élève trouvé : {infos_eleve[1]} {infos_eleve[0]}, niveau : {infos_eleve[2]}"))
                        layout.add_widget(btn_supprimer)
                    
                        popup.content = layout
                        popup.open()
                        eleve_trouve = True
                        break

                if not eleve_trouve:
                    self.popup.dismiss()
                    popup = Popup(title="Résultat de la recherche", content=Label(text="Élève non trouvé."), size_hint=(None, None), size=(300, 200))
                    popup.open()
        except FileNotFoundError:
            self.popup.dismiss()
            popup = Popup(title="Erreur", content=Label(text="Fichier non trouvé."), size_hint=(None, None), size=(300, 200))
            popup.open()

    def supprimer_eleve(self, nom, prenom):
        try:
            with open("liste_eleves.txt", "r") as file:
                lignes = file.readlines()
        
            with open("liste_eleves.txt", "a") as file:
                for ligne in lignes:
                    infos_eleve = ligne.strip().split(",")
                    if infos_eleve[0] != nom or infos_eleve[1] != prenom:
                        file.write(ligne)
                    
            self.popup.dismiss()
            popup = Popup(title="Succès", content=Label(text="Élève supprimé avec succès."), size_hint=(None, None), size=(300, 200))
            popup.open()
        except FileNotFoundError:
            self.popup.dismiss()
            popup = Popup(title="Erreur", content=Label(text="Fichier non trouvé."), size_hint=(None, None), size=(300, 200))
            popup.open()



    def open_create_account_window(self, instance):
        content = BoxLayout(orientation='vertical')
        self.popup = Popup(title="Créer un Compte Élève", content=content, size_hint=(None, None), size=(400, 300))

        self.label_nom = Label(text="Nom de l'élève :")
        self.input_nom = TextInput(multiline=False)

        self.label_prenom = Label(text="Prénom de l'élève :")
        self.input_prenom = TextInput(multiline=False)

        self.label_niveau = Label(text="Niveau de l'élève :")
        self.input_niveau = TextInput(multiline=False)

        self.create_button = Button(text="Créer le compte")
        self.create_button.bind(on_press=self.creer_compte)

        content.add_widget(self.label_nom)
        content.add_widget(self.input_nom)
        content.add_widget(self.label_prenom)
        content.add_widget(self.input_prenom)
        content.add_widget(self.label_niveau)
        content.add_widget(self.input_niveau)
        content.add_widget(self.create_button)

        self.popup.open()

    def creer_compte(self, instance):
        nom = self.input_nom.text
        prenom = self.input_prenom.text
        niveau = self.input_niveau.text

        if nom and prenom and niveau:
            eleve = {'Nom': nom, 'Prénom': prenom, 'Niveau': niveau}
            self.enregistrer_compte_eleve(eleve)
            print(f"Le compte pour {nom} {prenom} a été créé.")
            self.popup.dismiss()
        else:
            print("Veuillez remplir tous les champs.")

    def enregistrer_compte_eleve(self, eleve):
        with open("comptes_eleves.txt", "a") as file:
            file.write(f"Nom: {eleve['Nom']}, Prénom: {eleve['Prénom']}, Niveau: {eleve['Niveau']}\n")

    
    def GoBack_click(self,instance):
        self.clear_widgets()
        self.add_widget(HomeScreen())

        # Add student-specific interface elements here
#AJOUTER ELEVE
class GestionEleves(BoxLayout):
    def __init__(self, **kwargs):
        super(GestionEleves, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.label_nom = Label(text="Nom de l'élève :")
        self.add_widget(self.label_nom)

        self.input_nom = TextInput(multiline=False)
        self.add_widget(self.input_nom)

        self.label_prenom = Label(text="Prénom de l'élève :")
        self.add_widget(self.label_prenom)

        self.input_prenom = TextInput(multiline=False)
        self.add_widget(self.input_prenom)

        self.label_niveau = Label(text="niveau de l'élève :")
        self.add_widget(self.label_niveau)

        self.input_niveau = TextInput(multiline=False)
        self.add_widget(self.input_niveau)

        self.ajouter_button = Button(text="Ajouter l'élève")
        self.ajouter_button.bind(on_press=self.ajouter_eleve)
        self.add_widget(self.ajouter_button)

        self.liste_eleves_label = Label(text="Liste des élèves :")
        self.add_widget(self.liste_eleves_label)

        GoBack_button = Button(text="retour",size_hint=(0.5, 0.2))
        GoBack_button.bind(on_press=self.GoBack_click)
        self.add_widget(GoBack_button)
        GoBack_button.pos_hint={'center_x': 0.5, 'center_y': 0.5}

        self.liste_eleves = []  # Initialise une liste vide pour stocker les élèves

    def ajouter_eleve(self, instance):
        # Récupère les informations de l'élève à partir des champs de saisie
        nom = self.input_nom.text
        prenom = self.input_prenom.text
        niveau = self.input_niveau.text

        # Vérifie si tous les champs sont remplis
        if nom and prenom and niveau:
            # Crée un dictionnaire pour représenter un élève avec les détails fournis
            eleve = {'Nom': nom, 'Prénom': prenom, 'niveau': niveau}
            self.liste_eleves.append(eleve)
            self.enregistrer_liste_eleves()
            self.afficher_liste_eleves()
        else:
            print("Veuillez remplir tous les champs.")

    def afficher_liste_eleves(self):
        # Affiche la liste de tous les élèves
        liste_texte = "Liste des élèves :\n"
        for eleve in self.liste_eleves:
            liste_texte += f"{eleve['Prénom']} {eleve['Nom']}, niveau : {eleve['niveau']}\n"

        self.liste_eleves_label.text = liste_texte

    def enregistrer_liste_eleves(self):
        # Enregistre la liste des élèves dans un fichier texte
        with open("liste_eleves.txt", "a") as file:
            for eleve in self.liste_eleves:
                file.write(f"{eleve['Nom']},{eleve['Prénom']},{eleve['niveau']}\n")

    def GoBack_click(self,instance):
        self.clear_widgets()
        self.add_widget(HomeScreen())
##################################################
        


class TeacherScreen(BoxLayout):  
    def __init__(self, **kwargs):
        super(TeacherScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        add_button = Button(text="Ajouter")
        add_button.bind(on_press=self.open_add_window)
        self.add_widget(add_button)

        modify_button = Button(text="Modifier")
        modify_button.bind(on_press=self.open_modify_window)
        self.add_widget(modify_button)

        self.liste_enseignants = self.charger_liste_enseignants()


        search_button = Button(text="Chercher")
        search_button.bind(on_press=self.open_search_window)
        self.add_widget(search_button)

        create_account_button = Button(text="Créer un compte enseignant")
        create_account_button.bind(on_press=self.open_create_account_window)
        self.add_widget(create_account_button)

        GoBack_button = Button(text="retour",size_hint=(0.5, 0.2))
        GoBack_button.bind(on_press=self.GoBack_click)
        self.add_widget(GoBack_button)
        GoBack_button.pos_hint={'center_x': 0.5, 'center_y': 0.5}
    
    def open_add_window(self, instance):
        self.clear_widgets()
        self.add_widget(GestionProf())


    def charger_liste_enseignants(self):
        try:
            with open("liste_enseignants.txt", "r") as file:
                enseignants = []
                for line in file.readlines():
                    nom, prenom, niveau = line.strip().split(',')
                    enseignant = {'Nom': nom, 'Prénom': prenom, 'niveau': niveau}
                    enseignants.append(enseignant)
                return enseignants
        except FileNotFoundError:
            print("Fichier introuvable. La liste d'élèves est vide.")
            return []

    def enregistrer_liste_enseignants(self):
        with open("liste_enseignants.txt", "w") as file:
            for enseignant in self.liste_enseignants:
                file.write(f"{enseignant['Nom']},{enseignant['Prénom']},{enseignant['niveau']}\n")


    def open_modify_window(self, instance):
        content = BoxLayout(orientation='vertical')
        self.popup = Popup(title="Modifier Élève", content=content, size_hint=(None, None), size=(500, 400))

        self.label_nom = Label(text="Nom de l'enseignant à modifier:")
        self.input_nom = TextInput(multiline=False)

        self.label_nnom = Label(text="Nouveau Nom:")
        self.input_nnom = TextInput(multiline=False)

        self.label_prenom = Label(text="Prénom de l'enseignant à modifier:")
        self.input_prenom = TextInput(multiline=False)

        self.label_nprenom = Label(text="Nouveau Prénom:")
        self.input_nprenom = TextInput(multiline=False)

        modify_button = Button(text="Modifier")
        modify_button.bind(on_press=self.modifier_enseignant)

        content.add_widget(self.label_nom)
        content.add_widget(self.input_nom)
        content.add_widget(self.label_nnom)
        content.add_widget(self.input_nnom)
        content.add_widget(self.label_prenom)
        content.add_widget(self.input_prenom)
        content.add_widget(self.label_nprenom)
        content.add_widget(self.input_nprenom)
        content.add_widget(modify_button)

        self.popup.open()

    def modifier_enseignant(self, instance):
        nom_a_modifier = self.input_nom.text
        prenom_a_modifier = self.input_prenom.text
        nnom=self.input_nnom.text
        nprenom=self.input_nprenom.text

        for enseignant in self.liste_enseignants:
            if enseignant['Nom'] == nom_a_modifier and enseignant['Prénom'] == prenom_a_modifier:
                enseignant['Nom'] = self.input_nnom.text  # Mise à jour du nom
                enseignant['Prénom'] = self.input_nprenom.text  # Mise à jour du prénom
                self.enregistrer_liste_enseignants()  # Mettre à jour le fichier après la modification
                print(f"Données de l'enseignant {nom_a_modifier} {prenom_a_modifier} modifiées.")
                self.popup.dismiss()
                break

    def open_search_window(self, instance):
        content = BoxLayout(orientation='vertical')
        self.popup = Popup(title="Chercher Enseignant", content=content, size_hint=(None, None), size=(300, 200))

        self.label = Label(text="Entrez le nom de l'enseignant à rechercher:")
        self.input_nom = TextInput(multiline=False)
        chercher_button = Button(text="Chercher")
        chercher_button.bind(on_press=self.chercher_enseignant)

        content.add_widget(self.label)
        content.add_widget(self.input_nom)
        content.add_widget(chercher_button)

        self.popup.open()

    def chercher_enseignant(self, instance):
        nom_recherche = self.input_nom.text
        try:
            with open("liste_enseignants.txt", "r") as file:
                lignes = file.readlines()
                enseignant_trouve = False

                for ligne in lignes:
                    infos_enseignant = ligne.strip().split(",")
                    if infos_enseignant[0].lower() == nom_recherche.lower():
                        self.popup.dismiss()
                        popup = Popup(title="Résultat de la recherche", content=Label(text=f"Enseignant trouvé : {infos_enseignant[1]} {infos_enseignant[0]}"), size_hint=(None, None), size=(400, 200))
                    
                        btn_supprimer = Button(text="Supprimer", size_hint=(None, None), size=(100, 50))
                        btn_supprimer.bind(on_press=lambda instance, nom=infos_enseignant[0], prenom=infos_enseignant[1]: self.supprimer_enseignant(nom, prenom))

                        layout = BoxLayout(orientation='vertical')
                        layout.add_widget(Label(text=f"Enseignant trouvé : {infos_enseignant[1]} {infos_enseignant[0]}"))
                        layout.add_widget(btn_supprimer)
                    
                        popup.content = layout
                        popup.open()
                        enseignant_trouve = True
                        break

                if not enseignant_trouve:
                    self.popup.dismiss()
                    popup = Popup(title="Résultat de la recherche", content=Label(text="Enseignant non trouvé."), size_hint=(None, None), size=(300, 200))
                    popup.open()
        except FileNotFoundError:
            self.popup.dismiss()
            popup = Popup(title="Erreur", content=Label(text="Fichier non trouvé."), size_hint=(None, None), size=(300, 200))
            popup.open()

    def supprimer_enseignant(self, nom, prenom):
        try:
            with open("liste_enseignants.txt", "r") as file:
                lignes = file.readlines()
        
            with open("liste_enseignants.txt", "w") as file:
                for ligne in lignes:
                    infos_enseignant = ligne.strip().split(",")
                    if infos_enseignant[0] != nom or infos_enseignant[1] != prenom:
                        file.write(ligne)
                    
            self.popup.dismiss()
            popup = Popup(title="Succès", content=Label(text="Enseignant supprimé avec succès."), size_hint=(None, None), size=(300, 200))
            popup.open()
        except FileNotFoundError:
            self.popup.dismiss()
            popup = Popup(title="Erreur", content=Label(text="Fichier non trouvé."), size_hint=(None, None), size=(300, 200))
            popup.open()




    def open_create_account_window(self, instance):
        content = BoxLayout(orientation='vertical')
        self.popup = Popup(title="Créer un Compte Enseignant", content=content, size_hint=(None, None), size=(400, 300))

        self.label_nom = Label(text="Nom de l'enseignant :")
        self.input_nom = TextInput(multiline=False)

        self.label_prenom = Label(text="Prénom de l'enseignant :")
        self.input_prenom = TextInput(multiline=False)

        self.create_button = Button(text="Créer le compte")
        self.create_button.bind(on_press=self.creer_compte)

        content.add_widget(self.label_nom)
        content.add_widget(self.input_nom)
        content.add_widget(self.label_prenom)
        content.add_widget(self.input_prenom)
        content.add_widget(self.create_button)

        self.popup.open()

    def creer_compte(self, instance):
        nom = self.input_nom.text
        prenom = self.input_prenom.text

        if nom and prenom:
            enseignant = {'Nom': nom, 'Prénom': prenom}
            self.enregistrer_compte_enseignant(enseignant)
            print(f"Le compte pour {nom} {prenom} a été créé.")
            self.popup.dismiss()
        else:
            print("Veuillez remplir tous les champs.")

    def enregistrer_compte_enseignant(self, enseignant):
        with open("comptes_enseignants.txt", "a") as file:
            file.write(f"Nom: {enseignant['Nom']}, Prénom: {enseignant['Prénom']}\n")

    
    def GoBack_click(self,instance):
        self.clear_widgets()
        self.add_widget(HomeScreen())

        # Add teacher-specific interface elements here
#######################################################
        
#AJOUTER ENSEIGNANT
class GestionProf(BoxLayout):
    def __init__(self, **kwargs):
        super(GestionProf, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.label_nom = Label(text="Nom de l'enseignant :")
        self.add_widget(self.label_nom)

        self.input_nom = TextInput(multiline=False)
        self.add_widget(self.input_nom)

        self.label_prenom = Label(text="Prénom de l'enseignant :")
        self.add_widget(self.label_prenom)

        self.input_prenom = TextInput(multiline=False)
        self.add_widget(self.input_prenom)

        self.ajouter_button = Button(text="Ajouter l'enseignant")
        self.ajouter_button.bind(on_press=self.ajouter_enseignant)
        self.add_widget(self.ajouter_button)

        self.liste_enseignants_label = Label(text="Liste des enseignants :")
        self.add_widget(self.liste_enseignants_label)

        GoBack_button = Button(text="retour",size_hint=(0.5, 0.2))
        GoBack_button.bind(on_press=self.GoBack_click)
        self.add_widget(GoBack_button)
        GoBack_button.pos_hint={'center_x': 0.5, 'center_y': 0.5}

        self.liste_enseignants = []  # Initialise une liste vide pour stocker les élèves

    def ajouter_enseignant(self, instance):
        # Récupère les informations de l'enseignant à partir des champs de saisie
        nom = self.input_nom.text
        prenom = self.input_prenom.text

        # Vérifie si tous les champs sont remplis
        if nom and prenom :
            # Crée un dictionnaire pour représenter un élève avec les détails fournis
            enseignant = {'Nom': nom, 'Prénom': prenom,}
            self.liste_enseignants.append(enseignant)
            self.enregistrer_liste_enseignants()
            self.afficher_liste_enseignants()
        else:
            print("Veuillez remplir tous les champs.")

    def afficher_liste_enseignants(self):
        # Affiche la liste de tous les élèves
        liste_texte = "Liste des enseignants :\n"
        for enseignant in self.liste_enseignants:
            liste_texte += f"{enseignant['Prénom']} {enseignant['Nom']}, \n"

        self.liste_enseignants_label.text = liste_texte

    def enregistrer_liste_enseignants(self):
        # Enregistre la liste des élèves dans un fichier texte
        with open("liste_enseignants.txt", "a") as file:
            for enseignant in self.liste_enseignants:
                file.write(f"{enseignant['Nom']},{enseignant['Prénom']},\n")

    def GoBack_click(self,instance):
        self.clear_widgets()
        self.add_widget(HomeScreen())


class MyApp(App):
    def build(self):
        return HomeScreen()


if __name__ == '__main__':
    MyApp().run()
