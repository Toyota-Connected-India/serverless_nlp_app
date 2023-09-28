# Enter into following docker `amazon/aws-lambda-python:3.8`

# in your terminal
docker run -ti --entrypoint /bin/bash amazon/aws-lambda-python:3.8

###### You have Entered the Docker Container #######

# commands to create a spacy layer inside `python` directory
rm -rf python && mkdir -p python



pip install -U --no-cache pip setuptools wheel -t python 
#`pip install -U --no-cache spacy -t python
pip install -U spacy urllib3==1.26.6 https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0.tar.gz -t python


# now zip all the package
yum install -y zip
zip -r spacy_layer.zip .

#### Work inside the Docker Container is Over (do not close the container ###### 

# in another terminal
docker cp container_id:/var/task/spacy_layer.zip .

# copy the zip file into s3 bucker
aws s3 cp name_of_zip_file.zip s3://s3_bucket_location

# to create a layer
aws lambda publish-layer-version \
    --layer-name $spacy_layer \  
    --description "spacy" \                 
    --content S3Bucket=s3://s3_bucket_location,S3Key=spacy_layer.zip \
    --compatible-runtimes python3.8


# you can now close the docker container that was running the image `amazon/aws-lambda-python:3.8`

