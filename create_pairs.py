import pandas as pd

#creating a new data frame with pairs of records. My idea is to calculate angular distance in the sky between each object
# However, file size can get pretty big. I have 19,249 records in the catalog (after filtering for Stars <Mag 7 and DSOs < Mag 13)
# this would translate to 370 million pairs!
# The idea is to feed this to Spark as a Spark Dataframe for processing and perform the processing in parallel
# 

df = pd.read_csv('combined.csv')

print(df.shape)
print(df.head())


id_list = df["RowId"].tolist()


df_combinations = pd.DataFrame(columns=['Source','Destination'])

for ind in range(5000):
    df_temp = pd.DataFrame({'Source':df["RowId"].iloc[ind], 'Destination':id_list})
    df_combinations = pd.concat([df_combinations, df_temp])

print(df_combinations.shape)
print(df_combinations.head())

df_combinations.to_csv('multiplied.csv', index=False)
