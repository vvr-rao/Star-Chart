import pandas as pd
import math

#read the combined data set of 19249 records
# Stars less than Mag 7 and DSOs less than Mag 13
# this will be my reference dataframe
df_ref = pd.read_csv('combined.csv')
print(df_ref.head())

print(df_ref.shape)


#read the paired data. This will go into the Pyspark Dataframe
# I will loop through this dataframe, read the ra and dec from the reference dataframe
df_pairs = pd.read_csv('pairs1.csv')
print(df_pairs.head())

print(df_pairs.shape)



# function to calculate the Angular distance
def getAngDist(df_s, df_d):
    ra1 = df_s.ra.iloc[0]
    #print('RA1: '+str(ra1))
    ra2 = df_d.ra.iloc[0]
    #print('RA2: '+str(ra2))
    dec1 = df_s.dec.iloc[0]
    #print('DEC1: '+str(dec1))
    dec2 = df_d.dec.iloc[0]
    #print('DEC2: '+str(dec2))
    sin_dec1 = math.sin(math.radians(dec1))
    #print('SINE DEC1: ' + str(sin_dec1))
    sin_dec2 = math.sin(math.radians(dec2))
    #print('SINE DEC2: ' + str(sin_dec2))
    cos_dec1 = math.cos(math.radians(dec1))
    #print('COSINE DEC1: ' + str(cos_dec1))
    cos_dec2 = math.cos(math.radians(dec2))
    #print('COSINE DEC2: ' + str(cos_dec2))
    raDiff = math.radians((ra1 - ra2)*15)
    cos_ra = math.cos(raDiff)
    #print('COSINE RA DIFF: '+ str(cos_ra))
    cosAng = sin_dec1*sin_dec2 + cos_dec1*cos_dec2*cos_ra
    #print('COSINE OF ANGULAR DIST: ' + str(cosAng))
    #Note: divide by 0.01745329252 below to convert radians to degrees
    return(math.acos(cosAng)/0.01745329252)



df_dist = pd.DataFrame(columns = ['Source', 'Destination', 'SourceRA', 'SourceDec', 'DestRA', 'DestDec', 'AngularDist'])



#for ind in df_pairs.index:
for ind in range(1,100000,1):
    df_source = df_ref.loc[df_ref['RowId'] == df_pairs['Source'].iloc[ind]]
    df_dest = df_ref.loc[df_ref['RowId'] == df_pairs['Destination'].iloc[ind]]
    #print(df_source.head())
    #print(df_dest.head())
    #print('ANGULAR DISTANCE: ' + str(getAngDist(df_source, df_dest)))
    #print(getAngDist(df_source, df_dest))
    #print(df_pairs['Source'].iloc[ind])
    #print(df_pairs['Destination'].iloc[ind])
    #print(df_source.ra.iloc[0])
    #print(df_source.dec.iloc[0])
    angDistDeg = getAngDist(df_source, df_dest)
    if (angDistDeg <5):
        df_dist = df_dist.append({'Source':df_pairs['Source'].iloc[ind],
                              'Destination':df_pairs['Destination'].iloc[ind],
                              'SourceRA':df_source.ra.iloc[0],
                              'SourceDec':df_source.dec.iloc[0],
                              'DestRA':df_dest.ra.iloc[0],
                              'DestDec':df_dest.dec.iloc[0],
                              'AngularDist':getAngDist(df_source, df_dest)},
                             ignore_index = True)
    
print(df_dist.head())
df_dist.to_csv('paired_distances.csv', index=False)



