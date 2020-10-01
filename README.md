# pr-pandas-redshift-wrapper
Playbook to upload pandas dataframe to redshift table

Final output of data analysis projects often involves a dashboard visualization in PowerBI or Tableau, with the data stored in an AWS Redshift datawarehouse table.  Uploading to Redshift is a clunky multi-step process: (1) the data converted to CSV files, (2) the CSV files uploaded to an AWS S3 bucket, (3) SQL commands to upload CSV files in S3 bucket to Redshift.  
