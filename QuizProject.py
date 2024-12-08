import os
import json
import random
import textwrap
from natsort import natsorted  # Use natsort for natural sorting

# Helper function to load quiz files
def load_quiz(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Erreur lors du chargement du fichier.")
        return []

# Helper function to save quiz files
def save_quiz(filepath, data):
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print("✅ Quiz sauvegardé avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")

# Helper function to save themes and paths
def save_themes(themes):
    themes_file = "quizPath.txt"
    try:
        with open(themes_file, 'w') as file:
            for theme, path in themes.items():
                file.write(f"[{theme}]-[{path}]\n")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde des thèmes : {e}")

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
                            print(f"⚠️ Ligne mal formée ignorée : {line.strip()}")
                    else:
                        print(f"⚠️ Ligne mal formée ignorée : {line.strip()}")
    except Exception as e:
        print(f"❌ Erreur lors du chargement des thèmes : {e}")
    return themes

def edit_category():
    themes = load_themes()
    if not themes:
        print("❌ Aucun thème n'est disponible.")
        return

    print("\n📂 Catégories disponibles :")
    for idx, (theme, path) in enumerate(themes.items(), 1):
        print(f"{idx}. {theme} : {path}")

    try:
        selected_idx = int(input("🎯 Entrez le numéro de la catégorie à modifier : ")) - 1
        if selected_idx < 0 or selected_idx >= len(themes):
            print("❌ Sélection invalide.")
            return

        selected_theme = list(themes.items())[selected_idx]
        new_name = input(f"📝 Entrez le nouveau nom pour '{selected_theme[0]}' : ").strip()
        if not new_name:
            print("❌ Nom invalide.")
            return

        themes[new_name] = themes.pop(selected_theme[0])
        save_themes(themes)
        print(f"✅ Catégorie renommée en '{new_name}' avec succès !")

    except ValueError:
        print("❌ Entrée invalide.")

# Add a function to delete categories
def delete_category():
    themes = load_themes()
    if not themes:
        print("❌ Aucun thème n'est disponible.")
        return

    print("\n📂 Catégories disponibles :")
    for idx, (theme, path) in enumerate(themes.items(), 1):
        print(f"{idx}. {theme} : {path}")

    try:
        selected_idx = int(input("🎯 Entrez le numéro de la catégorie à supprimer : ")) - 1
        if selected_idx < 0 or selected_idx >= len(themes):
            print("❌ Sélection invalide.")
            return

        selected_theme = list(themes.items())[selected_idx]
        confirm = input(f"⚠️ Êtes-vous sûr de vouloir supprimer '{selected_theme[0]}' ? (oui/non) : ").strip().lower()
        if confirm == 'oui':
            themes.pop(selected_theme[0])
            save_themes(themes)
            print(f"✅ Catégorie '{selected_theme[0]}' supprimée avec succès !")
        else:
            print("❌ Suppression annulée.")

    except ValueError:
        print("❌ Entrée invalide.")

# Display formatted explanation
def display_explanation(explanation):
    print("\n📖 Explication :")
    print(textwrap.fill(explanation, width=100))  # Wider wrapping for better readability


def handle_matching_question(question_data, score, errors_to_save):
    """
    Handles matching-type questions with options shuffled and categories remaining in order.
    """
    question_text = question_data[0]
    categories = [item[0][3:] for item in question_data[1:] if isinstance(item, list) and item[0][0].isalpha()]
    options = [item[0][3:] for item in question_data[1:] if isinstance(item, list) and item[0][0].isdigit()]
    explanation = question_data[-2]
    original_mapping = question_data[-1]

    # Extract the text corresponding to each key in original_mapping
    original_option_texts = {key: next(opt[0][3:] for opt in question_data[1:] if opt[0].startswith(key)) for key in original_mapping.keys()}

    # Shuffle options
    shuffled_options = options[:]
    random.shuffle(shuffled_options)

    # Create shuffled mapping based on shuffled options
    shuffled_mapping = {
        category: str(shuffled_options.index(original_option_texts[key]) + 1)
        for key, category in original_mapping.items()
    }

    # Display the question
    print(textwrap.fill(question_text, width=100))

    # Display categories
    print("\n📂 Categories:")
    for idx, category in enumerate(categories, start=1):
        print(f"   {chr(64 + idx)}. {category}")

    # Display shuffled options
    print("\n📜 Options:")
    for idx, option in enumerate(shuffled_options, start=1):
        print(f"   {idx}. {option}")

    # Prompt the user for their answer
    print("\n👉 Associez chaque catégorie à un numéro en utilisant le format : 'A=1,B=2,...'")
    while True:
        user_input = input("💡 Votre réponse : ").strip()
        try:
            # Parse the user's input into a dictionary
            user_answer = {
                pair.split('=')[0].strip(): pair.split('=')[1].strip()
                for pair in user_input.split(',')
            }

            # Check if the user's answer matches the shuffled mapping
            if user_answer == shuffled_mapping:
                print("✅ Bonne réponse !")
                score += 1
                print("\n✔️ Réponse correcte :")
                for key, value in shuffled_mapping.items():
                    print(f"   {key} = {value}")
                break
            else:
                print("❌ Mauvaise réponse.")
                print("\n✔️ Réponse correcte :")
                for key, value in shuffled_mapping.items():
                    print(f"   {key} = {value}")
                errors_to_save.append(question_data)
                break
        except Exception:
            print("⚠️ Format invalide. Réessayez en utilisant le format spécifié.")

    return score


def randomize_mcq_answers(question_data):
    """
    Randomizes the answers in MCQ questions while maintaining the correctness information.
    :param question_data: The question data list with question text, options, and explanation.
    :return: The updated question data with randomized options.
    """
    question_text = question_data[0]
    options = question_data[1:-1]
    explanation = question_data[-1]

    # Shuffle options while preserving their correctness
    randomized_options = options[:]
    random.shuffle(randomized_options)

    # Update the question data with shuffled options
    return [question_text, *randomized_options, explanation]


def play_quiz():
    themes = load_themes()

    # Ensure the "Errors" theme exists
    error_theme_path = "Errors"
    if "Review my errors" not in themes:
        os.makedirs(error_theme_path, exist_ok=True)
        themes["Review my errors"] = error_theme_path
        save_themes(themes)

    if not themes:
        print("❌ Aucun thème n'est disponible. Veuillez charger des quiz.")
        return

    print("\n🎨 Thèmes disponibles :")
    for idx, (theme, path) in enumerate(themes.items(), 1):
        print(f"{idx}. {theme} : {path}")
    print("0. Annuler")

    try:
        selected_theme_idx = int(input("🎯 Entrez le numéro du thème que vous voulez sélectionner : ")) - 1
        if selected_theme_idx == -1:
            return
        selected_theme = list(themes.items())[selected_theme_idx]
    except (ValueError, IndexError):
        print("❌ Sélection invalide.")
        return

    theme_name, theme_path = selected_theme
    quizzes = [file for file in os.listdir(theme_path) if file.endswith('.json')]

    if not quizzes:
        print("❌ Aucun quiz disponible dans ce thème.")
        return

    # Sort quizzes alphabetically and numerically
    quizzes = natsorted(quizzes)

    # Enhanced quiz display
    print("\n📚 Quizzes disponibles :")
    print(f"{'#':<5} {'Nom du Quiz':<25} {'Nombre de Questions'}")
    print("-" * 45)
    for idx, quiz in enumerate(quizzes, 1):
        quiz_path = os.path.join(theme_path, quiz)
        questions = load_quiz(quiz_path)
        print(f"{idx:<5} {quiz:<25} {len(questions)} questions")
    print("0. Annuler")

    selected_indices = input("🎯 Entrez les numéros des quiz (séparés par des virgules) : ")
    if selected_indices.strip() == "0":
        return

    try:
        selected_files = [quizzes[int(i) - 1] for i in selected_indices.split(',') if
                          i.isdigit() and 0 < int(i) <= len(quizzes)]
    except IndexError:
        print("❌ Sélection invalide.")
        return

    random_order = input("🎲 Voulez-vous un ordre aléatoire des questions ? (oui/non) : ").strip().lower() == 'oui'

    questions = []
    for quiz_file in selected_files:
        questions.extend(load_quiz(os.path.join(theme_path, quiz_file)))

    if random_order:
        random.shuffle(questions)

    score = 0
    errors_to_save = []

    for idx, question_data in enumerate(questions, 1):
        print("\n" + "=" * 100)
        print(f"❓ Question {idx}/{len(questions)}:")

        # Check if the question is of Match type
        if isinstance(question_data[-1], dict):
            score = handle_matching_question(question_data, score, errors_to_save)
        else:
            # Randomize MCQ answers
            question_data = randomize_mcq_answers(question_data)

            # Process standard MCQ
            options = question_data[1:-1]
            explanation = question_data[-1]

            # Properly format and display the question with controlled line breaks
            question_text = question_data[0]
            formatted_question = "\n".join(
                textwrap.fill(paragraph, width=100) for paragraph in question_text.split('\n')
            )
            print(formatted_question)
            print()  # Blank line between the question and the answers

            for option_idx, option in enumerate(options, 1):
                print(f"   {option_idx}. {option[0]}")

            print()  # Blank line between the last answer and the user input

            correct_answers = [i + 1 for i, opt in enumerate(options) if opt[1]]

            # Notify user about multiple answers
            if len(correct_answers) > 1:
                print(
                    f"ℹ️ Cette question a {len(correct_answers)} réponses correctes. Entrez vos réponses séparées par des virgules.")

            while True:  # Loop until the user provides the correct number of answers
                try:
                    user_answers = input("👉 Votre réponse : ").strip()
                    user_answers = [int(ans.strip()) for ans in user_answers.split(',')]

                    # Check for the correct number of answers
                    if len(user_answers) != len(correct_answers):
                        print(f"⚠️ Vous devez entrer exactement {len(correct_answers)} réponses. Réessayez.")
                        continue  # Loop back for user input

                    # Check if answers are correct
                    if set(user_answers) == set(correct_answers):
                        print("✅ Bonne réponse !")
                        display_explanation(explanation)
                        score += 1
                        break
                    else:
                        print("❌ Mauvaise réponse.")
                        print(f"✔️ La bonne réponse était : {', '.join(map(str, correct_answers))}")
                        display_explanation(explanation)
                        errors_to_save.append(question_data)
                        break
                except ValueError:
                    print("❌ Réponse invalide. Veuillez réessayer.")

    # Save incorrect questions
    if errors_to_save:
        new_error_file = os.path.join(error_theme_path, f"MyError_{len(errors_to_save)}.json")
        save_quiz(new_error_file, errors_to_save)

    print("\n🎉 Résultat final :")
    print(f"   📊 Votre score : {score}/{len(questions)}")
    print("=" * 100)


# Load quiz paths and themes
def load_quiz_paths():
    path = input("📂 Entrez le chemin d'accès du dossier contenant les quiz : ")
    if not os.path.isdir(path):
        print("❌ Dossier introuvable.")
        return

    theme_name = input("🎨 Entrez le nom du thème pour ce dossier : ")
    themes = load_themes()
    themes[theme_name] = path
    save_themes(themes)
    print(f"✅ Thème '{theme_name}' enregistré avec succès.")

# Create a new quiz
def create_quiz():
    path = input("📂 Entrez le chemin d'accès du dossier pour sauvegarder le quiz : ")
    if not os.path.isdir(path):
        print("❌ Dossier introuvable.")
        return

    questions = []
    while True:
        question = input("❓ Entrez la question : ")
        options = []
        while True:
            option = input("➡️ Entrez une option (ou tapez 'stop' pour arrêter) : ")
            if option.lower() == 'stop':
                break
            is_correct = input("✔️ Est-ce une bonne réponse ? (oui/non) : ").strip().lower() == 'oui'
            options.append([option, is_correct])
        explanation = input("📖 Entrez l'explication : ")
        questions.append([question, *options, explanation])

        another = input("➕ Voulez-vous ajouter une autre question ? (oui/non) : ").strip().lower()
        if another != 'oui':
            break

    filename = input("💾 Entrez le nom du fichier pour le quiz (sans extension) : ")
    save_quiz(os.path.join(path, f"{filename}.json"), questions)

# View incorrect questions
def view_errors():
    error_theme_path = "Errors"
    if not os.path.exists(error_theme_path):
        print("❌ Aucune erreur enregistrée.")
        return

    error_files = sorted([file for file in os.listdir(error_theme_path) if file.startswith("MyError") and file.endswith(".json")], reverse=True)

    if not error_files:
        print("❌ Aucune erreur enregistrée.")
        return

    print("\n📂 Dernières tentatives (de la plus récente à la plus ancienne) :")
    for idx, file in enumerate(error_files, 1):
        print(f"{idx}. {file}")
    print("0. Annuler")

    try:
        selected_file_idx = int(input("🎯 Entrez le numéro du fichier à réviser : ")) - 1
        if selected_file_idx == -1:
            return
        if 0 <= selected_file_idx < len(error_files):
            selected_file = os.path.join(error_theme_path, error_files[selected_file_idx])
            questions = load_quiz(selected_file)
        else:
            print("❌ Sélection invalide.")
            return
    except ValueError:
        print("❌ Entrée invalide.")
        return

    print("\n📖 Questions incorrectes :")
    for idx, question_data in enumerate(questions[:], 1):
        while True:
            print("\n" + "=" * 100)
            print(f"❓ Question {idx}/{len(questions)}:")
            print(textwrap.fill(question_data[0], width=100))
            print()  # Blank line between question and first answer
            options = question_data[1:-1]
            explanation = question_data[-1]

            for option_idx, option in enumerate(options, 1):
                print(f"   {option_idx}. {option[0]}")
            print()  # Blank line between the last answer and user input

            correct_answers = [i + 1 for i, opt in enumerate(options) if opt[1]]

            try:
                user_answers = input("👉 Votre réponse : ").strip()
                user_answers = [int(ans.strip()) for ans in user_answers.split(',')]

                # Check for invalid number of answers
                if len(user_answers) != len(correct_answers):
                    print(f"⚠️ Vous devez entrer exactement {len(correct_answers)} réponses. Réessayez.")
                    continue  # Prompt the user again

                if set(user_answers) == set(correct_answers):
                    print("✅ Bonne réponse !")
                    display_explanation(explanation)
                    questions.remove(question_data)
                    break
                else:
                    print("❌ Mauvaise réponse.")
                    print(f"✔️ La bonne réponse était : {', '.join(map(str, correct_answers))}")
                    display_explanation(explanation)
            except ValueError:
                print("❌ Réponse invalide. Veuillez réessayer.")

    save_quiz(selected_file, questions)

# Main menu
def main():
    while True:
        print("\n🏠 Menu Principal")
        print("1. 🧠 Tester ses connaissances")
        print("2. 📂 Charger un quiz")
        print("3. ✍️ Créer un quiz")
        print("4. 🚫 Voir mes erreurs")
        print("5. ✏️ Modifier une catégorie")
        print("6. 🗑️ Supprimer une catégorie")
        print("7. 🚪 Quitter")

        choice = input("🎯 Entrez votre choix : ").strip()

        if choice == '1':
            play_quiz()
        elif choice == '2':
            load_quiz_paths()
        elif choice == '3':
            create_quiz()
        elif choice == '4':
            view_errors()
        elif choice == '5':
            edit_category()
        elif choice == '6':
            delete_category()
        elif choice == '7':
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide.")


if __name__ == "__main__":
    main()
