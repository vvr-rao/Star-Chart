# Star-Chart

Work in Progress code. Using this to analyze Astronomy data.
Data source is from the HYG Database and is available here: https://www.astronexus.com/hyg AND https://github.com/astronexus

The source dataset combines data from the Hipparcos Catalog, Yale Bright Star Catalog & Gliese Catalog. (I DO NOT own the dataset - refer links above for the original source) 

Planning to use the data to build and starhopping Website using AWS Athena and Neo4j. 
Starhopping, in amateur astonomy, is the process of finding objects in a telescope or binoculars by identtifying nearby stars.

## Methodology:

Below is the planned methodlogy.
1) Build and dataset of interesting Stars and DSOs.
2) Calculate angular distances between them (I am expecting this to be a compute intensive process and will use AWS EMR with Pyspark for the computation)
3) Load the dataset and distances into S3 as multiple .CSVs and use AWS Athena to query the data.
4) Build a front end using Lambda and expose publically


## Current State: 
I have been able to extract a subset of the data and create a queryable database using AWS Athena.

Explanation of files:

1) htgdata_v3.zip & dso.zip - source data files from the links above. Please refer to original links for data.
2) Extract_subset_and_combine.py - pulls out a subset of data. I am focussing on stars of Mag 7 or lower and DSO of mag 13 or lower. combinedV2.csv has the dataset
3) create_pairs.py - combine stars and dsos into pairs. The purpose of this step is to ease creation of a Pyspark dataframe. This would allow me to run computation of Angular Distances on a large dataset without crashing my machine
4) Calculate_Distances_using_Pyspark.ipynb - used this to do the compute using Pyspark. I spun up AWS EMR instances for the compute. (Calculate_Distances_using_Standard_Python.py - is an alternative without Pyspark but is a lot slower and not scalable)
