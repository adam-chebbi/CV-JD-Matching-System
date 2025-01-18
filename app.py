from flask import Flask, request, render_template, redirect, url_for
import os
from utils.file_processing import extract_text_from_file
from utils.text_matching import calculate_similarity, generate_visualizations
from utils.database import init_db, get_connection

# Initialize the app and database
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
init_db()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle CV uploads
        cv_files = request.files.getlist('cvs')
        jd_file = request.files.get('jd')
        jd_text_input = request.form.get('jd_text')
        
        # Ensure either JD file or text is provided
        if not jd_file and not jd_text_input:
            return render_template('home.html', error="Please provide either a JD file or enter JD text.")
        
        # Process JD text
        if jd_file:
            jd_filename = jd_file.filename
            jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
            jd_file.save(jd_path)
            jd_text = extract_text_from_file(jd_path)
        else:
            jd_text = jd_text_input.strip()

        # Save JD to the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO job_descriptions (filename, content) VALUES (?, ?)', 
                       (jd_file.filename if jd_file else "Text Input", jd_text))
        jd_id = cursor.lastrowid

        # Process CV files
        cv_data = []
        for cv_file in cv_files:
            cv_filename = cv_file.filename
            cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_filename)
            cv_file.save(cv_path)
            cv_text = extract_text_from_file(cv_path)
            cv_data.append((cv_filename, cv_text))
        
        # Calculate similarity scores
        cv_texts = [data[1] for data in cv_data]
        similarity_scores = calculate_similarity(cv_texts, jd_text)

        # Save CVs and their similarity scores in the database
        for (cv_filename, cv_text), score in zip(cv_data, similarity_scores):
            cursor.execute(
                'INSERT INTO cvs (filename, content, jd_id, similarity_score) VALUES (?, ?, ?, ?)',
                (cv_filename, cv_text, jd_id, score)
            )
        
        conn.commit()
        conn.close()

        # Generate visualizations
        chart_paths = generate_visualizations(similarity_scores, cv_files)

        # Redirect to results page
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

    return render_template('results.html', scores=filtered_results)

@app.route('/manage', methods=['GET'])
def manage_data():
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM job_descriptions WHERE id = ?', (jd_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_data'))

@app.route('/delete_cv/<int:cv_id>', methods=['POST'])
def delete_cv(cv_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cvs WHERE id = ?', (cv_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_data'))

if __name__ == '__main__':
    app.run(debug=True)
