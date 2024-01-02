from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
import pandas as pd

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

        try:
            # Charger les données du fichier Excel
            data = pd.read_excel("liste_eleves.xlsx")

            # Modifier les données dans le DataFrame Pandas
            mask = (data['Nom'] == nom_a_modifier) & (data['Prénom'] == prenom_a_modifier)
            data.loc[mask, 'niveau'] = nouveau_niveau
            data.loc[mask, 'Nom'] = self.input_nnom.text  # Mise à jour du nom
            data.loc[mask, 'Prénom'] = self.input_nprenom.text  # Mise à jour du prénom

            # Enregistrer les modifications dans le fichier Excel
            data.to_excel("liste_eleves.xlsx", index=False)
            print(f"Données de l'élève {nom_a_modifier} {prenom_a_modifier} modifiées dans le fichier Excel.")
            self.popup.dismiss()

        except FileNotFoundError:
            print("Fichier introuvable. Impossible de modifier les données.")
        except Exception as e:
            print(f"Erreur lors de la modification des données : {e}")


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
            # Charger les données depuis le fichier Excel
            data = pd.read_excel("liste_eleves.xlsx")

            eleve_trouve = False

            for index, row in data.iterrows():
                if row['Nom'].lower() == nom_recherche.lower():
                    self.popup.dismiss()
                
                    popup = Popup(title="Résultat de la recherche", size_hint=(None, None), size=(400, 200))
                
                    btn_supprimer = Button(text="Supprimer", size_hint=(None, None), size=(100, 50))
                    btn_supprimer.bind(on_press=lambda instance, nom=row['Nom'], prenom=row['Prénom']: self.supprimer_eleve(nom, prenom))

                    layout = BoxLayout(orientation='vertical')
                    layout.add_widget(Label(text=f"Élève trouvé : {row['Prénom']} {row['Nom']}, niveau : {row['niveau']}"))
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
            # Charger les données depuis le fichier Excel
            data = pd.read_excel("liste_eleves.xlsx")

            # Trouver l'index de l'élève à supprimer
            index_to_drop = data[(data['Nom'] == nom) & (data['Prénom'] == prenom)].index

            if not index_to_drop.empty:
                # Supprimer l'élève
                data.drop(index_to_drop, inplace=True)

                # Enregistrer les modifications dans le fichier Excel
                data.to_excel("liste_eleves.xlsx", index=False)

                self.popup.dismiss()
                popup = Popup(title="Succès", content=Label(text="Élève supprimé avec succès."), size_hint=(None, None), size=(300, 200))
                popup.open()
            else:
                self.popup.dismiss()
                popup = Popup(title="Erreur", content=Label(text="Élève non trouvé."), size_hint=(None, None), size=(300, 200))
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

        self.label_mot_de_passe = Label(text="Mot de passe :")
        self.input_mot_de_passe = TextInput(multiline=False)

        self.create_button = Button(text="Créer le compte")
        self.create_button.bind(on_press=self.creer_compte)

        content.add_widget(self.label_nom)
        content.add_widget(self.input_nom)
        content.add_widget(self.label_prenom)
        content.add_widget(self.input_prenom)
        content.add_widget(self.label_niveau)
        content.add_widget(self.input_niveau)
        content.add_widget(self.label_mot_de_passe)
        content.add_widget(self.input_mot_de_passe)
        content.add_widget(self.create_button)

        self.popup.open()

    def creer_compte(self, instance):
        try:
            # Récupère les informations de l'eleve à partir des champs de saisie
            username = f"{self.input_nom.text}.{self.input_prenom.text}"
            
            mot_de_passe = self.input_mot_de_passe.text  # Champ pour le mot de passe
            # Ajoutez d'autres champs si nécessaire

            # Vérifie si tous les champs sont remplis
            if username and mot_de_passe:
                # Charger les données depuis le fichier Excel
                data = pd.read_excel("login.xlsx")

                # Créer un dictionnaire pour l'eleve  à ajouter
                enseignant = {'Username':username, 'Mot de passe': mot_de_passe,'type':"S"}

                # Ajouter le nouvel eleve à une liste de dictionnaires
                comptes_eleves = data.to_dict('records')
                comptes_eleves.append(enseignant)

                # Créer un nouveau DataFrame à partir de la liste mise à jour
                nouveau_data = pd.DataFrame(comptes_eleves)

                # Enregistrer le DataFrame mis à jour dans le fichier Excel
                nouveau_data.to_excel("login.xlsx", index=False)

                self.popup.dismiss()
            else:
                print("Veuillez remplir tous les champs.")
        except FileNotFoundError:
            print("Fichier non trouvé.")

    
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
        try:
            # Récupère les informations de l'élève à partir des champs de saisie
            nom = self.input_nom.text
            prenom = self.input_prenom.text
            niveau = self.input_niveau.text

            # Vérifie si tous les champs sont remplis
            if nom and prenom and niveau:
                # Charger les données depuis le fichier Excel
                data = pd.read_excel("liste_eleves.xlsx")

                # Créer un dictionnaire pour l'élève à ajouter
                nouvel_eleve = {'Nom': nom, 'Prénom': prenom, 'niveau': niveau}

                # Ajouter le nouvel élève à une liste de dictionnaires
                liste_eleves = data.to_dict('records')
                liste_eleves.append(nouvel_eleve)

                # Créer un nouveau DataFrame à partir de la liste mise à jour
                nouveau_data = pd.DataFrame(liste_eleves)

                # Enregistrer le DataFrame mis à jour dans le fichier Excel
                nouveau_data.to_excel("liste_eleves.xlsx", index=False)

                self.afficher_liste_eleves()  # Actualise l'affichage des élèves
            else:
                print("Veuillez remplir tous les champs.")
        except FileNotFoundError:
            print("Fichier non trouvé.")

    def afficher_liste_eleves(self):
        try:
            # Charger les données depuis le fichier Excel
            data = pd.read_excel("liste_eleves.xlsx")

            # Afficher la liste des élèves
            liste_texte = "Liste des élèves :\n"
            for _, eleve in data.iterrows():
                liste_texte += f"{eleve['Prénom']} {eleve['Nom']}, niveau : {eleve['niveau']}\n"

            self.liste_eleves_label.text = liste_texte
        except FileNotFoundError:
            print("Fichier non trouvé.")

    

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
        nouveau_niveau = self.input_niveau.text

        try:
            # Charger les données du fichier Excel des enseignants
            data = pd.read_excel("liste_enseignants.xlsx")

            # Modifier les données dans le DataFrame Pandas
            mask = (data['Nom'] == nom_a_modifier) & (data['Prénom'] == prenom_a_modifier)
            data.loc[mask, 'niveau'] = nouveau_niveau
            data.loc[mask, 'Nom'] = self.input_nnom.text  # Mise à jour du nom
            data.loc[mask, 'Prénom'] = self.input_nprenom.text  # Mise à jour du prénom

            # Enregistrer les modifications dans le fichier Excel des enseignants
            data.to_excel("liste_enseignants.xlsx", index=False)
            print(f"Données de l'enseignant {nom_a_modifier} {prenom_a_modifier} modifiées dans le fichier Excel.")
            self.popup.dismiss()

        except FileNotFoundError:
            print("Fichier introuvable. Impossible de modifier les données.")
        except Exception as e:
            print(f"Erreur lors de la modification des données : {e}")


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
            # Charger les données depuis le fichier Excel des enseignants
            data = pd.read_excel("liste_enseignants.xlsx")

            enseignant_trouve = False

            for index, row in data.iterrows():
                if row['Nom'].lower() == nom_recherche.lower():
                    self.popup.dismiss()
                
                    popup = Popup(title="Résultat de la recherche", size_hint=(None, None), size=(400, 200))
                
                    btn_supprimer = Button(text="Supprimer", size_hint=(None, None), size=(100, 50))
                    btn_supprimer.bind(on_press=lambda instance, nom=row['Nom'], prenom=row['Prénom']: self.supprimer_enseignant(nom, prenom))

                    layout = BoxLayout(orientation='vertical')
                    layout.add_widget(Label(text=f"Enseignant trouvé : {row['Prénom']} {row['Nom']}"))
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
            # Charger les données depuis le fichier Excel des enseignants
            data = pd.read_excel("liste_enseignants.xlsx")

            # Trouver l'index de l'enseignant à supprimer
            index_to_drop = data[(data['Nom'] == nom) & (data['Prénom'] == prenom)].index

            if not index_to_drop.empty:
                # Supprimer l'enseignant
                data.drop(index_to_drop, inplace=True)

                # Enregistrer les modifications dans le fichier Excel
                data.to_excel("liste_enseignants.xlsx", index=False)

                self.popup.dismiss()
                popup = Popup(title="Succès", content=Label(text="Enseignant supprimé avec succès."), size_hint=(None, None), size=(300, 200))
                popup.open()
            else:
                self.popup.dismiss()
                popup = Popup(title="Erreur", content=Label(text="Enseignant non trouvé."), size_hint=(None, None), size=(300, 200))
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

        self.label_mot_de_passe = Label(text="Mot de passe :")
        self.input_mot_de_passe = TextInput(multiline=False)

        self.create_button = Button(text="Créer le compte")
        self.create_button.bind(on_press=self.creer_compte)

        content.add_widget(self.label_nom)
        content.add_widget(self.input_nom)
        content.add_widget(self.label_prenom)
        content.add_widget(self.input_prenom)
        content.add_widget(self.label_mot_de_passe)
        content.add_widget(self.input_mot_de_passe)
        content.add_widget(self.create_button)
        

        self.popup.open()

    def creer_compte(self, instance):
        try:
            # Récupère les informations de l'enseignant à partir des champs de saisie
            username = f"{self.input_nom.text}.{self.input_prenom.text}"
            
            mot_de_passe = self.input_mot_de_passe.text  # Champ pour le mot de passe
            # Ajoutez d'autres champs si nécessaire

            # Vérifie si tous les champs sont remplis
            if username and mot_de_passe:
                # Charger les données depuis le fichier Excel
                data = pd.read_excel("login.xlsx")

                # Créer un dictionnaire pour l'enseignant à ajouter
                enseignant = {'Username':username, 'Mot de passe': mot_de_passe,'type':"T"}

                # Ajouter le nouvel enseignant à une liste de dictionnaires
                comptes_enseignants = data.to_dict('records')
                comptes_enseignants.append(enseignant)

                # Créer un nouveau DataFrame à partir de la liste mise à jour
                nouveau_data = pd.DataFrame(comptes_enseignants)

                # Enregistrer le DataFrame mis à jour dans le fichier Excel
                nouveau_data.to_excel("login.xlsx", index=False)
                
                self.popup.dismiss()
               
            else:
                print("Veuillez remplir tous les champs.")
        except FileNotFoundError:
            print("Fichier non trouvé.")


    
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
        try:
            # Récupère les informations de l'enseignant à partir des champs de saisie
            nom = self.input_nom.text
            prenom = self.input_prenom.text
            # Ajoutez d'autres champs si nécessaire

            # Vérifie si tous les champs sont remplis
            if nom and prenom:
                # Charger les données depuis le fichier Excel
                data = pd.read_excel("liste_enseignants.xlsx")

                # Créer un dictionnaire pour l'enseignant à ajouter
                nouvel_enseignant = {'Nom': nom, 'Prénom': prenom}

                # Ajouter le nouvel enseignant à une liste de dictionnaires
                liste_enseignants = data.to_dict('records')
                liste_enseignants.append(nouvel_enseignant)

                # Créer un nouveau DataFrame à partir de la liste mise à jour
                nouveau_data = pd.DataFrame(liste_enseignants)

                # Enregistrer le DataFrame mis à jour dans le fichier Excel
                nouveau_data.to_excel("liste_enseignants.xlsx", index=False)

                self.afficher_liste_enseignants()  # Actualise l'affichage des enseignants
            else:
                print("Veuillez remplir tous les champs.")
        except FileNotFoundError:
                print("Fichier non trouvé.")


    def afficher_liste_enseignants(self):
        try:
            # Charger les données depuis le fichier Excel
            data = pd.read_excel("liste_enseignants.xlsx")

            # Afficher la liste des enseignants
            liste_texte = "Liste des enseignants :\n"
            for _, enseignant in data.iterrows():
                liste_texte += f"{enseignant['Prénom']} {enseignant['Nom']}\n"

            self.liste_enseignants_label.text = liste_texte
        except FileNotFoundError:
            print("Fichier non trouvé.")


    def GoBack_click(self,instance):
        self.clear_widgets()
        self.add_widget(HomeScreen())


class MyApp(App):
    def build(self):
        return HomeScreen()


if __name__ == '__main__':
    MyApp().run()
