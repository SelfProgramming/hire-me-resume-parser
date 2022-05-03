from urllib.request import urlopen, Request
from pyresparser import ResumeParser
import io, base64, os, json, uuid
import boto3

def upload(event, context):
    s3 = boto3.client('s3')

    eventBody = base64.b64decode(event["body"])

    key = str(uuid.uuid4()) + '.pdf'
    bucket_name = os.environ['BUCKET_NAME']
 
    s3.put_object(Bucket=bucket_name, Key=key, Body=eventBody)
    url = s3.generate_presigned_url(ClientMethod='get_object', Params={
        'Bucket': bucket_name,
        'Key': key
    })

    body = {
        "message": "Success!",
        "fileLink": url,
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def parse(event, context):
    s3_resume_link = event["body"]
    req = Request(s3_resume_link)
    pdf_file = urlopen(req).read()

    pdf_bytes = io.BytesIO(pdf_file)
    pdf_bytes.name = "cv.pdf"

    data = ResumeParser(pdf_bytes).get_extracted_data()
    body = {
        "message": "Success!",
        "data": data
    } 

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
