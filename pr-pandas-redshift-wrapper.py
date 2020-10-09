def pr_pd_to_rs(df_upload, redshift_table_name, 
    str_s3bucket, str_s3subdirectory, 
    flag_print, 
    str_dbname, str_host, str_port, str_user, str_pw, 
    str_accesskeyid, str_secretaccesskey
    ):
    '''
    Upload pandas dataframe to Redshift table.
    
    Redshift has 3 layers: database, schema, table.
        Our syntax combines schema and table into single str.  
            However, if the schema doesn't exist, create in SQL/Aginity:
                CREATE SCHEMA IF NOT EXISTS schema_name;
    
    Dependencies:
        import pandas_redshift as pr
    Input:
        df_upload - dataframe, pandas df to upload
        redshift_table_name - str, redshift table name of upload destination 
        str_s3bucket - str, S3 bucket name to store CSV files
        str_s3subdirectory - str, S3 folder to store CSV files
        flag_print - flag, True/False whether to download and print confirmation
        str_dbname - str, Redshift database 
        str_host - str, Redshift host address
        str_port - str, Redshift port number
        str_user - str, Redshift username credential
        str_pw - str, Redshift password credential
        str_accesskeyid - str, AWS IAM username access key
        str_secretaccesskey - str, AWS IAM username secret access key
    '''
    # create copy of dataframe to avoid changing original dataframe
    df_upload_copy = df_upload.copy()
    
    # Redshift cannot have column name 'Timestamp', so convert pandas column name if exists
    if 'timestamp' in [x.lower() for x in df_upload_copy.columns]:
        ls_new_cols = ['ts_rename_timestamp' if x.lower()=='timestamp' else x for x in df_upload_copy.columns]
        df_upload_copy.columns = ls_new_cols
    
    # create pandas-redshift connection
    pr.connect_to_redshift(dbname=str_dbname, host=str_host, port=str_port, user=str_user, password=str_pw)
    
    # Connect to S3
    pr.connect_to_s3(aws_access_key_id = str_accesskeyid,
                    aws_secret_access_key = str_secretaccesskey,
                    bucket = str_s3bucket,
                    subdirectory = str_s3subdirectory
                    # As of release 1.1.1 you are able to specify an aws_session_token (if necessary):
                    # aws_session_token = <aws_session_token>
                    )
    
    # Write the DataFrame to S3 and then to redshift
    pr.pandas_to_redshift(data_frame = df_upload_copy, 
                          redshift_table_name = redshift_table_name)
    
    if flag_print:
        print("Confirm upload by reading pandas dataframe from Redshift, only 100 rows: \n")
        
        # create pandas-redshift connection
        pr.connect_to_redshift(dbname=str_dbname, host=str_host, port=str_port, user=str_user, password=str_pw)
        
        # create dataframe from redshift query
        sql_query = f"SELECT * FROM {str_dbname}.{redshift_table_name} LIMIT 100"
        df_download = pr.redshift_to_pandas(sql_query)

        print("Columns of dataframe: ", df_download.columns, "\n")
        print("First 5 rows of dataframe: ", df_download.head(), "\n")
        
    pr.close_up_shop()
    
    
def pr_rs_to_pd(redshift_table_name, 
    str_dbname, str_host, str_port, str_user, str_pw
    ):
    '''
    
    Download Redshift table to pandas dataframe.
    
    Redshift has 3 layers: database, schema, table.
        Our syntax combines schema and table into single str.  
            However, if the schema doesn't exist, create in SQL/Aginity:
                CREATE SCHEMA IF NOT EXISTS schema_name;
    
    Dependencies:
        import pandas_redshift as pr
    Input:
        redshift_table_name - str, redshift table name of upload destination 
        str_dbname - str, Redshift database 
        str_host - str, Redshift host address
        str_port - str, Redshift port number
        str_user - str, Redshift username credential
        str_pw - str, Redshift password credential
    Return:
        df_download - pandas dataframe, downloaded from Redshift table
    '''

    # create pandas-redshift connection
    pr.connect_to_redshift(dbname=str_dbname, host=str_host, port=str_port, user=str_user, password=str_pw)

    # create dataframe from redshift query
    sql_query = f"SELECT * FROM {str_dbname}.{redshift_table_name}"
    df_download = pr.redshift_to_pandas(sql_query)

    print("Columns of dataframe: ", df_download.columns, "\n")
    print("First 5 rows of dataframe: ", df_download.head(), "\n")
        
    pr.close_up_shop()
    
    return df_download
