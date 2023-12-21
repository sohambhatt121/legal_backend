import os
import boto3

S3_BUCKET = os.getenv("S3_BUCKET_NAME")

class S3_Client:
    def init_client_obj(self):
        S3_ACCESS_KEY = os.getenv("S3_BUCKET_ACCESS_KEY")
        S3_SECRET_KEY = os.getenv("S3_BUCKET_SECRET_TOKEN")
        self.s3_client_obj = boto3.client(
            's3',
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY
        )

    def upload(self, file, folder_name, file_name):
        try:
            self.init_client_obj(self)
            self.s3_client_obj.upload_fileobj(file, S3_BUCKET, f"{folder_name}/{file_name}")
            #return f"https://{S3_BUCKET}.s3.amazonaws.com/{folder_name}/{file_name}"
        except Exception as e:
            raise Exception(str(e))
    
    def delete(self, file_name):
        try:
            self.init_client_obj(self)
            self.s3_client_obj.delete_object(Bucket = S3_BUCKET, Key = file_name)
        except Exception as e:
            raise Exception(str(e))