import psycopg2
import boto3
from datetime import datetime

def execute_query(query):
    """
    Executes the provided SQL query on Amazon Redshift and returns the results.
    """
    connection_params = {
        'dbname': 'productiondwh',
        'user': 'readonly',
        'password': 'r3@d0Ly@0424',
        'host': 'productiondwh.c5iyekvfm1hi.us-east-1.redshift.amazonaws.com',
        'port': '5439'
    }
    
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return results
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error executing query: {error}")
        return None

def read_file_from_s3(uri):
    """
    Reads file content from Amazon S3 given a URI (s3://bucket_name/path/to/file).
    """
    try:
        s3 = boto3.client('s3')
        bucket_name, object_key = parse_s3_uri(uri)
        
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response['Body'].read().decode('utf-8')
        
        return file_content
    
    except Exception as e:
        print(f"Error reading file from S3: {e}")
        return None

def parse_s3_uri(uri):
    """
    Parses an S3 URI to extract bucket name and object key.
    """
    uri_parts = uri.split('/')
    bucket_name = uri_parts[2]
    object_key = '/'.join(uri_parts[3:])
    return bucket_name, object_key

def format_processed_date(processed_at):
    """
    Formats the processed date to YYYY-MM-DD format.
    """
    try:
        if isinstance(processed_at, str):
            processed_date = datetime.strptime(processed_at, "%Y-%m-%d %H:%M:%S.%f")
            formatted_processed_date = processed_date.strftime("%Y-%m-%d")
            return formatted_processed_date
        else:
            return processed_at.strftime("%Y-%m-%d")
    
    except Exception as e:
        print(f"Error formatting processed date: {e}")
        return None
