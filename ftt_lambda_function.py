"""
-*- coding: utf-8 -*-
========================
AWS Lambda
========================
Contributor: Chirag Rathod (Srce Cde)
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

        #print(f"Bucket: {bucketname} ::: Key: {filename}")

        response = textract.analyze_document(
            Document={
                "S3Object": {
                    "Bucket": bucketname,
                    "Name": filename,
                }
            },
            FeatureTypes=["FORMS", "TABLES"],
        )

        #print(json.dumps(response))

        raw_text = extract_text(response, extract_by="LINE")
        word_map = map_word_id(response)
        table = extract_table_info(response, word_map)
        key_map = get_key_map(response, word_map)
        value_map = get_value_map(response, word_map)
        final_map = get_kv_map(key_map, value_map)

        #print(json.dumps(table))
        #print(json.dumps(final_map))
        #print(raw_text)
        first_item = raw_text[0]
        print(first_item)
        
        line = str(raw_text)
        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)
        email = match.group(0)
        print(email)
        
        match_2 = re.search(r'\b\d{5}(?:-\d{4})?\b', line)
        
        now = datetime.now()
        
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        print(dt_string)
        
        if not match_2:
            print('Zip Code is null')
            
        elif match_2:
            zip_code = match_2.group(0)
            print(zip_code)
        
        if 'Coding bootcamp' in line:
            education = 'Education - Bootcamp'
        
        else:
            education = 'No bootcamp education'
            
        match_3 = re.search(r'(?:[A-Z][a-z.-]+[ ]?)+', line)
        city = match_3.group(0)
        print(city)
        
        if 'Python' in line:
            python_experience = 'Skill - Python'
            
        else:
            python_experience = 'No python experience'
            
        client = boto3.resource('dynamodb')

        table = client.Table('Job_Applicants')
    
        response = table.put_item(
    
           Item={
    
               'id': dt_string,
    
               'name': first_item,
               
               'email': email,
    
               'zip_code': zip_code,
    
               'education': education,
               
               'python_experience': python_experience
           }
    
       )

    return {"statusCode": 200, "body": json.dumps("Thanks from Srce Cde!")}
