# Star-Chart


Purpose of this code is to build a starhopping app using AWS Athena and/or Neo4j. 
(Starhopping, in amateur astonomy, is the process of finding objects of interest in the sky using a telescope or binoculars by identifying nearby stars.)

My Data source is the HYG Database and is available here: https://www.astronexus.com/hyg AND https://github.com/astronexus
The source dataset combines data from the Hipparcos Catalog, Yale Bright Star Catalog & Gliese Catalog. (I DO NOT own the dataset - refer links above for the original source) 



Screenshot of Front End...

![Screenshot](https://github.com/vvr-rao/Star-Chart/blob/main/images/screenshot.jpg?raw=true)

## Methodology:

Below is the planned methodlogy.
1) Build the dataset of interesting Stars and DSOs. 
2) Calculate angular distances between them (I expect this to be a compute intensive process and will use Pyspark on AWS EMR for the computation)
3) Load the dataset and distances into S3 as multiple .CSVs and use AWS Athena to query the data.
4) Build a front end using AWS Lambda and expose publically
5) Optionally also load the data into Neo4j. This optimizes querying based on relationships. 


## Current State: 
I have been able to create a queryable database using AWS Athena, am able to query it using Lambda and provide external access via the API Gateway and a static webpage (hosted on S3). Cleaning up and adding bells and whistles

## Explanation of files:

1) htgdata_v3.zip & dso.zip - source data files from the links above. Please refer to original links for data.
2) Extract_subset_and_combine.py - pulls out a subset of data. I am focussing on stars of Mag 7 or lower and DSO of mag 13 or lower. combinedV2.csv has the dataset
3) create_pairs.py - combine stars and dsos into pairs. The purpose of this step is to ease creation of a Pyspark dataframe. This would allow me to run computation of Angular Distances on a large dataset without crashing my machine
4) Calculate_Distances_using_Pyspark.ipynb - used this to do the compute using Pyspark. I spun up AWS EMR instances for the compute. (Calculate_Distances_using_Standard_Python.py - is an alternative without Pyspark but is a lot slower and not scalable)
5) Lambda-to-search-Athena-based-on-Catalog-Id.py - Lambda function to accept Catalog Name and Id, query Athena and return the closest Stars and DSOs
6) index.html - static webpage for the query. Working to clean it up and add bells and whistles
