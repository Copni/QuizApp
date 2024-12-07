# Quiz Program

This Python program allows users to create, load, and take quizzes, while also keeping track of questions they answered incorrectly. Users can review their past mistakes and attempt to improve their performance.

## Features

1. **Take a Quiz**:
   - Select a quiz theme and specific quiz files to attempt.
   - Choose between random or sequential question order.
   - Incorrectly answered questions are stored for later review.

2. **Load a Quiz Theme**:
   - Add a new theme by specifying a folder containing quiz files.
   - Themes are saved in a `quizPath.txt` file for future reference.

3. **Create a Quiz**:
   - Add questions, answer options, and explanations interactively.
   - Save the quiz in JSON format within a specified folder.

4. **Review Mistakes**:
   - Incorrectly answered questions are stored in the `Errors` folder, with a maximum of 10 recent error files.
   - Users can select a past error file to review and retry incorrect questions.

5. **Menu Navigation**:
   - Each menu includes an option to cancel and return to the main menu.

## File Structure

- **Quiz Files**: Stored in JSON format with the following structure:
  ```json
  [
      [
          "Question text",
          ["Option 1", true],
          ["Option 2", false],
          ["Option 3", false],
          ["Option 4", false],
          "Explanation for the correct answer"
      ],
      ...
  ]
  ```

- **Themes**: Saved in `quizPath.txt` with the format:
  ```
  [Theme Name]-[Path to Folder]
  ```

- **Error Files**: Stored in the `Errors` folder with filenames like `MyError01.json`.

## How to Use

### Running the Program
Run the program using Python:
```bash
python quiz_program.py
```

### Main Menu Options

1. **Take a Quiz**
   - Displays available themes.
   - Allows selecting quizzes from the chosen theme.
   - Saves incorrect questions for later review.

2. **Load a Quiz Theme**
   - Specify a folder containing quiz files.
   - Add a theme name for better organization.

3. **Create a Quiz**
   - Create a new quiz by adding questions, options, and explanations.
   - Save the quiz to a chosen folder.

4. **Review Mistakes**
   - Lists up to 10 recent error files.
   - Allows reviewing and retrying incorrect questions.

5. **Exit**
   - Exits the program.

### Example Workflow

1. Load a quiz theme:
   - Add a folder with quizzes using "Load a Quiz Theme."

2. Take a quiz:
   - Select a theme and specific quiz files.
   - Answer questions and review your score.

3. Review mistakes:
   - Select an error file from the "Errors" folder.
   - Retry the questions you got wrong.

## Requirements

- Python 3.x

## Notes

- The `Errors` folder and the `quizPath.txt` file are created automatically.
- A maximum of 10 error files is maintained in the `Errors` folder.

## License

This project is licensed under the GPL (GNU General Public License).

