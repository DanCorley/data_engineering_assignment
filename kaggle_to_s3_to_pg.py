import kaggle
import os
import boto3
import json
import time
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine


def kaggle_download(local_dir: str, force=False, quiet=False, unzip=True):

    kaggle.api.dataset_download_files(
        dataset='olistbr/brazilian-ecommerce',
        path='./brazilian-ecommerce/',
        force=force,
        quiet=quiet,
        unzip=unzip
    )


def _s3_client():
    return boto3.client(
        service_name='s3',
        region_name='us-east-1'
    )


def s3_batch_upload(bucket: str, files: list):
    
    s3 = _s3_client()
    
    # create if not exists
    bucket_info = s3.create_bucket(Bucket=bucket)
    
    # placeholder for share_urls
    s3_url_info = {}

    for file in files:

        s3.upload_file(
            Bucket=bucket,
            Filename=os.path.join(local_dir, file),
            Key=file,
            ExtraArgs={
                'ContentType': 'text/csv',
                'ACL': 'authenticated-read'
            }
        )

        s3_url_info[file] = {
            's3_link':
                s3.generate_presigned_url(
                ClientMethod='get_object',
                ExpiresIn=7200,
                Params={'Bucket':bucket, 'Key':file}
                ),
            'expiresIn': 7200,
            'created_at': pd.Timestamp.utcnow().isoformat()
        }
        
    return s3_url_info


def s3_to_dataframe(key: str, s3, bucket):
    
    file = s3.get_object(Bucket=bucket, Key=key)
    
    data_gen = file['Body'].read()
    
    return pd.read_csv(StringIO(data_gen.decode('utf-8')))


def create_postgres_tables(conn_str):

    db = create_engine(conn_str)

    with db.connect() as conn:

        with open('./db_create_tables.txt') as f:
            create_query = f.read()

        conn.execute(create_query)


def upload_to_db(files: list, conn_str: str):
    
    s3 = _s3_client()
    
    db = create_engine(conn_str)
    
    with db.connect() as conn:
        
        for file in files:
            
            then = time.perf_counter()
            
            base_name = file.split('.')[0]
            
            print(f'Starting file {base_name}', end='')
            
            df = s3_to_dataframe(file, s3, s3_bucket)

            df.to_sql(base_name, conn, index=False, if_exists='append')
            
            now = round(time.perf_counter() - then, 3)
            
            print(f' - Upload took {now} seconds.')

        

if __name__ == '__main__':
    
    local_dir = './brazilian-ecommerce'
    s3_bucket = 'data-engineering-assignment'
    conn_str = 'postgresql://postgres:postgres@localhost:5432/postgres'

    files_to_upload = [
        'olist_customers_dataset.csv',
        'olist_orders_dataset.csv',
        'olist_products_dataset.csv',
        'olist_order_items_dataset.csv'
    ]

    kaggle_download(local_dir)
    
    csv_s3_file_info = s3_batch_upload(s3_bucket, files_to_upload)
    
    with open('csv_s3_file_info.json', 'w') as f:
        json.dump(csv_s3_file_info, f)
    
    create_postgres_tables(conn_str)
    
    upload_to_db(files_to_upload,conn_str)
