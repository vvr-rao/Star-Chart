import boto3
import pandas as pd
import math
import os

# Creating the low level functional client
s3client = boto3.client('s3')
BUCKET = "BUCKET"
FOLDERNAME  = 'FOLDER'


paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket=BUCKET, Prefix=FOLDERNAME)

for page in pages:
    #print(page['Contents'])
    for obj in page['Contents']:
        print(obj['Key'])

#KEY = 'pairsv3/pairsv2-last.csv'
KEY = 'pairsv3/pairsv2-9.csv'
response = s3client.get_object(
                    Bucket = BUCKET,
                    Key = KEY
                )
                
status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

print(status)

df_pairs = pd.read_csv(response.get("Body"))
print(df_pairs.head())


print(math.radians(0))

# function to calculate the Angular distance
def getAngDist(SourceRA, SourceDec, DestRA, DestDec):
    ra1 = SourceRA
    ra2 = DestRA
    dec1 = SourceDec
    dec2 = DestDec
    print("ra1: " + str(ra1) + " ra2: " + str(ra2) + " dec1: " + str(dec1) + " dec2: " + str(dec2)) 
    sin_dec1 = math.sin(math.radians(dec1))
    sin_dec2 = math.sin(math.radians(dec2))
    cos_dec1 = math.cos(math.radians(dec1))
    cos_dec2 = math.cos(math.radians(dec2))
    radiff1 = (ra1 - ra2)*15
    raDiff = math.radians(radiff1)
    print("raDiff: " + str(raDiff))
    cos_ra = math.cos(raDiff)
    print("cos_ra: " + str(cos_ra))
    cosAng = sin_dec1*sin_dec2 + cos_dec1*cos_dec2*cos_ra
    print("cosAng: " + str(cosAng))
    #Note: divide by 0.01745329252 below to convert radians to degrees
    # Note2: for some reason, math.acos(0) gives a math domain error.
    # In pyspark this causes the job to crash with a confusing "unable to overwrite file" error
    if ((ra1 == ra2) & (dec1 == dec2)):
        ret = 0
    else:
        ret = math.acos(cosAng)
    print("ret: " + str(ret))
    return(ret/0.01745329252)
    
df_dist = pd.DataFrame(columns = ['Source', 'Destination', 'SourceRA', 'SourceDec', 'DestRA', 'DestDec', 'AngularDist'])


#for ind in range(1,50,1):
for ind in df_pairs.index:
    SourceRA = df_pairs['SourceRA'].iloc[ind]
    SourceDec = df_pairs['SourceDec'].iloc[ind]
    DestRA = df_pairs['DestRA'].iloc[ind]
    DestDec = df_pairs['DestDec'].iloc[ind]
    angDistDeg = getAngDist(SourceRA, SourceDec, DestRA, DestDec)
    df_dist = df_dist.append({'Source':df_pairs['Source'].iloc[ind],
                        'Destination':df_pairs['Destination'].iloc[ind],
                        'SourceRA':SourceRA,
                        'SourceDec':SourceDec,
                        'DestRA':DestRA,
                        'DestDec':DestDec,
                        'AngularDist':angDistDeg},
                       ignore_index = True)

print(df_dist.head())
out_filename = 'out4.csv'
df_dist.to_csv(out_filename, index=False)

response = s3client.upload_file(out_filename, BUCKET, 'distances/'+out_filename)
os.remove(out_filename)
