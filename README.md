
# Spoton Data Engineering Assignment


### Quick table of contents
- [Dan's Work](#dans-work)
- [Original Assignment](#assignment-test)

# Dan's Work

Forked repo for the SpotOn data engineering assessment. Originally found [HERE](https://github.com/SpotOnInc/data_engineering_assignment)\
The bulk of this work is done in a python script, with some setup before.

### Setup 
Before triggering the .py script, we need to store credentials for s3 and kaggle, along with setting up a Postgres db instance.

 1. Credentials should be stored in `~/.aws/config` for Amazon and `~/.kaggle/kaggle.json` for Kaggle
 2. cd into this directory
 3. run `docker-compose up -d` to launch a postgres instance in the background with pre-built tables
 4. create a virtual environment with `python3 -m venv spoton_env; source spoton_env/bin/activate`
 5. install packages with `pip3 install -r requirements.txt`
 6. run the script with `python3 kaggle_to_s3_to_pg.py` which will complete the following tasks:
    * download and unzip the [Brazilian ecommerce data set](https://www.kaggle.com/olistbr/brazilian-ecommerce) and put into `./brazilian-ecommerce`
    * upload the four required datasets to Amazon s3 storage
    * pull from the s3 object store and upload to postgres
 7. run `docker-compose down -v` to remove the container and volumes


# Assignment Test
Your task is to automate the download and ingestion of the [Brazilian ecommerce data set](https://www.kaggle.com/olistbr/brazilian-ecommerce) using the Kaggle API. 

1) Fork this repo to your account
2) Create an account with Kaggle if you don't already have one.  You will need this to access their API to retreive data for the assigment.
3) Create a script to retrieve Brazilian eCommerce data from the Kaggle API and place the files listed below in object storage.
  - Minio is provided in docker compose or feel free to use your choice of object storage (e.g. Google Cloud Storage, AWS S3)
  - **Load only the following datasets:**
  
    ```
    olist_customers_dataset.csv
    olist_order_items_dataset.csv
    olist_orders_dataset.csv
    olist_products_dataset.csv
    ```
4) Ingest files from object storage into Postgres using Singer, python or your programming language of choice.  Provided is a base python image in the `Dockerfile` along with a Postgres instance that can be created using docker compose.  Your ingestion process should create a table for each file.  Here are some helpful links if you are using singer (hint, we link singer ;), but use whatever you are most comfortable with)
    - CSV Singer tap: https://github.com/singer-io/tap-s3-csv
    - Postgres Singer target: https://github.com/datamill-co/target-postgres

5) Create a `nexsteps.md` in the repo and cover deployment considerations along with thoughts on further optimization for scale.


## Acceptance Criteria


- [x] We will pulling from the master/main branch of your provided repo link
- [ ] We should be able to run your code by running the following command `docker-compose up`.
- [x] We should be able to access the generated tables in the Postgres DB at `localhost:5432`.
- [x] **Note, feel free to use patterns that you might otherwise avoid if they save a significant amount of time.  However, be sure to call these out in your `nextsteps.md` and be prepared to discuss how you might implement given additional time.**