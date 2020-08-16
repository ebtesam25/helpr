import logging

import azure.functions as func
from pymongo import MongoClient
from pymongo.collection import ObjectId
import bcrypt
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def initdb():

    client = MongoClient("mongodb+srv://user:password3142@cluster0.dyrpk.azure.mongodb.net/<dbname>?retryWrites=true&w=majority")

    db = client.get_database("helpr")

    return client, db



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    
    client, db = initdb()
    
    if req.get_json():


        request_json = req.get_json()
        col = db.helprequests
        results = []
        maxid = 0
        # for x in col.find():
        #     id = int(x["id"])
        #     maxid +=1
        # id = str(maxid+id)

        results = []
        if request_json and 'id' in request_json:
            id = request_json['id']
            col.update_one({"id":str(id)}, {"$set":{"description":"thanks to a generous benefactor, this request has been fulfilled"}})
            col.update_one({"id":str(id)}, {"$set":{"status":"fulfilled"}})
            # if 'emoji' in request_json:
            #     col.update_one({"id":str(id)}, {"$set":{"emoji":str(request_json['emoji'])}})
            # if 'img_url' in request_json:
            #     col.update_one({"id":str(id)}, {"$set":{"img_url":str(request_json['img_url'])}})
            # if 'looking_for' in request_json:
            #     col.update_one({"userid":str(userid)}, {"$set":{"looking_for":str(request_json['looking_for'])}})
            # if 'orientation' in request_json:
            #     col.update_one({"userid":str(userid)}, {"$set":{"orientation":str(request_json['orientation'])}})
            # if 'bio' in request_json:
            #     col.update_one({"userid":str(userid)}, {"$set":{"bio":str(request_json['bio'])}})
            # if 'age' in request_json:
            #     col.update_one({"userid":str(userid)}, {"$set":{"age":str(request_json['age'])}})
            # if 'address' in request_json:
            #     col.update_one({"userid":str(userid)}, {"$set":{"address":str(request_json['address'])}})
            # if 'hobbies' in request_json:
            #     col.update_one({"userid":str(userid)}, {"$set":{"hobbies":str(request_json['hobbies'])}})
            # if 'imageUrl' in request_json:
            #     col.update_one({"userid":str(userid)}, {"$set":{"imageUrl":str(request_json['imageUrl'])}})
            # if 'audioUrl' in request_json:
            #     col.update_one({"userid":str(userid)}, {"$set":{"audioUrl":str(request_json['audioUrl'])}})

            retjson = {}

            retjson['id'] = id
            retjson['mongoresult'] = "successfully modified"

            # return json.dumps(retjson)

            ret = json.dumps(retjson)

            return  func.HttpResponse(
                ret,
                mimetype="application/json",
                status_code=200
            )


    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )


