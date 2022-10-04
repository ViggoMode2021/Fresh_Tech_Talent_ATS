"""
========================
Fresh Tech Talent ATS
========================
Contributors: Chirag Rathod (Srce Cde) and Ryan Viglione
========================
"""

from datetime import datetime
import re
import json
import boto3
from pprint import pprint
from parser import (
    extract_text,
    map_word_id,
    extract_table_info,
    get_key_map,
    get_value_map,
    get_kv_map,
)

def lambda_handler(event, context):
    textract = boto3.client("textract", region_name = 'us-east-1')
    if event:
        file_obj = event["Records"][0]
        bucketname = str(file_obj["s3"]["bucket"]["name"])
        filename = str(file_obj["s3"]["object"]["key"])

        response = textract.analyze_document(
            Document={
                "S3Object": {
                    "Bucket": bucketname,
                    "Name": filename,
                }
            },
            FeatureTypes=["FORMS", "TABLES"],
        )

        resume_info_extraction = extract_text(response, extract_by="LINE")
        
        name = resume_info_extraction[0]
        print(name)
        
        resume_info_extraction_string = str(resume_info_extraction)
        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', resume_info_extraction_string)
        email = match.group(0)

        match_2 = re.search(r'\b\d{5}(?:-\d{4})?\b', resume_info_extraction_string)
        
        now = datetime.now()
        
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        if not match_2:
            zip_code = 'Null'
            
        elif match_2:
            zip_code = match_2.group(0)

        if 'Coding bootcamp' or 'Coding Bootcamp' in resume_info_extraction_string:
            education = 'Education - Bootcamp'
            adequate_job_education = 'This person has adequate education.'
        
        else:
            education = 'Null'
            adequate_job_education = 'This person does not have adequate education.'
            
        match_3 = re.search(r'(?:[A-Z][a-z.-]+[ ]?)+', resume_info_extraction_string)
        city = match_3.group(0)
        
        if city in resume_info_extraction_string:
            city = city
        
        else:
            city = 'Null'

        if 'Python' in resume_info_extraction_string:
            python_experience = 'Skill - Python'
            adequate_python_experience = 'This person has adequate Python experience.'
            
        else:
            adequate_python_experience = 'This person does not have adequate Python experience.'
            python_experience = 'Null'
            
        if adequate_job_education and adequate_python_experience:
            email_message = 'Congratulations, you are chosen to move to the second round!'
        else:
            email_message = 'Sorry, but you do not have either adequate experience nor adequate education'
            
        client = boto3.resource('dynamodb')

        table = client.Table('Job_Applicants')
    
        response = table.put_item(
    
           Item={
    
               'id': dt_string,
    
               'name': name,
               
               'email': email,
               
               'city': city,
    
               'zip_code': zip_code,
    
               'education': education,
               
               'python_experience': python_experience
           }
    
       )
       
        client = boto3.client('ses')
            
        response = client.send_email(
            Source='bburnerson840@gmail.com',
            Destination={
                'ToAddresses': [
                    'ryansviglione@gmail.com',
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Your job application status'
                },
                'Body': {
                    'Text': {
                        'Data': email_message
                    },
                    'Html': {
                        'Data': email_message
                    }
                }
            }
        )

    return {"statusCode": 200, "body": json.dumps("Thank you for submitting your resume1!")}
