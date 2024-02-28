import subprocess
import git
from github import Github

def ajouter_ligne_numerotee(nom_fichier, i):
    try:
        # Ouvrir le fichier en mode lecture
        with open(nom_fichier, 'r') as f:
            lignes = f.readlines()

        # Ajouter une ligne avec le numéro de ligne
        numero_derniere_ligne = len(lignes) + 1
        nouvelle_ligne = f"Ligne n°{numero_derniere_ligne}\n"

        # Ouvrir le fichier en mode écriture et ajouter la nouvelle ligne
        with open(nom_fichier, 'a') as f:
            f.write(nouvelle_ligne)
        print("Ligne ajoutée avec succès.")
        
        git_repo = git.Repo.init()
        
        github = Github("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")  # Remplacez par votre token GitHub
        reposi = github.get_repo("Thomas141203/PR-AutomationV2")  # Remplacez par le nom de votre utilisateur et de votre dépôt
        
        nouvelle_branche = f"feature-{numero_derniere_ligne}"
        git_repo.git.checkout("-b", nouvelle_branche)

        # Ajouter le fichier modifié à l'index de Git
        git_repo.index.add([nom_fichier])

        # Faire un commit avec le numéro de ligne comme message
        message_commit = f"Ajout de la ligne numéro {numero_derniere_ligne}"
        git_repo.index.commit(message_commit)

        # Pousser la nouvelle branche sur le dépôt distant
        origin = git_repo.remote(name="origin")
        origin.push(nouvelle_branche)
        print(f"Branche '{nouvelle_branche}' poussée vers le dépôt distant.")

        # Créer une pull request
        pull = reposi.create_pull(
            title=message_commit,
            body="Pull request pour ajouter une ligne numérotée",
            head=nouvelle_branche,
            base="master"  # Remplacez par le nom de votre branche principale
        )
        print("Pull request créée avec succès.")
        
        pull = reposi.get_pull(i+65)

        # Fusionner la pull request
        pull.merge()

    except FileNotFoundError:
        print(f"Le fichier '{nom_fichier}' est introuvable.")

# Exemple d'utilisation
nom_fichier = "fichier.txt"
for i in range(1):
    ajouter_ligne_numerotee(nom_fichier, i)