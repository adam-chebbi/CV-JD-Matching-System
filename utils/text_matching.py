from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import os

# Load BERT model
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(cv_texts, jd_text):
    # Generate embeddings for CVs and JD
    all_texts = cv_texts + [jd_text]
    embeddings = bert_model.encode(all_texts)
    
    jd_embedding = embeddings[-1]  # Last embedding is for the JD
    cv_embeddings = embeddings[:-1]
    
    # Calculate cosine similarity
    scores = cosine_similarity(cv_embeddings, [jd_embedding]).flatten()
    return scores

def generate_visualizations(similarity_scores, cv_files):
    # File paths for saving charts
    bar_chart_path = './static/similarity_bar_chart.png'
    histogram_path = './static/similarity_histogram.png'
    pie_chart_path = './static/similarity_pie_chart.png'
    
    # Bar Chart
    plt.figure(figsize=(10, 6))
    plt.bar([cv.filename for cv in cv_files], similarity_scores, color='blue')
    plt.xlabel('CVs')
    plt.ylabel('Similarity Score')
    plt.title('CV-JD Similarity Scores')
    plt.savefig(bar_chart_path)
    plt.close()
    
    # Histogram
    plt.figure(figsize=(10, 6))
    plt.hist(similarity_scores, bins=10, color='green', alpha=0.7)
    plt.xlabel('Similarity Scores')
    plt.ylabel('Frequency')
    plt.title('Distribution of Similarity Scores')
    plt.savefig(histogram_path)
    plt.close()
    
    # Pie Chart
    high_relevance = sum(1 for score in similarity_scores if score >= 0.8)
    moderate_relevance = sum(1 for score in similarity_scores if 0.5 <= score < 0.8)
    low_relevance = sum(1 for score in similarity_scores if score < 0.5)
    
    labels = ['Highly Relevant', 'Moderately Relevant', 'Not Relevant']
    sizes = [high_relevance, moderate_relevance, low_relevance]
    colors = ['gold', 'lightblue', 'lightcoral']
    
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Relevance Distribution')
    plt.savefig(pie_chart_path)
    plt.close()
    
    return [bar_chart_path, histogram_path, pie_chart_path]