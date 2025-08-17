import boto3
import os
from botocore.exceptions import NoCredentialsError

def upload_to_s3(file_name, bucket, object_name=None):
   # If S3 object_name was not specified, use file_name
   if object_name is None:
       object_name = file_name

   # Create an S3 client
   s3_client = boto3.client('s3')

   try:
       # Upload the file
       response = s3_client.upload_file(file_name, bucket, object_name)
       print(f"File {file_name} uploaded to {bucket}/{object_name} successfully.")
   except FileNotFoundError:
       print(f"The file {file_name} was not found.")
   except NoCredentialsError:
       print("Credentials not available.")


def read_file_from_s3(bucket_name, object_name):
   """Read a file from an S3 bucket and return its contents.

   :param bucket_name: The name of the S3 bucket
   :param object_name: The name/key of the object in the S3 bucket
   :return: The contents of the file as a string
   """
   # Create an S3 client
   s3_client = boto3.client('s3')

   try:
       # Fetch the object from S3
       response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
       print(response)

       # Read the contents of the file
       file_content = response['Body'].read().decode('iso-8859-1')
       return file_content

   except NoCredentialsError:
       return "Error: AWS credentials not found."
   except PartialCredentialsError:
       return "Error: Incomplete AWS credentials provided."
   except s3_client.exceptions.NoSuchKey:
       return f"Error: The object {object_name} does not exist in the bucket {bucket_name}."
   except Exception as e:
       return f"Error: {e}"

# Example usage
#content = upload_to_s3('dldg_databricks.pdf', 'aws-sfl01-s3-us-east-1-data-1-mjr-bedrock-poc-5')
def delete_file(file_keys, bucket_name): 
   s3_client = boto3.client('s3') 
   file_keys = ['file1.txt', 'folder/file2.txt', 'folder/file3.txt']

   # Prepare objects for deletion
   objects_to_delete = [{'Key': key} for key in file_keys]

   # Delete the files
   response = s3_client.delete_objects(
      Bucket=bucket_name,
      Delete={'Objects': objects_to_delete}
   )

def upload_folder_to_s3(folder_path, bucket_name, s3_folder=""):
    """
    Uploads a folder and its contents to an S3 bucket.

    :param folder_path: Local folder path to upload.
    :param bucket_name: Name of the S3 bucket.
    :param s3_folder: Folder path in the S3 bucket (optional).
    """
    s3_client = boto3.client('s3')

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, folder_path)
            s3_file_path = os.path.join(s3_folder, relative_path).replace("\\", "/")  # Ensure S3 uses forward slashes
            
            try:
                s3_client.upload_file(local_file_path, bucket_name, s3_file_path)
                print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_file_path}")
            except Exception as e:
                print(f"Failed to upload {local_file_path}: {e}")

# Example usage
# upload_to_s3('dummy.pdf', 'aws-sfl01-s3-us-east-1-data-1-mjr-bedrock-poc-5')

file_keys = ['dldg_databricks.pdf']
# Prepare objects for deletion
delete_file(file_keys, 'aws-sfl01-s3-us-east-1-data-1-mjr-bedrock-poc-5')
# Example usage
folder_to_upload = "/home/ssm-user/devops_project/output_md"
bucket_name = 'aws-sfl01-s3-us-east-1-data-1-mjr-bedrock-poc-5'

upload_folder_to_s3(folder_to_upload, bucket_name)




