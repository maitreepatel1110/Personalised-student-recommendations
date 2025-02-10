import json
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from nlp_utils import predict_difficulty_level, assess_option_confusingness
import base64
import io


def analyze_quiz_data_advanced(quiz_data, quiz_submission_data):

    questions = quiz_data['quiz']['questions']
    total_questions_quiz_data = len(questions)
    response_map = quiz_submission_data.get('response_map', {})

    final_score = quiz_submission_data.get('final_score')
    negative_score = quiz_submission_data.get('negative_score')
    correct_answers_count = quiz_submission_data.get('correct_answers')
    incorrect_answers_count = quiz_submission_data.get('incorrect_answers')
    source = quiz_submission_data.get('source')
    quiz_type = quiz_submission_data.get('type')
    started_at = quiz_submission_data.get('started_at')
    ended_at = quiz_submission_data.get('ended_at')
    duration = quiz_submission_data.get('duration')
    better_than = quiz_submission_data.get('better_than')
    total_questions = quiz_submission_data.get('total_questions')

    topic_performance = defaultdict(lambda: {'correct': 0, 'total': 0})
    difficulty_performance = defaultdict(lambda: {'correct': 0, 'total': 0})
    correct_count = 0

    question_categories = {
        "Easy - Correct": [],
        "Easy - Incorrect": [],
        "Medium - Correct": [],
        "Medium - Incorrect": [],
        "Hard - Correct": [],
        "Hard - Incorrect": []
    }

    default_difficulty = quiz_data['quiz'].get(
        'difficulty_level', 'Not Specified')

    for question in questions:
        question_id = str(question['id'])
        topic = question['topic']

        difficulty = question.get('difficulty_level', default_difficulty)

        if difficulty is None or difficulty == "Not Specified":
            question['difficulty_level'] = predict_difficulty_level(
                question['description'], question['detailed_solution'])
            difficulty = question['difficulty_level']

        if difficulty is None:
            difficulty = "Not Specified"

        is_correct = False
        if question_id in response_map:
            selected_option_id = str(response_map[question_id])

            for option in question['options']:
                if str(option['id']) == selected_option_id:
                    if option['is_correct']:
                        is_correct = True
                    break

        topic_performance[topic]['total'] += 1
        difficulty_performance[difficulty]['total'] += 1

        if is_correct:
            topic_performance[topic]['correct'] += 1
            difficulty_performance[difficulty]['correct'] += 1
            correct_count += 1

        if is_correct:
            category = f"{difficulty} - Correct"
        else:
            category = f"{difficulty} - Incorrect"
        question_categories[category].append(question)

        confusingness_score = assess_option_confusingness(question['options'])
        question['confusingness'] = confusingness_score

    overall_accuracy = (correct_count / total_questions_quiz_data) * \
        100 if total_questions_quiz_data > 0 else 0

    weak_topics = []
    for topic, performance in topic_performance.items():
        accuracy = (performance['correct'] / performance['total']
                    ) * 100 if performance['total'] > 0 else 0
        if accuracy < 60:
            weak_topics.append({'topic': topic, 'accuracy': accuracy})

    weak_topics = sorted(weak_topics, key=lambda x: x['accuracy'])

    difficulty_analysis = []
    for difficulty, performance in difficulty_performance.items():
        accuracy = (performance['correct'] / performance['total']
                    ) * 100 if performance['total'] > 0 else 0
        difficulty_analysis.append(
            {'difficulty': difficulty, 'accuracy': accuracy})

    difficulty_analysis = sorted(
        difficulty_analysis, key=lambda x: x['accuracy'])

    recommendations = []

    if weak_topics:
        recommendations.append(
            f"Focus on improving your understanding of the following topics: {', '.join([t['topic'] for t in weak_topics])}")
    else:
        recommendations.append(
            "Good job! You have a strong understanding of all topics covered in this quiz.")

    recommendations.append(
        "Consider reviewing the detailed solutions for questions you answered incorrectly to reinforce your understanding.")

    recommendations.append("\nQuestion Category Analysis:")
    for category, questions_list in question_categories.items():
        num_incorrect = len(questions_list)
        recommendations.append(f"  - {category} (Count: {num_incorrect})")
        if num_incorrect > 0:
            recommendations.append("     Sample questions:")
            for i in range(min(3, num_incorrect)):
                recommendations.append(
                    f"       - {questions_list[i]['description'][:100]}...")

    student_persona = generate_student_persona(
        overall_accuracy, weak_topics, difficulty_analysis)

    results = {
        "overall_accuracy": overall_accuracy,
        "weak_topics": weak_topics,
        "difficulty_analysis": difficulty_analysis,
        "recommendations": recommendations,
        "question_categories": question_categories,
        "student_persona": student_persona,
        "final_score": final_score,
        "negative_score": negative_score,
        "correct_answers": correct_answers_count,
        "incorrect_answers": incorrect_answers_count,
        "source": source,
        "type": quiz_type,
        "started_at": started_at,
        "ended_at": ended_at,
        "duration": duration,
        "better_than": better_than,
        "total_questions": total_questions
    }

    return results


def generate_student_persona(overall_accuracy, weak_topics, difficulty_analysis):

    persona = {}

    if overall_accuracy >= 90:
        persona['name'] = "The Ace"
        persona['description'] = "Consistently demonstrates mastery. Excels in understanding and application."
        persona['strengths'] = "Strong grasp of fundamental concepts, excellent problem-solving skills."
        persona['weaknesses'] = "Potential overconfidence, may benefit from exploring advanced topics."
    elif overall_accuracy >= 70:
        persona['name'] = "The Diligent Learner"
        persona['description'] = "Shows good understanding with room for improvement. Responds well to targeted practice."
        persona['strengths'] = "Solid foundation, consistent effort, willing to learn."
        persona['weaknesses'] = "Inconsistencies in applying knowledge, needs to reinforce weaker areas."
    else:
        persona['name'] = "The Budding Biologist"
        persona['description'] = "Demonstrates potential but struggles with core concepts. Requires focused attention and practice."
        persona['strengths'] = "Enthusiastic and curious."
        persona['weaknesses'] = "Gaps in foundational knowledge, needs a structured approach to learning."

    if weak_topics:
        persona['specific_weaknesses'] = f"Struggles with: {', '.join([t['topic'] for t in weak_topics])}"
    else:
        persona['specific_weaknesses'] = "No significant topic weaknesses identified."

    if difficulty_analysis and all(item['difficulty'] in ["Not Specified", None, ""] for item in difficulty_analysis) is False:
        valid_difficulties = [
            d for d in difficulty_analysis if d['difficulty'] != "Not Specified"]
        easiest = valid_difficulties[-1]['difficulty'] if valid_difficulties else "Unknown"
        hardest = valid_difficulties[0]['difficulty'] if valid_difficulties else "Unknown"
        persona['difficulty_profile'] = f"Excels at {easiest} difficulty, struggles with {hardest}."
    else:
        persona['difficulty_profile'] = "Difficulty level performance is not specified"

    return persona


def predict_neet_rank(quiz_accuracy):

    predicted_rank = predict_rank_from_dataset(quiz_accuracy)

    return predicted_rank


def predict_rank_from_dataset(quiz_accuracy):

    global neet_data

    predicted_score = quiz_accuracy / 100 * 720

    nearest_index = np.argmin(np.abs(neet_data['score'] - predicted_score))

    predicted_rank = neet_data['rank'][nearest_index]

    return predicted_rank


neet_data = {
    'score': [100, 150, 200, 250, 300, 350, 400, 450, 500, 510, 520, 530, 640, 650, 660, 670, 680, 690, 700, 710, 715, 720],
    'rank': [700000, 650000, 600000, 550000, 450000, 400000, 350000, 300000, 250000, 240000, 230000, 220000, 110000, 100000, 90000, 80000, 70000, 60000, 50000, 25000, 12500, 1]
}

neet_data['score'] = np.array(neet_data['score'])
neet_data['rank'] = np.array(neet_data['rank'])


def generate_html_report(analysis_results):

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quiz Performance Analysis</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            h2 {{ color: #666; }}
            .section {{ margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; }}
            .insight {{ margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h1>Quiz Performance Analysis</h1>

        <div class="section">
            <h2>Overall Performance</h2>
            <p class="insight"><strong>Overall Accuracy:</strong> {analysis_results['overall_accuracy']:.2f}%</p>
            <p class="insight"><strong>Final Score:</strong> {analysis_results['final_score']}</p>
            <p class="insight"><strong>Negative Score:</strong> {analysis_results['negative_score']}</p>
            <p class="insight"><strong>Correct Answers:</strong> {analysis_results['correct_answers']}</p>
            <p class="insight"><strong>Incorrect Answers:</strong> {analysis_results['incorrect_answers']}</p>
            <p class="insight"><strong>Source:</strong> {analysis_results['source']}</p>
            <p class="insight"><strong>Type:</strong> {analysis_results['type']}</p>
            <p class="insight"><strong>Started At:</strong> {analysis_results['started_at']}</p>
            <p class="insight"><strong>Ended At:</strong> {analysis_results['ended_at']}</p>
            <p class="insight"><strong>Duration:</strong> {analysis_results['duration']}</p>
            <p class="insight"><strong>Better Than:</strong> {analysis_results['better_than']}%</p>
            <p class="insight"><strong>Total Questions:</strong> {analysis_results['total_questions']}</p>
        </div>

        <div class="section">
            <h2>Weak Topics</h2>
            <ul>
                {"".join(f"<li>{topic_data['topic']}: {topic_data['accuracy']:.2f}% accuracy</li>" for topic_data in analysis_results['weak_topics'])}
            </ul>
        </div>

        <div class="section">
            <h2>Difficulty Level Analysis</h2>
            <ul>
                {"".join(f"<li>{difficulty_data['difficulty']}: {difficulty_data['accuracy']:.2f}% accuracy</li>" for difficulty_data in analysis_results['difficulty_analysis'])}
            </ul>
        </div>

        <div class="section">
            <h2>Recommendations</h2>
            <ul>
                {"".join(f"<li>{recommendation}</li>" for recommendation in analysis_results['recommendations'])}
            </ul>
        </div>

        <div class="section">
            <h2>Student Persona</h2>
            <p class="insight"><strong>Name:</strong> {analysis_results['student_persona']['name']}</p>
            <p class="insight"><strong>Description:</strong> {analysis_results['student_persona']['description']}</p>
            <p class="insight"><strong>Strengths:</strong> {analysis_results['student_persona']['strengths']}</p>
            <p class="insight"><strong>Weaknesses:</strong> {analysis_results['student_persona']['weaknesses']}</p>
        </div>
    </body>
    </html>
    """
    return html_content


with open('current_test_data.txt', 'r') as f:
    quiz_data = json.load(f)
with open('quiz_submission_data.txt', 'r') as f:
    quiz_submission_data = json.load(f)

analysis_results = analyze_quiz_data_advanced(quiz_data, quiz_submission_data)


html_report = generate_html_report(analysis_results)


with open('report.html', 'w') as f:
    f.write(html_report)

print("HTML report generated successfully! Open 'report.html' in your browser to view.")
