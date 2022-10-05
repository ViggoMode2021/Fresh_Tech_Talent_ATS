from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
import boto3
from dotenv import load_dotenv, find_dotenv
from botocore.exceptions import ClientError

application = Flask(__name__)

load_dotenv(find_dotenv())

dotenv_path = os.path.join(os.path.dirname(__file__), ".env-flask")
load_dotenv(dotenv_path)
application.secret_key = os.getenv("SECRET_KEY")

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

BUCKET_NAME = 'textract-example-bucket-vig'

@application.route('/')
def sign_up():
    return render_template("sign_up.html")

@application.route('/python_job_submit', methods=['POST'])
def python_job_submit():
    if request.method == 'POST':
        resume = request.files['file']
        if resume:
            filename = secure_filename(resume.filename)
            resume.save(filename)
            s3.upload_file(
                    Bucket=BUCKET_NAME,
                    Filename=filename,
                    Key=filename
                )
            flash('Thank you for submitting your resume!')
            return render_template('sign_up.html')

if __name__ == '__main__':
    application.run(debug=True)
