# CV-JD Similarity Matching System

## Overview
The CV-JD Similarity Matching System is designed to help users upload resumes (CVs) and Job Descriptions (JDs) to compute similarity scores. The system utilizes advanced text processing and machine learning techniques to provide an intuitive interface for uploading files, calculating similarity scores, and visualizing the results.

## Core Features
### File Uploads for CVs and JDs
- Upload resumes (CVs) and job descriptions (JDs) in **PDF** or **DOCX** formats.
- Direct input of JDs as plain text through a user-friendly interface.

### Matching and Similarity Calculation
- Calculates a similarity score for each CV-JD pair using algorithms like **TF-IDF** or embeddings (e.g., **BERT**).

### Display of Results
- Shows similarity scores for each CV-JD pair.
- Provides detailed statistics and visualizations, such as bar charts and score distributions.

### Interactive Interface
- **Home Page:** Upload/select CVs and JDs and compute matches.
- **Selection Page:** View similarity scores for CVs matched to a selected JD, with sorting and filtering options.

### Backend & File Processing
- Utilizes Python libraries for text extraction, similarity computation, and data visualization.

## Detailed Specifications
### 1. File Handling
- Supports file uploads in `.pdf` and `.docx` formats.
- Extracts text from files using libraries like `PyPDF2` and `python-docx`.
- Allows direct text input for JDs.

### 2. Text Preprocessing
- Normalizes text (lowercase, removes stop words and punctuation).
- Tokenizes, lemmatizes, or stems words using `nltk` or `spaCy`.

### 3. Matching Algorithm
- Uses **TF-IDF** or **BERT embeddings** for text similarity.
- Computes similarity scores using **cosine similarity**.
- Scores range from 0 (no similarity) to 1 (perfect match).

### 4. Statistics and Visualizations
- **Similarity Scores:** Displays sorted similarity scores for CV-JD pairs.
- **Charts/Graphs:**
  - Bar chart for similarity scores.
  - Histogram for score distribution.
  - Pie chart for high vs. low similarity matches.
- Visualization libraries: `matplotlib`, `seaborn`, or `plotly`.

### 5. Interface Pages
#### Home Page
- Upload/select CVs and JDs.
- "Compute Match" button triggers the similarity computation.
- Displays results in a table format.

#### Selection Page
- Lists available JDs.
- Displays similarity scores for CVs matched to the selected JD.
- Allows sorting and filtering by score thresholds.

### 6. Tech Stack
#### Backend
- Python (Flask/Django for the web interface).

#### Text Processing
- Libraries: `nltk`, `spaCy`, `PyPDF2`, `python-docx`.

#### Similarity Calculation
- Libraries: `scikit-learn` (for TF-IDF and cosine similarity), `transformers` (for BERT embeddings).

#### Visualization
- Libraries: `matplotlib`, `seaborn`, `plotly`.

#### Frontend (Optional)
- HTML, CSS, JavaScript (Flask/Django templates).

#### Database (Optional)
- Store uploaded CVs and JDs for future use.

## Processing and Display Workflow
1. Extract text from uploaded files.
2. Preprocess text data (tokenization, lemmatization, etc.).
3. Compute similarity between CVs and JDs.
4. Display results in tables and visualizations.

## Final Deliverables
1. **Python Backend**: Flask/Django application for file handling and similarity calculations.
2. **Web Interface**: User-friendly pages for uploading files and viewing results.
3. **Text Matching Logic**: Implemented using TF-IDF or BERT embeddings.
4. **Visualizations**: Graphs and charts for similarity scores.

## Libraries Used
- **Backend**: Flask/Django
- **Text Processing**: nltk, spaCy, PyPDF2, python-docx
- **Similarity Calculation**: scikit-learn, transformers
- **Visualization**: matplotlib, seaborn, plotly
