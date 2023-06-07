import json
import os
import mysql.connector

# This is a method for query image by tag and count
def execute_query(cursor, tag_list):
    query = "SELECT image_url FROM image_det.image_info WHERE "
    for index, tag in enumerate(tag_list):
        label = tag.get("tag")  # Use get method to get tag and count
        count = tag.get("count", 1)  # if count is not exist, then make it to 1 by default
        if index == 0:
            query += f"(tag = '{label}' and count >= {count})"
        else:
            query += f" OR (tag = '{label}' and count >= {count})"
    
    # Combin same image and make sure it meet 2 condition
    query += f" GROUP BY image_url HAVING COUNT(DISTINCT tag) = {len(tag_list)};"
    
    # Close MySQL
    cursor.execute(query)
    result = cursor.fetchall()
    print(f"result={result}")
    result = {"links":[i[0] for i in result]}
    return result

def lambda_handler(event, context):
    
    # API Gateway Connected, then load json body
    body = json.loads(event["body"])
    tag_list = body["tags"]
    print(f"tag_list={tag_list}")
    
    # Connect MySQL database
    print("Mysql DB Connecting..............")
    cnx = mysql.connector.connect(
        user = "admin",
        password = "12345678",
        host = "db-5225ass2.c250ugkumvye.ap-southeast-2.rds.amazonaws.com",
        database = "image_det"
    )
    print("Mysql DB Connected.")
    cursor = cnx.cursor()
    
    try:
        result = execute_query(cursor, tag_list)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
                
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }
    finally:
        cursor.close()
        cnx.close()

