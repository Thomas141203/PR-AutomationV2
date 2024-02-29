import subprocess
import git
from github import Github

def ajouter_ligne_numerotee(nom_fichier, i):
    try:
        with open(nom_fichier, 'r') as f:
            lignes = f.readlines()

        numero_derniere_ligne = len(lignes) + 1
        nouvelle_ligne = f"Ligne n°{numero_derniere_ligne}\n"

        with open(nom_fichier, 'a') as f:
            f.write(nouvelle_ligne)
        print("Ligne ajoutée avec succès.")
        
        git_repo = git.Repo.init()
        
        github = Github("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")
        reposi = github.get_repo("Thomas141203/PR-AutomationV2")
        
        nouvelle_branche = f"feature-{numero_derniere_ligne}"
        git_repo.git.checkout("-b", nouvelle_branche)

        git_repo.index.add([nom_fichier])

        message_commit = f"Ajout de la ligne numéro {numero_derniere_ligne}"
        git_repo.index.commit(message_commit)

        origin = git_repo.remote(name="origin")
        origin.push(nouvelle_branche)
        print(f"Branche '{nouvelle_branche}' poussée vers le dépôt distant.")

        pull = reposi.create_pull(
            title=message_commit,
            body="Pull request pour ajouter une ligne numérotée",
            head=nouvelle_branche,
            base="main"
        )
        print("Pull request créée avec succès.")
        
        pull = reposi.get_pull(i)

        pull.merge()

    except FileNotFoundError:
        print(f"Le fichier '{nom_fichier}' est introuvable.")

nom_fichier = "fichier.txt"
for i in range(1):
    ajouter_ligne_numerotee(nom_fichier, i)