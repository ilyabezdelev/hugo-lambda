# Overview

`hugo-lambda` enables running static website generator Hugo inside AWS Lambda.

The repo includes the following contents:
* `app` - Lambda's Python code.
* `demo_site` - demo Hugo site you can use for testing.
* `template.yml` - AWS SAM template that deploys the app to AWS
* `deploy_template.sh` - shell script that packages dependencies and deploys the SAM template

# 1. Pre-requisites

* Read my blog post [How to build a Hugo website in AWS Lambda and deploy it to S3](https://bezdelev.com/hacking/hugo-aws-lambda-static-website-amazon-s3/) to understand the concepts.
* Follow steps 1, 2 and 3 to obtain dependencies: `hugo` binary, `libstdc++` library and `AWS CLI` packaged with all of its dependencies. These dependencies are not included in this repository to avoid licensing issues. You can download pre-packaged layers using links in my blog post.
* Place zipped files from the previous step in directory `layers`.
* Install AWS CLI: `pip install awscli` and configure it.

# 2. Edit deployment template

* Copy `deploy_template.sh` to `deploy.sh`.
* Execute `chmod u+x deploy.sh` to set the execution permissions.
* Open `deploy.sh` in a text editor and make the following changes:
    - In `export SOURCE_CODE_BUCKET=BUCKETNAME` replace `BUCKETNAME` with the name of an S3 bucket that will be used for temporary storage of layers and Lambda's code.
    - In `export HUGO_LAYER_FILE_NAME=lambda-layer-hugo-0.54.zip` change the name of the zip file to whatever you named your `hugo` layer.
    - In `export LIBSTDC_LAYER_FILE_NAME=lambda-layer-libstdc.zip` change the name of the zip file to whatever you named your `libstdc++` layer.
    - In `export AWSCLI_LAYER_FILE_NAME=lambda-layer-awscli-1.16.115.zip` change the name of the zip file to whatever you named your `AWS CLI` layer.

# 3. Deploy

* Execute `./deploy.sh` from the command line.
* If the deployment is successful, you should see outputs in the JSON format.

# 4. Test

* Upload demo_site to the S3 bucket listed under `SourceS3Bucket` in outputs: `aws s3 sync demo_site s3://SOURCE_BUCKET_NAME`.
* Invoke API Gateway endpoint listed under `BuildApi` in outputs. It should look like `https://abcdefghij.execute-api.us-east-1.amazonaws.com/Prod/build/`. Copy the link and open it in a browser. It will take a few seconds to run due to a Lambda cold start. When the build completes, the page will show `Build complete`.
* Open the URL listed under `WebsiteS3BucketURL` in a browser. You should see a test site titled `My New Hugo Site`.
