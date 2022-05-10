# Star-Chart


Purpose of this code is to build a starhopping app using the features of AWS. 
(Starhopping, in amateur astonomy, is the process of finding objects of interest in the sky using a telescope or binoculars by identifying nearby stars.)

My Data source is the HYG Database and is available here: https://www.astronexus.com/hyg AND https://github.com/astronexus
The source dataset combines data from the Hipparcos Catalog, Yale Bright Star Catalog & Gliese Catalog. (I DO NOT own the dataset - refer links above for the original source) 

Video Tutorial explaining what I did:      [![Video Tutorial](https://github.com/vvr-rao/Star-Chart/blob/main/images/youtube.jpg)](https://www.youtube.com/watch?v=R11cTC2mKOw&list=PLTPAjdTj-kaYB0GXZKk-j1mwSpZNKxN1d)

Screenshot of Front End...

![Screenshot](https://github.com/vvr-rao/Star-Chart/blob/main/images/screenshot.jpg?raw=true)

## Methodology:

Below is the planned methodlogy.
1) Build the dataset of interesting Stars and DSOs. 
2) Calculate angular distances between them (I expect this to be a compute intensive process and will use Pyspark on AWS EMR for the computation). Store the distances in a separate set of files.
3) Load the dataset and distances into S3 as multiple .CSVs and use AWS Athena to query the data. This is a pseudo Graph Database with the Stars & DSOs table as the NODES and the distances between them as the EDGES.
4) Build a front end using AWS Lambda and and a static website hosted on S3 and expose publically
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

## Potential Future Upgrades:
1) Modify the Spark jobs to use Transient Clusters. This would be useful in case I need to build out a pipeline to ingest data on a regular basis
2) Enhance the front and back ends. Potentially, could use Amplify to build out a React frontend while retaining a Lambda based REST API as the backend. Datastore can be moved to DynoamoDB for vastly improved performance. Advantage of Amplify if that it could be expanded into a mobile app.
3) Some sort of logic to traverse from a source to a destination node using the edges. This would give the 'star-hopping' functionality. Can optimize using an appropriate algorithm.

