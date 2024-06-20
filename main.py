from flask import Flask, request, render_template
# Importing necessary modules from Flask to create a web application
import os
# Importing the os module to handle file system paths and operations
import docx2txt
# Importing docx2txt to extract text from .docx files
import PyPDF2
# Importing PyPDF2 to extract text from PDF files
from sklearn.feature_extraction.text import TfidfVectorizer
# Importing TfidfVectorizer from sklearn to convert text data into TF-IDF feature vectors
from sklearn.metrics.pairwise import cosine_similarity
# Importing cosine_similarity from sklearn to compute cosine similarity between vectors

# Initializing a Flask application
app = Flask(__name__)
# Configuring the upload folder for the application
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

# Function to extract text from a TXT file
def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to determine the file type and extract text accordingly
def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

# Route for the homepage
@app.route("/")
def matchresume():
    return render_template('matchresume.html')

# Route for handling the form submission
@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        # Getting the job description from the form
        job_description = request.form['job_description']
        # Getting the uploaded resume files from the form
        resume_files = request.files.getlist('resumes')

        resumes = []
        for resume_file in resume_files:
            # Saving each uploaded file to the uploads folder
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)
            # Extracting text from the saved file
            resumes.append(extract_text(filename))

        # If no resumes or job description are provided, return an error message
        if not resumes or not job_description:
            return render_template('matchresume.html', message="Please upload resumes and enter a job description.")

        # Vectorize job description and resumes using TF-IDF
        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()

        # Calculate cosine similarities between job description vector and resume vectors
        job_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_vector], resume_vectors)[0]

        # Get top 3 resumes and their similarity scores
        top_indices = similarities.argsort()[-5:][::-1]
        top_resumes = [resume_files[i].filename for i in top_indices]
        similarity_scores = [round(similarities[i], 2) for i in top_indices]

        # Render the template with the results
        return render_template('matchresume.html', message="Top matching resumes:", top_resumes=top_resumes, similarity_scores=similarity_scores)

    return render_template('matchresume.html')

# Main block to run the Flask application
if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    # Run the Flask application in debug mode
    app.run(debug=True)