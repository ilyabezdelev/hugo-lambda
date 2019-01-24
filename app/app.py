import subprocess
import os
import logging

# TODO:
# * Test with and without trailing slashes
# * Provide examples of input parameters
# * Talk to arnab and ask how to package with all the dependencies
# * README
# * SAM template with deps

# Environment variables
LOCAL_SOURCE_DIR = '/tmp/hugo_source'
LOCAL_BUILD_DIR = '/tmp/hugo_build'
SOURCE_S3_BUCKET_PATH = os.environ['SOURCE_PATH']
DESTINATION_BUCKET = os.environ['DESTINATION_BUCKET']

# Setting up a logger with a more readable format
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s',level=logging.DEBUG)

# Runs a shell command. Throws an exception if fails.
def run_command(command):
    command_list = command.split(' ')
    try:
        logger.info("Running shell command: \"{0}\"".format(command))
        result = subprocess.run(command_list, stdout=subprocess.PIPE);
        logger.info("Command output:\n---\n{0}\n---".format(result.stdout.decode('UTF-8')))
    except Exception as e:
        logger.error("Exception: {0}".format(e))
        raise e
    return True

# Downloads source of the Hugo website from S3
def download_from_s3(s3_path,local_path):
    logger.info('Downloading source code from S3: {0}'.format(s3_path))
    run_command('/opt/aws s3 ls {0}'.format(s3_path))
    run_command('/opt/aws s3 sync s3://{0} {1}'.format(s3_path,local_path))
    run_command('ls -l {}'.format(local_path))

# Builds a hugo website
def build_hugo(source_dir, destination_dir,debug=False):
    logger.info("Building Hugo site")
    run_command("/opt/hugo -s {0} -d {1}".format(source_dir,destination_dir))
    run_command("ls -l {0}".format(destination_dir))

# Uploads the built website to S3
def upload_to_s3(local_path,s3_path):
    logger.info('Uploading Hugo site to S3: {0}'.format(s3_path))
    run_command('/opt/aws s3 rm s3://{0} --recursive'.format(s3_path))
    run_command('/opt/aws s3 sync {0} s3://{1}'.format(local_path,s3_path))
    run_command('/opt/aws s3 ls {0}'.format(s3_path))

def lambda_handler(event, context):
    download_from_s3(SOURCE_S3_BUCKET_PATH,LOCAL_SOURCE_DIR)
    build_hugo(LOCAL_SOURCE_DIR,LOCAL_BUILD_DIR)
    upload_to_s3(LOCAL_BUILD_DIR,DESTINATION_BUCKET)

    return {"statusCode": 200, \
        "headers": {"Content-Type": "text/html"}, \
        "body": "Build complete"}