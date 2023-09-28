import spacy
import boto3

def lambda_handler(event, context):
    '''
    runs spacy model and predicts names in text
    '''
    # the following code is just placeholder

    nlp = spacy.load('en_core_web_sm')

    s3_client = boto3.client('s3')

    input_bucket_name = event['input_bucket_name']
    output_bucket_name = event['output_bucket_name']
    file_key = event['file_key']


    # Use the client to get the object
    response = s3_client.get_object(Bucket=input_bucket_name, Key=file_key)
    text = response['Body'].read().decode('utf-8')

    # Process the text with spaCy
    doc = nlp(text)

    # Iterate through the detected entities and print the names
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            text = text.replace(ent.text, "<NAME>")

    s3_client.put_object(
        Bucket=output_bucket_name, 
        Key=file_key, 
        Body=text.encode('utf-8')
    )

    output = {
        'output_bucket_name': output_bucket_name,
        'file_key': file_key,
        'message': 'PII Redaction Pipeline worked successfully'
    }
    return output