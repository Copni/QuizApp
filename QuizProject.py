import os
import json
import random

# Global variable to store incorrect questions
incorrect_questions = []

# Helper function to load quiz files
def load_quiz(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Erreur lors du chargement du fichier.")
        return []

# Helper function to save quiz files
def save_quiz(filepath, data):
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print("Quiz sauvegardé avec succès !")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

# Helper function to save themes and paths
def save_themes(themes):
    themes_file = "quizPath.txt"
    try:
        with open(themes_file, 'w') as file:
            for theme, path in themes.items():
                file.write(f"[{theme}]-[{path}]\n")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des thèmes : {e}")

# Helper function to load themes and paths
def load_themes():
    themes_file = "quizPath.txt"
    themes = {}
    try:
        if os.path.exists(themes_file):
            with open(themes_file, 'r') as file:
                for line in file:
                    if line.strip().startswith('[') and ']-[' in line and line.strip().endswith(']'):
                        parts = line.strip()[1:-1].split(']-[')
                        if len(parts) == 2:
                            theme, path = parts
                            themes[theme] = path
                        else:
                            print(f"Ligne mal formée ignorée : {line.strip()}")
                    else:
                        print(f"Ligne mal formée ignorée : {line.strip()}")
    except Exception as e:
        print(f"Erreur lors du chargement des thèmes : {e}")
    return themes

# Play a quiz
def play_quiz():
    themes = load_themes()

    # Ensure the "Errors" theme exists
    error_theme_path = "Errors"
    if "Review my errors" not in themes:
        os.makedirs(error_theme_path, exist_ok=True)
        themes["Review my errors"] = error_theme_path
        save_themes(themes)

    if not themes:
        print("Aucun thème n'est disponible. Veuillez charger des quiz.")
        return

    print("\nThèmes disponibles :")
    for idx, (theme, path) in enumerate(themes.items(), 1):
        print(f"{idx}. {theme} : {path}")
    print("0. Annuler")

    try:
        selected_theme_idx = int(input("Entrez le numéro du thème que vous voulez sélectionner : ")) - 1
        if selected_theme_idx == -1:
            return
        selected_theme = list(themes.items())[selected_theme_idx]
    except (ValueError, IndexError):
        print("Sélection invalide.")
        return

    theme_name, theme_path = selected_theme
    quizzes = [file for file in os.listdir(theme_path) if file.endswith('.json')]

    if not quizzes:
        print("Aucun quiz disponible dans ce thème.")
        return

    print("Quizzes disponibles :")
    for idx, quiz in enumerate(quizzes, 1):
        quiz_path = os.path.join(theme_path, quiz)
        questions = load_quiz(quiz_path)
        print(f"{idx}. {quiz} - {len(questions)} questions")
    print("0. Annuler")

    selected_indices = input("Entrez les numéros des quiz (séparés par des virgules) : ")
    if selected_indices.strip() == "0":
        return

    try:
        selected_files = [quizzes[int(i) - 1] for i in selected_indices.split(',') if i.isdigit() and 0 < int(i) <= len(quizzes)]
    except IndexError:
        print("Sélection invalide.")
        return

    random_order = input("Voulez-vous un ordre aléatoire des questions ? (oui/non) : ").strip().lower() == 'oui'

    questions = []
    for quiz_file in selected_files:
        questions.extend(load_quiz(os.path.join(theme_path, quiz_file)))

    if random_order:
        random.shuffle(questions)

    score = 0
    error_theme_path = "Errors"

    # Create a unique error file name
    error_files = sorted([file for file in os.listdir(error_theme_path) if file.startswith("MyError") and file.endswith(".json")])
    if len(error_files) >= 10:
        os.remove(os.path.join(error_theme_path, error_files[0]))

    new_error_file = os.path.join(error_theme_path, f"MyError{len(error_files) + 1:02d}.json")
    errors_to_save = []

    for idx, question_data in enumerate(questions, 1):
        print(f"\nQuestion {idx}/{len(questions)}: {question_data[0]}")
        options = question_data[1:-1]
        explanation = question_data[-1]

        for option_idx, option in enumerate(options, 1):
            print(f"{option_idx}. {option[0]}")

        try:
            answer = int(input("Votre réponse : ")) - 1
            if 0 <= answer < len(options) and options[answer][1]:
                print("Bonne réponse !")
                score += 1
            else:
                print("Mauvaise réponse.")
                errors_to_save.append(question_data)
                print("Explication :", explanation)
        except ValueError:
            print("Réponse invalide.")

    save_quiz(new_error_file, errors_to_save)
    print(f"\nVotre score : {score}/{len(questions)}")

# Load quiz paths and themes
def load_quiz_paths():
    path = input("Entrez le chemin d'accès du dossier contenant les quiz : ")
    if not os.path.isdir(path):
        print("Dossier introuvable.")
        return

    theme_name = input("Entrez le nom du thème pour ce dossier : ")
    themes = load_themes()
    themes[theme_name] = path
    save_themes(themes)
    print(f"Thème '{theme_name}' enregistré avec succès.")

# Create a new quiz
def create_quiz():
    path = input("Entrez le chemin d'accès du dossier pour sauvegarder le quiz : ")
    if not os.path.isdir(path):
        print("Dossier introuvable.")
        return

    questions = []
    while True:
        question = input("Entrez la question : ")
        options = []
        while True:
            option = input("Entrez une option (ou tapez 'stop' pour arrêter) : ")
            if option.lower() == 'stop':
                break
            is_correct = input("Est-ce une bonne réponse ? (oui/non) : ").strip().lower() == 'oui'
            options.append([option, is_correct])
        explanation = input("Entrez l'explication : ")
        questions.append([question, *options, explanation])

        another = input("Voulez-vous ajouter une autre question ? (oui/non) : ").strip().lower()
        if another != 'oui':
            break

    filename = input("Entrez le nom du fichier pour le quiz (sans extension) : ")
    save_quiz(os.path.join(path, f"{filename}.json"), questions)

# View incorrect questions
def view_errors():
    error_theme_path = "Errors"
    if not os.path.exists(error_theme_path):
        print("Aucune erreur enregistrée.")
        return

    error_files = sorted([file for file in os.listdir(error_theme_path) if file.startswith("MyError") and file.endswith(".json")], reverse=True)

    if not error_files:
        print("Aucune erreur enregistrée.")
        return

    print("\nDernières tentatives (de la plus récente à la plus ancienne) :")
    for idx, file in enumerate(error_files, 1):
        print(f"{idx}. {file}")
    print("0. Annuler")

    try:
        selected_file_idx = int(input("Entrez le numéro du fichier à réviser : ")) - 1
        if selected_file_idx == -1:
            return
        if 0 <= selected_file_idx < len(error_files):
            selected_file = os.path.join(error_theme_path, error_files[selected_file_idx])
            questions = load_quiz(selected_file)
        else:
            print("Sélection invalide.")
            return
    except ValueError:
        print("Entrée invalide.")
        return

    print("\nQuestions incorrectes :")
    for idx, question_data in enumerate(questions[:], 1):
        print(f"\nQuestion {idx}/{len(questions)}: {question_data[0]}")
        options = question_data[1:-1]
        explanation = question_data[-1]

        for option_idx, option in enumerate(options, 1):
            print(f"{option_idx}. {option[0]}")

        try:
            answer = int(input("Votre réponse : ")) - 1
            if 0 <= answer < len(options) and options[answer][1]:
                print("Bonne réponse !")
                questions.remove(question_data)
            else:
                print("Mauvaise réponse.")
                print("Explication :", explanation)
        except ValueError:
            print("Réponse invalide.")

    save_quiz(selected_file, questions)

# Main menu
def main():
    while True:
        print("\nMenu Principal")
        print("1. Tester ses connaissances")
        print("2. Charger un quiz")
        print("3. Créer un quiz")
        print("4. Voir mes erreurs")
        print("5. Quitter")

        choice = input("Entrez votre choix : ").strip()

        if choice == '1':
            play_quiz()
        elif choice == '2':
            load_quiz_paths()
        elif choice == '3':
            create_quiz()
        elif choice == '4':
            view_errors()
        elif choice == '5':
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
