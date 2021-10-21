import pandas as pd
import boto3
from botocore.exceptions import ClientError
import os

#creating a new data frame with pairs of records. My idea is to calculate angular distance in the sky between each object
# However, file size can get pretty big. I have 19,249 records in the catalog (after filtering for Stars <Mag 7 and DSOs < Mag 13)
# this would translate to 370 million pairs!
# The idea is to feed this to Spark as a Spark Dataframe for processing and perform the processing in parallel
# 

df = pd.read_csv('combined.csv')

print(df.shape)
print(df.head())


id_list = df["RowId"].tolist()

# going to break into chunks. even with 1000 rows at a time I still get 19 million rows in each file
# 100 rows would net me 1.9 million rows in each file and 195 files

s3_client = boto3.client('s3')
bucket = "BUCKET_NAME"
filenum = 1

for ctr in range(0, 300, 100):
    s = ctr
    e = ctr + 100
    print("start: " + str(s) + "   End: " + str(e))
    df_combinations = pd.DataFrame(columns=['Source','Destination'])
    for ind in range(s,e):
        df_temp = pd.DataFrame({'Source':df["RowId"].iloc[ind], 'Destination':id_list})
        df_combinations = pd.concat([df_combinations, df_temp])
    filename = 'pairs' + str(filenum) + '.csv'
    filenum = filenum + 1
    df_combinations.to_csv(filename, index=False)
    response = s3_client.upload_file(filename, bucket, filename)
    os.remove(filename) 
    print("100 done!! Last Index: " + str(e))
        
 
#note: I ran this in AWS Cloud9 and struggled with memory usage. Can also copy to your S3 bucket using aws s3 cp Outputdirectory s3://BUCKET_NAME/FOLDER --recursive

