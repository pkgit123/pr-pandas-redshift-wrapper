# pr-pandas-redshift-wrapper
Playbook to upload pandas dataframe to redshift table

Final output of data analysis projects often involves a dashboard visualization in PowerBI or Tableau, with the data stored in an AWS Redshift datawarehouse table.  

Uploading to Redshift is a clunky multi-step process: 
1. the data converted to CSV files
1. the CSV files uploaded to an AWS S3 bucket
1. execute SQL commands to upload CSV files in S3 bucket to Redshift

Use pandas_redshift library (https://github.com/agawronski/pandas_redshift), which is a wrapper on `psycopg2` library.  However because the pandas_redshift library requires credentials (Redshift and IAM user), wrote some wrapper code for ease of code-reuse.

pip install and import: 
`pip install pandas_redshift`
`import pandas_redshift as pr`

Two specific implementation details of Redshift:
1. pandas_redshift library assumes the schema has been created
    * Redshift has 3 layers: database, schema, table.
      - Our syntax combines schema and table into single str.  
      - However, if the schema doesn't exist, create in SQL/Aginity:
      ```SQL
      CREATE SCHEMA IF NOT EXISTS schema_name;
      ```
1. redshift columns cannot be named `Timestamp`, otherwise throws error
    * So the code renames any pandas dataframe column `Timestamp` before upload

Reference: 
* https://github.com/agawronski/pandas_redshift
* https://pypi.org/project/pandas-redshift/
* https://blog.jetbrains.com/pycharm/2017/08/analyzing-data-in-amazon-redshift-with-pandas/
