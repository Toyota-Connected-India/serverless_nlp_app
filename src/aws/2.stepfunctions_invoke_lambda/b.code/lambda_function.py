import json
import boto3
import pprint
import re 
import uuid
import os 

def lambda_handler(event, context):
    '''
    Triggers a StepFunctions workflow 
    when a file lands in a s3 bucket
    '''
    lambda_name = re.split('/',context.log_group_name)[-1]
    
    STATE_MACHINE = os.getenv("STATE_MACHINE_NAME")
    ACCOUNT_ID = os.getenv("ACCOUNT_ID")
    REGION = os.getenv("AWS_REGION")
    INTERMEDIARY_BUCKET_NAME = os.getenv("INTERMEDIARY_BUCKET_NAME")
    FINAL_BUCKET_NAME = os.getenv("FINAL_BUCKET_NAME")

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    file_name = file_key
    file_name_w_extension = re.split('/',file_key)[-1]
    file_name_wo_extension = re.sub('\.\w{3}','',file_name_w_extension)

    input_to_sf = {
        "input_bucket_name": bucket_name,
        "intermediary_output_bucket_name": INTERMEDIARY_BUCKET_NAME,
        "final_output_bucket_name": FINAL_BUCKET_NAME,
        "file_key": file_key
    }

    print(f'arn:aws:states:{REGION}:{ACCOUNT_ID}:stateMachine:{STATE_MACHINE}')
    print(input_to_sf)
    # unique identifier limited to char length of 80
    unique_state_machine_name = f"{str(uuid.uuid4())[-8:]}--{file_name_wo_extension}"[0:79]
    stepFunction = boto3.client('stepfunctions')
    response = stepFunction.start_execution(
        name=unique_state_machine_name,
        stateMachineArn=f'arn:aws:states:{REGION}:{ACCOUNT_ID}:stateMachine:{STATE_MACHINE}',
        input=json.dumps(
            input_to_sf,
            indent=4   
        )
    )

    return {"file_name": file_name_wo_extension, 
    "message": "Step Functions pipeline successfully started"}
