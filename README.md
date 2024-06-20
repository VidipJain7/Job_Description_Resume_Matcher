# Job Description and Resume Matcher

## Project Overview

The Job Description and Resume Matcher is a web application designed to help employers and recruiters efficiently match job descriptions with the most relevant resumes. By leveraging Natural Language Processing (NLP) techniques, the application analyzes the content of job descriptions and resumes to determine the best matches based on similarity scores.

## Features

- **Text Extraction:** Supports PDF, DOCX, and TXT file formats for resume uploads.
- **Natural Language Processing:** Uses TF-IDF Vectorization and Cosine Similarity to match job descriptions with resumes.
- **Web Interface:** User-friendly interface built with Flask and Bootstrap for easy interaction.
- **Top Matches:** Displays the top 5 resumes that best match the job description along with their similarity scores.

## Technologies Used

- **Backend:** Python, Flask
- **NLP:** Scikit-learn (TF-IDF Vectorizer, Cosine Similarity)
- **File Handling:** PyPDF2, docx2txt
- **Frontend:** HTML, CSS, Bootstrap
