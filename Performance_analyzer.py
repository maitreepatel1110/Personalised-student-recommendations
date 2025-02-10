import json
import matplotlib.pyplot as plt
import numpy as np
import datetime
from itertools import cycle  
import base64
import io

def analyze_performance_data(performance_data):
   

   
    titles = [item['quiz']['title'] for item in performance_data]
    scores = [item['score'] for item in performance_data]
    accuracies = [float(item['accuracy'].replace("%", "")) for item in performance_data]  
    submitted_dates = [item['submitted_at'] for item in performance_data]
    topics = [item['quiz']['topic'] for item in performance_data]
    total_questions = [item['total_questions'] for item in performance_data]
    incorrect_answers = [item['incorrect_answers'] for item in performance_data] 
    correct_answers = [item['correct_answers'] for item in performance_data] 

    
    dates = [datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f+05:30") for date_str in submitted_dates]

    
    sorted_indices = np.argsort(dates)
    dates = [dates[i] for i in sorted_indices]
    titles = [titles[i] for i in sorted_indices]
    scores = [scores[i] for i in sorted_indices]
    accuracies = [accuracies[i] for i in sorted_indices]
    topics = [topics[i] for i in sorted_indices]  
    total_questions = [total_questions[i] for i in sorted_indices] 
    incorrect_answers = [incorrect_answers[i] for i in sorted_indices] 
    correct_answers = [correct_answers[i] for i in sorted_indices]

    
    average_score = np.mean(scores)
    highest_score = np.max(scores)
    lowest_score = np.min(scores)
    average_accuracy = np.mean(accuracies)

  
    topic_performance = {}
    for i, topic in enumerate(topics):
        if topic in topic_performance:
            topic_performance[topic]['accuracies'].append(accuracies[i])
            topic_performance[topic]['scores'].append(scores[i])
        else:
            topic_performance[topic] = {'accuracies': [accuracies[i]], 'scores': [scores[i]]}

    topic_insights = {}
    for topic, data in topic_performance.items():
        avg_accuracy = np.mean(data['accuracies'])
        topic_insights[topic] = avg_accuracy

    
    strong_topics = {k: v for k, v in topic_insights.items() if v >= 75}
    weak_topics = {k: v for k, v in topic_insights.items() if v < 60}

   
    score_chart = generate_bar_chart(titles, scores)
    accuracy_chart = generate_line_chart(dates, accuracies)
    scatter_chart = generate_scatter_plot(scores, accuracies)
    topic_chart = generate_topic_chart(topic_insights)


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
            .graph {{ width: 600px; }}
        </style>
    </head>
    <body>
        <h1>Quiz Performance Analysis</h1>
        <div class="section">
            <h2>Overall Performance</h2>
            <p class="insight"><strong>Average Score:</strong> {average_score:.2f}</p>
            <p class="insight"><strong>Highest Score:</strong> {highest_score:.2f}</p>
            <p class="insight"><strong>Lowest Score:</strong> {lowest_score:.2f}</p>
            <p class="insight"><strong>Average Accuracy:</strong> {average_accuracy:.2f}%</p>
        </div>

        <div class="section">
            <h2>Topic Performance</h2>
            <p class="insight"><strong>Strong Topics (Accuracy >= 75%):</strong> {', '.join(strong_topics.keys()) or 'None'}</p>
            <p class="insight"><strong>Weak Topics (Accuracy < 60%):</strong> {', '.join(weak_topics.keys()) or 'None'}</p>
        </div>

        <div class="section">
            <h2>Graphs</h2>
            <img src="data:image/png;base64,{score_chart}" alt="Scores by Quiz Title" class="graph">
            <img src="data:image/png;base64,{accuracy_chart}" alt="Accuracy Over Time" class="graph">
            <img src="data:image/png;base64,{scatter_chart}" alt="Score vs Accuracy" class="graph">
            <img src="data:image/png;base64,{topic_chart}" alt="Average Accuracy by Topic" class="graph">
        </div>
    </body>
    </html>
    """

    return html_content

def generate_bar_chart(titles, scores):
    plt.figure(figsize=(14, 7))
    plt.bar(titles, scores, color="#66b3ff")
    plt.xlabel("Quiz Title")
    plt.ylabel("Score")
    plt.title("Scores by Quiz Title")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')

def generate_line_chart(dates, accuracies):
    plt.figure(figsize=(14, 7))
    plt.plot(dates, accuracies, marker='o', linestyle='-', color="#ff7043")
    plt.xlabel("Date")
    plt.ylabel("Accuracy (%)")
    plt.title("Accuracy Over Time")
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')

def generate_scatter_plot(scores, accuracies):
    plt.figure(figsize=(8, 6))
    plt.scatter(scores, accuracies, color="#9575cd", alpha=0.7)
    plt.xlabel("Score")
    plt.ylabel("Accuracy (%)")
    plt.title("Score vs Accuracy")
    plt.grid(True)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')

def generate_topic_chart(topic_insights):
    topic_names = list(topic_insights.keys())
    topic_avg_accuracies = list(topic_insights.values())

    plt.figure(figsize=(12, 6))
    plt.bar(topic_names, topic_avg_accuracies, color="#4db6ac")
    plt.xlabel("Topic")
    plt.ylabel("Average Accuracy (%)")
    plt.title("Average Accuracy by Topic")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')

if __name__ == "__main__":
    
    with open('Performance_data.txt', 'r') as f:
        performance_data = json.load(f)


    html_report = analyze_performance_data(performance_data)
    with open('performance_report.html', 'w') as f:
        f.write(html_report)

    print("Performance report generated successfully at performance_report.html")
