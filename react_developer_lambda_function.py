from datetime import datetime
import re
import json
import boto3
from pprint import pprint
from parser import extract_text

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

        resume_info_extraction_string = str(resume_info_extraction)
        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', resume_info_extraction_string)
        email = match.group(0)

        match_2 = re.search(r'\b\d{5}(?:-\d{4})?\b', resume_info_extraction_string)
        
        now = datetime.now()
        
        dt_email = now.strftime("%m/%d/%Y")
        
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
        
        if not match_2:
            zip_code = 'Null'
        elif match_2:
            zip_code = match_2.group(0)
        
        print(zip_code)

        if 'Coding bootcamp' or 'Coding Bootcamp' in resume_info_extraction_string:
            education = 'Education - Bootcamp'
            adequate_job_education = 'This person has adequate education.'
        else:
            education = 'Null'
            inadequate_job_education = 'This person does not have adequate education.'

        if 'ReactJS' or 'React' in resume_info_extraction_string:
            React_experience = 'Skill - React'
        elif 'React' in resume_info_extraction_string:
            React_experience = 'Skill - React'
        elif 'React.js' in resume_info_extraction_string:
            React_experience = 'Skill - React'
        else:
            React_experience = 'Null'
        
        tampa_zip_codes = ['33601', '33601', '33626', '33629', '33631', '33633', '33635', '33637', '33646', '33647', '33650', 
        '33655', '33660', '33664', '33672', '33675', '33677', '33679', '33682', '33684', '33689', '33694']
            
        if 'ReactJS' in resume_info_extraction_string and 'Coding bootcamp' or 'Coding Bootcamp' in resume_info_extraction_string and zip_code in tampa_zip_codes:
            email_message = f'Congratulations, {name} you are chosen to interview for the React Developer position! This is regarding your application on {dt_email}.'
        elif 'React' in resume_info_extraction_string and 'Coding bootcamp' or 'Coding Bootcamp' in resume_info_extraction_string and zip_code in tampa_zip_codes:
            email_message = f'Congratulations, {name} you are chosen to interview for the React Developer position! This is regarding your application on {dt_email}.'
        if zip_code not in tampa_zip_codes:
            email_message = f'Sorry, {name} but your location of {zip_code} is not in Tampa, Florida for the React Developer position. This is regarding your application on {dt_email}.'
        elif React_experience == 'Null':
            email_message = f'Sorry, {name} but you do not have either adequate experience nor adequate education for the React Developer position. This is regarding your application on {dt_email}.'
            
        client = boto3.resource('dynamodb')

        table = client.Table('React_Job_Applicants')
    
        response = table.put_item(
    
           Item={
    
               'id': dt_string,
    
               'name': name,
               
               'email': email,
               
               'zip_code': zip_code,
    
               'education': education,
               
               'react_experience': React_experience
           }
    
       )
       
        client = boto3.client('ses')
        
        email_message_2 = f'Hello, somebody just applied to your ReactJS job posting. Here is their information: name: {name}, email: {email}, zip_code: {zip_code}, education: {education}, react_experience: {React_experience}'
            
        email = client.send_email(
            Source='bburnerson840@gmail.com',
            Destination={
                'ToAddresses': [
                    email,
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
        
        email_2 = client.send_email(
            Source='ryansviglione@gmail.com',
            Destination={
                'ToAddresses': [
                    'bburnerson840@gmail.com',
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Somebody just applied to your ReactJS job!'
                },
                'Body': {
                    'Text': {
                        'Data': email_message_2
                    },
                    'Html': {
                        'Data': email_message_2
                    }
                }
            }
        )

    return {"statusCode": 200, "body": json.dumps("Thank you for submitting your resume!")}
   
