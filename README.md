# Personalised-student-recommendations
A Python-based solution to analyze quiz performance and provide students with personalized recommendations to improve their preparation for NEET.

# Quiz Performance Analysis and Reporting System

## Overview

This project automates the analysis of quiz data, providing personalized feedback and insights to students. It comprises two primary Python scripts: `test_analyzer.py` for individual quiz analysis and `performance_analyzer.py` for tracking performance over multiple quizzes. Both scripts generate comprehensive HTML reports with embedded data visualizations.

## Files Included

*   **`test_analyzer.py`:**
    *   Analyzes data from a single quiz attempt.
    *   Calculates quiz accuracy, identifies weak topics, analyzes performance by difficulty level, generates a student persona, predicts a potential NEET rank, and provides tailored recommendations.
    *   Generates HTML reports with graphs embedded as base64 images.
*   **`performance_analyzer.py`:**
    *   Analyzes performance across multiple quiz attempts.
    *   Calculates overall scores, accuracy, identifies high and low scores, and analyzes topic performance.
    *   Generates HTML reports with graphs embedded as base64 images.
*   **`nlp_utils.py`:**
    *   Provides utility functions for Natural Language Processing (NLP) tasks.
    *   Includes functions to predict question difficulty level and assess option confusingness.
*   **`current_test_data.txt`:**
    *   Sample JSON file containing quiz question data.
    *   Follows a predefined format for quiz structure, questions, options, topics, and difficulty levels.
*   **`quiz_submission_data.txt`:**
    *   Sample JSON file containing student responses to a quiz.
    *   Includes data such as student answers, scores, timestamps, and other submission-related information.
*   **`Performance_data.txt`:**
    *   Sample JSON file containing performance data across multiple quizzes.
    *   Includes quiz titles, scores, accuracies, submission dates, and topics.
*   **`report.html`:**
    *   The generated HTML report for a single quiz attempt.

## Data Formats

### `current_test_data.txt`
This file contains data about the structure and content of a single quiz. 

### `quiz_submission_data.txt`
This file contains data about a student's submission for a single quiz. 


## Dependencies

The following Python libraries are required:

*   `json`
*   `matplotlib`
*   `numpy`
*   `datetime`
*   `itertools`
*   `nltk`

### `test_analyzer.py`

This script analyzes a single quiz attempt and generates an HTML report.

1.  **Prepare Data:** Make sure `current_test_data.txt` and `quiz_submission_data.txt` are correctly formatted and contain the relevant data.

2.  **Run the Script:**
  
3.  **View Report:** Open the generated `report.html` file in your web browser.
   

  ![image](https://github.com/user-attachments/assets/9e322cc7-efad-4f0a-81d5-f14f9d1f061e)
     ![image](https://github.com/user-attachments/assets/261cd21a-1b3f-4c03-9afb-9a4aedde839d)
  ![image](https://github.com/user-attachments/assets/7de65db1-cddf-46f7-9770-8a6d220210e5)
  ![image](https://github.com/user-attachments/assets/0c70fc21-f067-4402-96c8-d4d8e9e4dd88)
![image](https://github.com/user-attachments/assets/c616b7ff-b285-4444-a86e-e2a9d6779980)
![image](https://github.com/user-attachments/assets/ac2b9dcb-5d62-4cc9-a63a-9b55be089f2b)
![image](https://github.com/user-attachments/assets/08287eb5-4779-4de4-a27e-5c914cd92aa8)


### `performance_analyzer.py`

This script analyzes performance data across multiple quizzes and generates an HTML report.

1.  **Prepare Data:** Make sure `Performance_data.txt` is correctly formatted and contains the relevant data.

2.  **Run the Script:**


3.  **View Report:** Open the generated `performance_report.html` file in your web browser.

![image](https://github.com/user-attachments/assets/1394137a-a66d-44a5-94b2-ad73ef702c38)
![image](https://github.com/user-attachments/assets/aa649619-598b-40f0-86b0-bc1bd2d90643)
![image](https://github.com/user-attachments/assets/6e5785d1-6d15-4838-9516-492a16f08220)
![image](https://github.com/user-attachments/assets/35a424d0-691d-4335-be75-4fed65d7471c)

## NLP Details

The `nlp_utils.py` file provides functions for:

*   **Predicting question difficulty (`predict_difficulty_level`):** This function uses text length and keyword analysis to estimate the difficulty of a question.
*   **Assessing option confusingness (`assess_option_confusingness`):** This function analyzes the similarity of answer options to identify potentially confusing choices.

## Customization

*   **Data Files:** Modify the `.txt` files to use with your test data.
*   **Analysis Parameters:** Adjust parameters like accuracy thresholds for weak topics in the Python scripts.
*   **Styling:** Customize the CSS within the HTML report generation functions for different presentation styles.
*   **NLP Techniques:** Expand the `nlp_utils.py` file with more sophisticated NLP techniques for deeper analysis of quiz content.

## Contributing

Contributions to this project are welcome! Feel free to submit pull requests with bug fixes, new features, or improvements to the documentation.







