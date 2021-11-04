import json
import boto3
import time

# Can expose this VIA API Gateway as a GET call
# {
#     "Catalog": "$input.params('Catalog')",
#     "CatalogId": "$input.params('CatalogId')"
# }
# NOTE: Athena does not support Synchronous Queries. You submit a query to a queue and retrieve results later. 
# Here, I am querying, pausing for a few seconds and then retrieveing query results

def lambda_handler(event, context):
    #return("Got event\n" + json.dumps(event, indent=2))
    cat = event['Catalog']
    cat_id = event['CatalogId']
    #cat = "NGC"
    #cat_id = "2261"
    my_query = "SELECT a.AngularDist, d.hd, d.type, d.ApMagnitude, d.Constellation, d.name, \
        d.cat1, d.id1  FROM \"AwsDataCatalog\".\"starchart\".\"distances\" a, \"AwsDataCatalog\".\"db_name\".\"table_name\" s, \
        \"AwsDataCatalog\".\"db_name\".\"table_name\" d   \
        where s.cat1 = \'" + cat + "\' and s.id1 = " + cat_id + " and a.Source = s.RowId   \
        and a.Destination = d.RowId  \
        ORDER BY (a.AngularDist) \
        LIMIT 20"
        
    database_name = "<ATHENA_DATABASE>"
    catalog_name = "<ATHENA_CATALOG>"
    
    athena_client = boto3.client('athena')
    
    QueryResponse = athena_client.start_query_execution(
        QueryString = my_query,
        QueryExecutionContext={
            "Database": database_name,
            "Catalog": catalog_name
        },
        ResultConfiguration={
            'OutputLocation': 's3://<BUCKET>/<FOLDER>/'
            }
        
        
        )
        
    QueryId = QueryResponse["QueryExecutionId"]
    
    time.sleep(5)
    
    
    query_results = athena_client.get_query_results(
            QueryExecutionId=QueryId,
            MaxResults=12
        
        )
    
    out = "result: "
        
    #for row in query_results['ResultSet']['Row']:
     #   print(row)
     #   out = out + row
    #json_object =  json.loads(query_results) 
    
        
    return (query_results["ResultSet"])
