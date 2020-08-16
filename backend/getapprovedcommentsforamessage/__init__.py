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
    
    if db:


        request_json = req.get_json()
        col = db.comments
        results = []
        maxid = 0
        mid = request_json["message_id"]
        
        for x in col.find():
            if x["mid"] != mid:
                continue
            if x["status"] != "approved":
                continue
            
            item = {}


            item["mid"] = str(x['mid'])
            item["comment"] =  str(x["comment"])
            # item["description"] =  x["description"]
            # item["phone"] =  x["phone"]
            # item["email"] =  x["email"]
            item["status"] =  x["status"]
            
            results.append(item)
            maxid +=1
        
        
        retjson = {}

        retjson['comments'] = results
        retjson['mongoresult'] = str(maxid)

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


