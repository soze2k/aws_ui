# import the necessary packages
import numpy as np
import sys
import time
import cv2
import os
import base64
import boto3
from botocore.exceptions import NoCredentialsError
import json
import mysql.connector


# construct the argument parse and parse the arguments
confthres = 0
nmsthres = 0

def lambda_handler(event, context):
    image = base64.b64decode(event["body"]["image"])
    # upload image to s3 bucket
    s3 = boto3.client("s3")
    upload_image_s3(image, s3, str(event["body"]["filename"]))
    # detection use yolo
    labelsPath = s3.get_object(
            Bucket = "yolo-bucket-ass2",
            Key = "coco.names"
        )
    configPath = s3.get_object(
            Bucket = "yolo-bucket-ass2",
            Key = "yolov3-tiny.cfg"
        )
    weightsPath = s3.get_object(
            Bucket = "yolo-bucket-ass2",
            Key = "yolov3-tiny.weights"
        )
    Lables=get_labels(labelsPath)
    CFG=get_config(configPath)
    Weights=get_weights(weightsPath)
    net=load_model(CFG,Weights)
    
    try:
        image = np.frombuffer(image,np.uint8)
        image = cv2.imdecode(image,cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        label_count = do_prediction(image, net, labels)
        response = findImageByTag(label_count)
        print(f"response = {response}")
        return response


    except Exception as e:

        print("Exception  {}".format(e))
        return{
            'statusCode': 500,
            'body': "Error, second internal server error"
            }

def upload_image_s3(image,s3,url):
    try:
        s3.put_object(
            Bucket = "image-upload-5225ass2",
            Key = url,
            Body = image,
            ContentType = "image/jpeg"
        )
        print(
            {
                'statusCode': 200,
                'body': "upload successfully"
            }
        )
    except NoCredentialsError:
        print(
            {
                'statusCode': 400,
                'body': "Error, check aws credentials"
            }
        )
    except Exception as e:
        print(e)
        print({
                'statusCode': 500,
                'body': "Error, internal server error"
            }
        )



def get_labels(labels_path):
    # load the COCO class labels our YOLO model was trained on
    LABELS = labels_path["Body"].read().decode("utf-8").strip().split("\n")
    print(LABELS)
    return LABELS


def get_weights(weights_path):
    # derive the paths to the YOLO weights and model configuration
    weightsPath = weights_path["Body"].read()
    return weightsPath

def get_config(config_path):
    configPath = config_path["Body"].read()
    return configPath

def load_model(configpath,weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net

def do_prediction(image,net,Lables,url):

    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    #print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])

                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # TODO Prepare the output as required to the assignment specification
    # ensure at least one detection exists

    
    if len(idxs) > 0:
        res_dic = []
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            res_dic.append(Lables[classIDs[i]])
        count_label = count_gen_label(res_dic)
        print(f"count label = {count_label}")
        #INSERT TO DATABASE
        response = insert_db(count_label,url)
        print(f"response = {response}")
        return response
        
def count_gen_label(res_dic):
    count_label = {}
    for label in res_dic:
        if label in list(count_label.keys()):
            count_label[label] += 1
        else:
            count_label[label] = 1

    return count_label
    

def insert_db(count_label,url):
    print("Mysql DB Connecting ..............")
    cnx = mysql.connector.connect(
        user = "admin",
        password = "12345678",
        host = "db-5225ass2.c250ugkumvye.ap-southeast-2.rds.amazonaws.com",
        database = "image_det"
    )
    print("Mysql DB Connected.")

    cursor = cnx.cursor()
    try:
        for label, count in count_label.items():
            query = "Insert into image_info (image_url, tag, count) VALUES (%s, %s, %s)"
            value = ("https://image-upload-5225ass2.s3.ap-southeast-2.amazonaws.com/" + url, label, count)
            print(f"query= {query}")
            cursor.execute(query, value)
        cnx.commit()
        print("Image " + url + " has insert to Mysql DB successfully")
        return {
                'statusCode': 200,
                'body': "upload successfully"
            }


    except Exception as e:
        print("Error: ", str(e))
        cnx.rollback()
        return {
            'statusCode': 500,
            'body': "Error, internal server error"
        }
    
    finally:
        cursor.close()
        cnx.close()

def findImageByTag(tag_list):
    image_url = []
    
    print("Mysql DB Connecting ..............")
    cnx = mysql.connector.connect(
        user = "admin",
        password = "12345678",
        host = "db-5225ass2.c250ugkumvye.ap-southeast-2.rds.amazonaws.com",
        database = "image_det"
    )
    print("Mysql DB Connected.")

    cursor = cnx.cursor()
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
    
    cursor.close()
    cnx.close()
    
    print(f"result={result}")
    result = {"links":[i[0] for i in result]}
    return result
    

