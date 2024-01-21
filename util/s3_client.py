import os
import boto3

S3_BUCKET = os.getenv("S3_BUCKET_NAME")

class S3_Client:
    def init_client_obj(self):
        S3_ACCESS_KEY = os.getenv("S3_BUCKET_ACCESS_KEY")
        S3_SECRET_KEY = os.getenv("S3_BUCKET_SECRET_TOKEN")
        S3_REGION = os.getenv("S3_BUCKET_REGION")
        self.s3_client_obj = boto3.client(
            's3',
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
            region_name=S3_REGION
        )

    def upload(self, file, folder_name, file_name, content_type):
        try:
            self.init_client_obj(self)
            #print(content_type)
            self.s3_client_obj.put_object(
                Body=file,
                Bucket=S3_BUCKET,
                Key=f"{folder_name}/{file_name}",
                ContentDisposition='inline',
                ContentType=content_type,
                ACL='public-read'
            )
            
            # Refer this url for all args: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_object.html#

        except Exception as e:
            raise Exception(str(e))
    
    def delete(self, file_name):
        try:
            self.init_client_obj(self)
            self.s3_client_obj.delete_object(Bucket = S3_BUCKET, Key = file_name)
        except Exception as e:
            raise Exception(str(e))
        
    def get_access(self, file_name, expiry):
        try:
            url = "https://"+S3_BUCKET+".s3.amazonaws.com/"+file_name
            return url
            
            """
            self.init_client_obj(self)
            response = self.s3_client_obj.getSignedUrlPromise(
                'get_object',
                Params={
                    'Bucket': S3_BUCKET,
                    'Key': file_name,
                    'ResponseContentDisposition': 'inline'
                }
            )
            return response
            """
        except Exception as e:
            return str(e)
