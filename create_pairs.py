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


# going to break into chunks. even with 1000 rows at a time I still get 19 million rows in each file 
# if I try to calculate distances between ALL objects
# Even 100 rows would net me 1.9 million rows in each file and 193 files

# Eventually, I decided that I only wanted to calculate distances where the objects (stars and DSOs) would be within 7 degrees of each other
# this would be fairly useful. As a reference -  Even with binoculars you would not get a FOV greater than 7 degrees. 
# an 80mm f/5 telescope with 1.25 inch eyepieces would have a max FOV of 4 degrees.
# My 10 inch F4.7 Dobsonian has a max FOV or 2.2 degrees with my widest eyepiece.

# a quick and dirty way to limit the size of the dataset would be to put filters on RA and DEC
# based on the 7 degree max angular distance -  the hour difference (RA) was + or - 0.5 hours and 7 degrees for the Dec difference

#note: I ran this in AWS Cloud9 and struggled with memory usage. Hence, uploading files to S3 as they are created
#Can also copy to your S3 bucket using the CLI - aws s3 cp Outputdirectory s3://BUCKET_NAME/FOLDER --recursive

s3_client = boto3.client('s3')
bucket = "emr-astronomy-petproj"
filenum = 1


for ctr in range(0, 18000, 1000):
    s = ctr
    e = ctr + 1000
    print("start: " + str(s) + "   End: " + str(e))
    df_combinations = pd.DataFrame(columns=['Source','Destination','SourceRA','SourceDec','DestRA','DestDec'])
    for ind in range(s,e):
        #df_temp = pd.DataFrame({'Source':df["RowId"].iloc[ind], 'Destination':id_list})
        SourceId = df["RowId"].iloc[ind]
        SourceRA = df["ra"].iloc[ind]
        SourceDec = df["dec"].iloc[ind]
        
        RAlower = SourceRA-0.5
        RAupper = SourceRA+0.5
        
        Declower = SourceDec - 7
        Decupper = SourceDec + 7
        
        #print("Source RA: " + str(SourceRA ) + "RA Range: " + str(RAlower) + " - " + str(RAupper) )
        #print("SourceDec: " + str(SourceDec) + "Dec Range: " + str(Declower) + " - " + str(Decupper) )
        
        df_subset = df.loc[ (df['ra'] >= RAlower)  &  (df['ra'] <= RAupper) & (df['dec'] >= Declower) & (df['dec'] <= Decupper) ]
        
        #print("Subset size: " + str(df_subset.size))
        
        id_list = df_subset["RowId"].tolist()
        ra_list = df_subset["ra"].tolist()
        dec_list = df_subset["dec"].tolist()
        
        
        df_temp = pd.DataFrame({'Source':df["RowId"].iloc[ind],
                                'Destination':id_list,
                                'SourceRA':df["ra"].iloc[ind],
                                'SourceDec':df["dec"].iloc[ind],
                                'DestRA':ra_list,
                                'DestDec':dec_list})
        df_combinations = pd.concat([df_combinations, df_temp])
    filename = 'pairsv2-' + str(filenum) + '.csv'
    filenum = filenum + 1
    df_combinations.to_csv(filename, index=False)
    #s3_client = boto3.client('s3')
    response = s3_client.upload_file(filename, bucket, filename)
    os.remove(filename) 
    print("1000 done!! Last Index: " + str(e) + " Filenum: " + str(filenum))
  
df_combinations = pd.DataFrame(columns=['Source','Destination','SourceRA','SourceDec','DestRA','DestDec'])
s = 19000
e = 19249
for ind in range(s,e):
    SourceId = df["RowId"].iloc[ind]
    SourceRA = df["ra"].iloc[ind]
    SourceDec = df["dec"].iloc[ind]
    
    RAlower = SourceRA-0.5
    RAupper = SourceRA+0.5
    
    Declower = SourceDec - 7
    Decupper = SourceDec + 7
    
    #print("Source RA: " + str(SourceRA ) + "RA Range: " + str(RAlower) + " - " + str(RAupper) )
    #print("SourceDec: " + str(SourceDec) + "Dec Range: " + str(Declower) + " - " + str(Decupper) )
    
    df_subset = df.loc[ (df['ra'] >= RAlower)  &  (df['ra'] <= RAupper) & (df['dec'] >= Declower) & (df['dec'] <= Decupper) ]
    
    #print("Subset size: " + str(df_subset.size))
    
    id_list = df_subset["RowId"].tolist()
    ra_list = df_subset["ra"].tolist()
    dec_list = df_subset["dec"].tolist()
    
    df_temp = pd.DataFrame({'Source':df["RowId"].iloc[ind],
                                'Destination':id_list,
                                'SourceRA':df["ra"].iloc[ind],
                                'SourceDec':df["dec"].iloc[ind],
                                'DestRA':ra_list,
                                'DestDec':dec_list})
    df_combinations = pd.concat([df_combinations, df_temp])



filename = 'pairsv2-last.csv'
df_combinations.to_csv(filename, index=False)
s3_client = boto3.client('s3')
response = s3_client.upload_file(filename, bucket, filename)
os.remove(filename)
print("AllDone!! Last Index: " + str(e))
