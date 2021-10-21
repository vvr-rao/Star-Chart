import pandas as pd
import math 

#read the data from file
#source: https://www.astronexus.com/hyg OR https://github.com/astronexus/HYG-Database

df_stars = pd.read_csv('hygdata_v3.csv')
print(df_stars.head())

df_dsos = pd.read_csv('dso.csv')
print(df_dsos.head())

print(df_stars.shape)
print(df_dsos.shape)

df_stars_5 = df_stars.head()
df_dsos_5 = df_dsos.head()

#filter for Mag7 or lower stars and mag13 or lower DSOs

df_stars_mag7 = df_stars.loc[(df_stars.mag < 7)].reset_index()
print(len(df_stars_mag7))
print(df_stars_mag7.shape)


df_dsos_mag13 = df_dsos.loc[(df_dsos.mag < 13)]
print(len(df_dsos_mag13))
print(df_dsos_mag13.shape)

#combine Dataframes
#I will use most of the columns in the DSO sheet and will retain the Bayer / Flamsteed designation("bf","bayer","flam"), spectral class("spect")
#     , luminosity("lum"), color index("ci"), Gliese Catalog ID ("gl" - useful if looking for stars near the sun)
#     , Double star indicators ("comp", "comp_primary", "base", "id")
df_combined = df_dsos_mag13.reset_index()

#df_combined.reindex(columns=['bf','bayer','flam','spect','lum','ci'])

RowIds = []

for ind in df_combined.index:
    RowIds.append('DSO-'+str(ind))

df_combined.insert(0,'RowId',RowIds)
df_combined.insert(10,'bf','')
df_combined.insert(11,'bayer','')
df_combined.insert(12,'flam','')
df_combined.insert(13,'spect','')
df_combined.insert(14,'lum','')
df_combined.insert(15,'ci','')
df_combined.insert(16,'gl','')
df_combined.insert(17,'comp','')
df_combined.insert(18,'comp_primary','')
df_combined.insert(19,'base','')
df_combined.insert(18,'hyg_id','')

print(df_combined.shape)
print(df_combined.head())


for ind in df_stars_mag7.index:
    df_combined = df_combined.append({'ra':df_stars_mag7['ra'].iloc[ind],
                                      'dec':df_stars_mag7['dec'].iloc[ind],
                                      'type':'Star',
                                      'mag':df_stars_mag7['mag'].iloc[ind],
                                      'name':df_stars_mag7['proper'].iloc[ind],
                                      'const':df_stars_mag7['con'].iloc[ind],
                                      'bf':df_stars_mag7['bf'].iloc[ind],
                                      'bayer':df_stars_mag7['bayer'].iloc[ind],
                                      'flam':df_stars_mag7['flam'].iloc[ind],
                                      'spect':df_stars_mag7['spect'].iloc[ind],
                                      'lum':df_stars_mag7['lum'].iloc[ind],
                                      'ci':df_stars_mag7['ci'].iloc[ind],
                                      'gl':df_stars_mag7['gl'].iloc[ind],
                                      'comp':df_stars_mag7['comp'].iloc[ind],
                                      'comp_primary':df_stars_mag7['comp_primary'].iloc[ind],
                                      'gl':df_stars_mag7['gl'].iloc[ind],
                                      'hyg_id':df_stars_mag7['id'].iloc[ind],
                                      'RowId':'STAR-'+str(ind)},
                                      ignore_index = True)

print(df_combined.shape)
print(df_combined.head())

df_combined.to_csv('combined.csv', index=False)

#define a function to calculate the angular distance between objects using the ra and dec
# in the sheet - ra is in hours and dec is in degrees
# The formula used is :cos(A) = sin(d1)sin(d2) + cos(d1)cos(d2)cos(ra1-ra2)
def getAngDist(df_s, df_d):
    ra1 = df_s.ra
    ra2 = df_d.ra
    dec1 = df_s.dec
    dec2 = df_d.dec
    sin_dec1 = math.sin(math.radians(dec1))
    sin_dec2 = math.sin(math.radians(dec2))
    cos_dec1 = math.cos(math.radians(dec1))
    cos_dec2 = math.cos(math.radians(dec2))
    raDiff = math.radians((ra1 - ra2)*15)
    cos_ra = math.cos(raDiff)
    cosAng = sin_dec1*sin_dec2 + cos_dec1*cos_dec2*cos_ra
    return(math.acos(cosAng)/0.01745329252)



