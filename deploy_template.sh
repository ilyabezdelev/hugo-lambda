export SOURCE_CODE_BUCKET=BUCKETNAME
export STACK_NAME=hugo-lambda
export HUGO_LAYER_FILE_NAME=hugo-layer.zip
export LIBSTDC_LAYER_FILE_NAME=libstdc-layer.zip
export AWSCLI_LAYER_FILE_NAME=awscli-layer.zip

# copy contents of layers to S3
aws s3 sync layers/ s3://${SOURCE_CODE_BUCKET}

# deploy
sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --s3-bucket ${SOURCE_CODE_BUCKET}

aws cloudformation deploy \
    --template-file packaged.yaml \
    --stack-name ${STACK_NAME} \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides LayersBucketName=${SOURCE_CODE_BUCKET} \
        HugoLayerKey=${HUGO_LAYER_FILE_NAME} \
        LibstdcLayerKey=${LIBSTDC_LAYER_FILE_NAME} \
        AWSCLILayerKey=${AWSCLI_LAYER_FILE_NAME}

aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --query 'Stacks[].Outputs'