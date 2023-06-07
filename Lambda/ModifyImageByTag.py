import json
import os
import mysql.connector

def lambda_handler(event, context):
    # Extract values from event
    img_url = event["url"]
    operation_type = event["type"]
    tags = event["tags"]

    # Establishing MySQL Connection
    print("MySQL Database connection.............")
    db_connection = mysql.connector.connect(
        user = "admin",
        password = "12345678",
        host = "db-5225ass2.c250ugkumvye.ap-southeast-2.rds.amazonaws.com",
        database = "image_det"
    )
    print("MySQL Database Connected.")
    db_cursor = db_connection.cursor()

    try:
        # Iterating through each tag in the event
        for tag in tags: 
            tag_label = tag.get("tag")  
            tag_count = tag.get("count", 1)

            # Constructing query to fetch existing record
            select_query = f"SELECT * FROM image_det.image_info WHERE image_url='{img_url}' and tag = '{tag_label}'"
            db_cursor.execute(select_query)
            existing_records = db_cursor.fetchall()
            print(f"Fetched existing records: {existing_records}")

            # If operation_type is 1, tags are to be added
            if operation_type == 1:
                print("Adding tags...")
                if existing_records:
                    # If record exists, update the count
                    if len(existing_records) != 1:
                        raise Exception("Error: Multiple records returned.")
                    existing_count = existing_records[0][3]
                    print(f"Updating existing tag count. Previous count: {existing_count}, New count: {existing_count + tag_count}")
                    update_query = f"UPDATE image_info SET count={existing_count + tag_count} WHERE image_url='{img_url}' and tag = '{tag_label}';"
                    db_cursor.execute(update_query)
                    db_connection.commit()
                else:
                    # If record does not exist, insert new record
                    print(f"Inserting new record. Tag: {tag_label}, Count: {tag_count}")
                    insert_query = "Insert into image_info (image_url, tag, count) VALUES (%s, %s, %s)"
                    insert_values = ("https://image-upload-5225ass2.s3.ap-southeast-2.amazonaws.com/" + img_url, tag_label, tag_count)
                    db_cursor.execute(insert_query, insert_values)
                    db_connection.commit()
            else:
                # If operation_type is 0, tags are to be removed
                print("Removing tags...")
                if existing_records:
                    # If record exists, update or delete based on the count
                    if len(existing_records) != 1:
                        raise Exception("Error: Multiple records returned.")
                    existing_count = existing_records[0][3]
                    if tag_count >= existing_count:
                        print(f"Deleting record. Tag: {tag_label}, Previous count: {existing_count}")
                        delete_query = f"DELETE FROM image_det.image_info WHERE image_url ='{img_url}' and tag = '{tag_label}';"
                        db_cursor.execute(delete_query)
                        db_connection.commit()
                    else:
                        print(f"Decreasing tag count. Previous count: {existing_count}, New count: {existing_count - tag_count}")
                        update_query = f"UPDATE image_info SET count={existing_count - tag_count} WHERE image_url='{img_url}' and tag='{tag_label}';"
                        db_cursor.execute(update_query)
                        db_connection.commit()
        return {
            'statusCode': 200,
            'body': json.dumps(existing_records)
        }   
    except Exception as err:
        print(f"An error occurred: {err}")
        return {
            'statusCode': 500,
            'body': str(err)
        }
    finally:
        # Closing cursor and connection
        db_cursor.close()
        db_connection.close()

