import re
import boto3


def lambda_handler(event, context):
    '''
    runs simple regex matches to capture email and phone number
    '''
    # the following code is just placeholder to check if pipeline works
    # to be edited

    s3_client = boto3.client('s3')

    input_bucket_name = event['input_bucket_name']
    intermediary_output_bucket_name = event['intermediary_output_bucket_name']
    file_key = event['file_key']

    # Use the client to get the object
    response = s3_client.get_object(Bucket=input_bucket_name, Key=file_key)
    text = response['Body'].read().decode('utf-8')

    email_pattern_verbose = r"""
        (\w+)       # Match one or more word characters (username part)
        [-_.]?      # Match an optional hyphen, underscore, or dot
        (\w+)       # Match one or more word characters (domain part)
        @           # Match the literal @ symbol
        ((\w|-)+)   # Match one or more word characters or hyphens (domain name)
        \.          # Match a literal dot
        \w+         # Match one or more word characters (top-level domain)
    """

    email_pattern = re.compile(email_pattern_verbose, re.VERBOSE|re.MULTILINE)


    # the below is a simple regex, you may want a more complicated regex
    # phone_pattern = r'\+(?P<country_code>\d+)\s(?P<phone_number>\d+)'

    phone_pattern_verbose = r"""
        (?:\+\d{1,3}\s)?       # Optional international code (+xx) followed by space
        (?:\d{3}[-\s]|\(\d{3}\)\s)?  # Area code with or without parentheses and followed by space or hyphen
        \d{3}                   # First three digits
        [-\s]?                  # Optional separator (hyphen or space)
        \d{3}                   # Next three digits
        [-\s]?                  # Optional separator (hyphen or space)
        \d{4}                   # Last four digits
    """

    # Compile the regex pattern with re.VERBOSE flag
    phone_pattern = re.compile(phone_pattern_verbose, re.VERBOSE|re.MULTILINE)

    new_text = email_pattern.sub('<EMAIL>',text)
    new_text = phone_pattern.sub('<PHONE>',new_text)

    s3_client.put_object(
        Bucket=intermediary_output_bucket_name, 
        Key=file_key, 
        Body=new_text.encode('utf-8')
    )

    input_to_next_lambda = {
        'input_bucket_name': event['intermediary_output_bucket_name'],
        'output_bucket_name': event['final_output_bucket_name'],
        'file_key': event['file_key']
    }

    return input_to_next_lambda