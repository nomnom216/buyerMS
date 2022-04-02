from flask import Flask, request, jsonify, render_template

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "esdbuyerms",
        "private_key_id": "84364940cca3bd0ae01cb42380217eec462fbed3",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCMKZWz1PNDFB8h\nwDa+3ZPOL6HEfHw3EyG3sS2UbM24qa0I2UqRYtgbr16OjAhcx8607mHIeOaiCRly\nm/xvBf6fd6hX0XEL6JHDzsiaxLDRx7FZxpleRmOgDp9AZ+7jcjwCnC4lPtmuafuc\nIbKRqVfce+35CJ+HK8U8U6aBO3X2Vj6YcgNmAeSRk0EH0qWbnjM6tQxJFq+WsT3N\n0U62y5pKhAyyaCdTwpwg2upZfCypTr2/afnQfYJlICSjrYUf9DB39YCnm0zUo14B\n24M0GzKuL69abPfvsngtiixB0OfZ7q1zFbc9Q3giVUJymasFTPIR4DxzqoFF66s9\npJ4Ieu13AgMBAAECggEAFqwPXCSBKQOTOZlnAZ7D7uFDkI32Zc5BcP5G+jBTYqCH\nrdvANR5BCNFoQTSjkaZ8aEX7KTttSx6fsCtNPQRCOLdZUsM9Pwjis0K6rlZMp9Je\nfMAkRNyr9tMGrZtiSAZNcLqkuD+fZJgeLBZDVU6IONEPIG5lp67L28NINrVQkoUJ\nl+eeAjbFjxP4k+FgHSz3ErZK9nujE0g0j4AJfCR21B2RBNFwYazpW80jvahkxV2J\nIPPLrKfVi+4uaP/UXiABvYtk3r4MgWe+AlKsOHhlKG9hXfGr9DJwkWckY3EyqHFj\nyuvBDcnuid0vUy6LdYRT90tbFjKM4QSAwKjx/G5dgQKBgQC/iN8uhvixwyfbB6Q9\nkPyB/XNqnTWOikiWHBzfk7AadjYIhcfF9SSlDzuCER5uJRfzmzIQxVxSBQ8kykZv\n8X6GtRK9Xrg+EDg13o/VgpbtLMzxXpmQYvhkbbb32Lz2b4jLXplzaZzH+LlgGF4S\nyudaLhfoaJ6PjZGSDMOvBTzeQQKBgQC7VlkkeCTOTZ80pPkP6OTeMA/3L+8ZAkij\nQgbm9V7+3Ien6slCXCWVTD5da7FDmwbwbfIzv6DuNq6iOHIuqM/WZhp2uus88+ON\nUbePxQ/upZJR3L7bP8ebJ5lNH+SugiKNC4mF7sU6cVZOrK3yfoytqCbWQ3d59AOa\nepygKH7NtwKBgEZN/14cvPzDHcYQMAFJTuaIGe1wd1AzAiHXf+GxXFraOUs3j/Th\n3umXhchgcEMN6pTIyr/NMe4JXV2rwd8lTcQ0gwRv2EEvwvJDF5jProawgym2B7gw\nG+0BOMARFot+tT+xIbJzedENQz46s41CXVmEwdHVVR5sYJqzhMChs44BAoGBAIeC\niGzW81i/0T/VbcvSXWtTPNlDNSLUAhMF+dQq/ZJBl2chcH+uBAmg4yPUeJ88jqJw\nBVjlbtWhfGUfi4iw19ZweQgVYX/vs1RQHgXDOCkaX2MT2ILj+dEDreKaBWMuAywf\nglT9SHFj9lhmlFTqsXwUPDOVDeGLXufpdU5svHy1AoGAIRtATYD36+itUUFWZELM\nK3K9Mnw1hUoWL3sGyUUsi7OCKCqmH4f1k49XhRbz2CRuY+TvMzIszl5c5m9j6Ncy\ntlmGt/MzXjhskdV92RnTtxrZNm72/PMpP+Nu/zYzxu0pLmjIsO+vYEZ2XGiOk8A7\ngxprF0yA1O2qdL57vMxaxsQ=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-wg4m0@esdbuyerms.iam.gserviceaccount.com",
        "client_id": "115344412453360573851",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-wg4m0%40esdbuyerms.iam.gserviceaccount.com"
    }
   
)


firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

#GET ALL BUYER
@app.route("/buyers")
def get_all_buyer():
    result  = []
    buyer_doc = db.collection('buyers').stream()
    for buyer in buyer_doc:
        result.append(buyer.to_dict())
    
    if len(result) == 0:
        return jsonify(
            {
                "code": 401,
                "message": "Buyer database is empty"
            }
        )
    return jsonify(
        {
            "code": 200,
            "data": {
                "buyers": result
            }
        }
    )

# ADD NEW BUYER
@app.route("/buyers/add", methods=["POST", "GET"])
def add_buyer():
    allBuyers = db.collection('buyers').get()
    buyerInfo = request.get_json()
    for buyer in allBuyers:
        buyer = buyer.to_dict()
        if buyer['email'] == buyerInfo["email"]:
            return jsonify(
                {
                    "code":  404,
                    "message": "buyer already exists"
                }
            )
    try:
        db.collection('buyers').document(buyerInfo['email']).set(buyerInfo)
        return jsonify(
            {
                "code": 200,
                "message": "Successfully added buyer"
            }
        )
    except:
        return jsonify(
            {
                "code": 404,
                "message": "Error occured when adding buyer"
            }
        )

#UPDATE BUYER INFO
@app.route("/buyer/update/<string:buyerEmail>", methods=["POST", "GET", "PUT"])
def update_buyer(buyerEmail):
    buyerRef = db.collection('buyers').document(buyerEmail)
    print(buyerRef)
    buyerInfo = request.get_json()
    print(buyerInfo)
    if buyerInfo["email"] != buyerEmail:
        try: #CREATE NEW
            db.collection("buyers").document(buyerInfo["email"]).set(buyerInfo)
             
             #DELETE OLD
            db.collection('buyers').document(buyerEmail).delete()
        except:
            return jsonify({"code": 404, "message": "Error occured when updating buyer"})
        
        return jsonify({"code": 201, "message": "Successfully Updated Email Address and Information"})
    else:
        try:
            buyerRef.update(buyerInfo)

        except:
            return jsonify({"code": 404, "message": "Error occured when updating buyer info"})
            
        return jsonify({"code": 201, "message": "Successfully Updated Information"})
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5055, debug=True)