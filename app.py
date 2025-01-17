from flask import Flask, request, render_template, redirect, url_for
import os
from utils.file_processing import extract_text_from_file
from utils.text_matching import calculate_similarity, generate_visualizations
from utils.database import init_db, get_connection

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the database
init_db()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle file uploads
        cv_files = request.files.getlist('cvs')
        jd_file = request.files['jd']
        
        # Save JD file to database
        jd_filename = jd_file.filename
        jd_text = jd_file.read().decode('utf-8')
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO job_descriptions (filename, content) VALUES (?, ?)', (jd_filename, jd_text))
        jd_id = cursor.lastrowid
        
        # Save CV files and compute similarity
        cv_data = []
        for cv_file in cv_files:
            cv_filename = cv_file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_filename)
            cv_file.save(file_path)
            cv_text = extract_text_from_file(file_path)
            cv_data.append((cv_filename, cv_text))
        
        # Calculate similarity
        cv_texts = [data[1] for data in cv_data]
        similarity_scores = calculate_similarity(cv_texts, jd_text)
        
        # Store CVs and their similarity scores in the database
        for (cv_filename, cv_text), score in zip(cv_data, similarity_scores):
            cursor.execute(
                'INSERT INTO cvs (filename, content, jd_id, similarity_score) VALUES (?, ?, ?, ?)',
                (cv_filename, cv_text, jd_id, score)
            )
        
        conn.commit()
        conn.close()
        
        # Generate visuals
        chart_paths = generate_visualizations(similarity_scores, cv_files)
        
        # Redirect to results
        return render_template('results.html', scores=zip([cv.filename for cv in cv_files], similarity_scores), charts=chart_paths)
    return render_template('home.html')

@app.route('/filter_results', methods=['GET'])
def filter_results():
    min_score = float(request.args.get('min_score', 0))
    jd_id = request.args.get('jd_id')  # Assume this comes from user selection
    
    # Query the database for filtered results
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT filename, similarity_score
        FROM cvs
        WHERE jd_id = ? AND similarity_score >= ?
        ORDER BY similarity_score DESC
    ''', (jd_id, min_score))
    filtered_results = cursor.fetchall()
    conn.close()
    
    return render_template('results.html', scores=filtered_results, charts=[])

@app.route('/manage', methods=['GET'])
def manage_data():
    """Display all JDs and their associated CVs."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename FROM job_descriptions')
    jds = cursor.fetchall()
    
    data = []
    for jd in jds:
        jd_id, jd_filename = jd
        cursor.execute('SELECT id, filename, similarity_score FROM cvs WHERE jd_id = ?', (jd_id,))
        cvs = cursor.fetchall()
        data.append({'jd_id': jd_id, 'jd_filename': jd_filename, 'cvs': cvs})
    
    conn.close()
    return render_template('manage.html', data=data)

@app.route('/delete_jd/<int:jd_id>', methods=['POST'])
def delete_jd(jd_id):
    """Delete a JD and its associated CVs."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM job_descriptions WHERE id = ?', (jd_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_data'))

@app.route('/delete_cv/<int:cv_id>', methods=['POST'])
def delete_cv(cv_id):
    """Delete an individual CV."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cvs WHERE id = ?', (cv_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_data'))

@app.route('/select_jd', methods=['GET'])
def select_jd():
    """Display a list of JDs for selection."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename FROM job_descriptions')
    jds = cursor.fetchall()
    conn.close()
    return render_template('select_jd.html', jds=jds)

if __name__ == '__main__':
    app.run(debug=True)
