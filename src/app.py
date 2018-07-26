# GENERAL Imports...
import numpy as np
import pandas as pd
import io
import os
import global_resume

# FLASK Imports...
from flask import Flask, make_response, request, render_template, jsonify
from flask_bootstrap import Bootstrap
from flask import Markup
import flask

# OCR Imports...
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi

# SKLEARN Imports...
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier


def scrape_web():
    pass

def ocr_on_pdf(resume_pdf):
    # Convert individual PDF into JPG and then OCR into STR
    pdf = wi(filename = resume_pdf, resolution = 300)
    pdfImage = pdf.convert('jpeg')

    imageBlobs = []
    for img in pdfImage.sequence:
        imgPage = wi(image = img)
        imageBlobs.append(imgPage.make_blob('jpeg'))

    recognized_text = []
    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang = 'eng')
        recognized_text.append(text)

    txt_as_str = recognized_text[0]
    return txt_as_str

def train_test_sgd_classifier():
    # Train and test algorithm
    df = pd.read_csv('../data/job_desc_csv_fixed_url.csv')
    X_train, X_test, y_train, y_test = train_test_split(df.job_descriptions, df.search_term, random_state=0)

    count_vect = CountVectorizer(stop_words='english')
    X_train_counts = count_vect.fit_transform(X_train)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf = SGDClassifier(loss='hinge', penalty='l1', alpha=1e-3, random_state=42, max_iter=5, tol=None)
    clf.fit(X_train_tfidf, y_train)

    preds = clf.predict(count_vect.transform(X_test))
    accuracy = np.mean(preds==np.array(y_test))

    return clf, count_vect, accuracy

def predict_resume(resume_text):
    # Run predict on trained algorithm
    text_as_series = pd.Series(resume_text)
    clf, count_vect, _ = train_test_sgd_classifier()
    prediction = clf.predict(count_vect.transform(text_as_series))
    return prediction[0]

def build_resume_html(resume):
    print('raw resume: ', resume)
    resume = resume.replace('\n', '<br />')
    return resume


app = Flask(__name__)

@app.route('/')
def index():
    # Load page
    return flask.render_template('index.html')



@app.route('/newlook')
def newlook():
    # Load page
    return flask.render_template('newlook.html')


@app.route('/upload_resume', methods=["POST"])
def upload_resume():
    # Accept uploaded resume and return raw text
    print('type (request)', type (request.files['data_file']))
    resume_pdf = request.files['data_file']
    if not resume_pdf:
        return "No file"

    resume_text = ocr_on_pdf(resume_pdf)
    global_resume.text = resume_text

    return flask.render_template(resume_text = resume_text)

@app.route('/demo_resumes', methods=["POST"])
def demo_resumes():
    # Accept selected demo resume and return raw text
    resumes_dict = {'mkt': 'marketing', 'dta': 'data', 'web': 'webdev', 'sls': 'sales', 'act': 'accountant'}
    print('request.form: ', request.form)
    for k, v in request.form.items():
        selected_resume = request.form[k]
    print('selected_resume: ', selected_resume)
    resume_pdf = "../data/resumes/{}_resume.pdf".format(resumes_dict[selected_resume])

    resume_text = ocr_on_pdf(resume_pdf)
    # global_resume.text = resume_text
    prediction_dict = {'JavaScript': 'Web Developer', 'Python': 'Data Scientist', 'Marketing': 'Marketing Manager', 'Sales': 'Sales Manager', 'Accounting': 'Accountant', 'Operations': 'Operations Manager'}
    resume_prediction = prediction_dict[predict_resume(resume_text)]
    return flask.jsonify(
                        resume_text = build_resume_html(resume_text),
                        resume_prediction = '<h3>'+resume_prediction+'</h3>'
                        )

# @app.route('/predict', methods=["GET"])
# def predict():
#     # Run predict function and return prediction
#     resume_text = global_resume.text
#     resume_prediction = predict_resume(resume_text)
#
#     return flask.jsonify(resume_prediction = '<h3>'+resume_prediction+'</h3>')


if __name__ == "__main__":
    Bootstrap(app)
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
