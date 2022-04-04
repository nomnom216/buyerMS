from audioop import cross
from flask import Flask, request, jsonify, render_template

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from flask_cors import CORS, cross_origin 

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "nomnom-db",
        "private_key_id": "c05892efb3974dbadeaaa4c6475146306619e538",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDQFXj8SxqCtnlu\nyZ0sN7JVa8puoGnuSYAY6bZ5NgGSsbI3hYS7OlMfn0siXUM5/9G9f/GPqjBiI87U\nacarvXwpXnzm773uSbKH+zEjzO74SGfsHe0W+inaH5s7ettWE+u8A52lMm9Wcnm7\npbwrXZm7lpRwIXL053tlzTExMg45CTgThQtCA33jcL7eVpEL2WhmA/fzzRd36UDv\nHGBFrAvOLahC1C4LbCC2KR5hHQAkB4mvBAGK2JCC/9qRGfXLqCNZQHHtwUOy+/J/\nxxIZo8A/pp1pdlNrz/vpKMEhakv3VqyTxdCbCMDw8zMUbFW+N3L5lzXOKlT7E0hQ\nHKUpvx2ZAgMBAAECggEAJcTX/ndFWxdy6CSJNkbvxCh6CGVuhNVrflohiFPAqlc9\noW1HP9Kg1tsLgLPL6YGhGNPZzTlXaeDVAGIosPCGUl33rtUyNMfEs4DpFPX0JDXE\nQyvVZnfG0/QrsXqlyDR6c9h2K0+BvP+vT9uP0ZE+P7nfvJCdtI01rS828BaFVV2e\nbhn4Z+bnvj47xa0HcOGgxLJoy0SUNiPMmzvFQUrrJeLloKpK4xxyh2WfZjjMHuIJ\nX6J4A9jsfoh3Gbhje+DlOh9cluSYxcdrZqhKX1J7yRc0pp8ifQhD7j3Xap47YGP9\n3zrl++RXjngtGN/NVe7M24EkUYnRiXmKVHK/QC0SrwKBgQD7GMvQ3RjfhdFgRBJZ\nY5NvE3BBkcKy0vYNqAuwwFG1wm6ZQ12e2JR6FnMtKj84lFkw6LNKf33I/hDmvfeW\nyxOS9hw9uxrKsEwcVyI6TeGxB8rBYvqslxKd7vo6CIeJ31f8bHLgKQx/MLB1i3tV\n9CiN5xba78CGYJEO2pr+6Q8r0wKBgQDUJajZxNElTC4zz4CXYi3FR0ZYdm8qGmu2\nDvaXi6IZKvuTGgV8/n8qUsrVH1GCvqsPMQpAvO8wmGDWW93Vep3FymViuyF+Eg8u\nKotcm9hfx42SlCifTlDROH/9uG02RVTGs9wAECUi+DsspTuK4jDWaPuFoGt76h99\n0eSxwdZJYwKBgGbB6wb6tGclGF5Q/UFfosJeLh5nTEpqUw+bqc0Xp1i+zQwjqXiM\nIZclANWG6IB7FVUSpezi59MNRlVngJ9RVB1cYopQu9Ie+8bNUdCSdr4/9hXWL8fZ\nu2Cun/CH9Q/TOuquZwSdR+P1RQGVp0+xr7cCzzOh0iQr+LEffTa8odzJAoGAdNd1\nAtOKmS829yQe38GcEd5qmQhJu3enwTLGj7rBAXmR63fWc/w7D5VfzzebjhXzYr+Q\ntQ0Z87rJAua/6/bHdIs/gbws+yF5KOUXsl7HMiFXENb29J6Olly26Yes5soSogmn\nboV13qe296TdgWWInl5dwUAUUsAkrghvG5P1sJ8CgYEA81c4yPuVypyR8VSuLMQV\nEgxKoRjqjYi+Y2xbLQ57/z9MlAL7CRvc2n7E4nevi2IDgT0o0y/LBoX9qVz55BEK\nMesPz74UBKr9mM8drzpDYfoEtAQJ0RkRb6Ddx8D5k0nkvF7a4ElYMawoOwJ4zwER\njbqQ7rI+iIaZ9qYXdnSz+iE=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-bhktu@nomnom-db.iam.gserviceaccount.com",
        "client_id": "108783214540036148659",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-bhktu%40nomnom-db.iam.gserviceaccount.com"
    }
   
)


firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)

#GET ALL BUYER
@app.route("/getAllBuyers")
@cross_origin()
def get_all_buyer():
    result  = []
    buyer_doc = db.collection('buyers').stream()
    for buyer in buyer_doc:
        result.append(buyer.to_dict())
    
    if len(result) == 0:
        return jsonify(
            {
                "code": 404,
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
@app.route("/addNewBuyer", methods=["POST", "GET"])
@cross_origin()
def add_buyer():
    allBuyers = db.collection('buyers').get()
    buyerInfo = request.get_json()
    # return buyerInfo
    for buyer in allBuyers:
        buyer = buyer.to_dict()
        if buyer['uid'] == buyerInfo['buyerInfo']["uid"]:
            return jsonify(
                {
                    "code":  400,
                    "message": "buyer already exists"
                }
            )
    try:
        db.collection('buyers').document(buyerInfo['buyerInfo']['uid']).set(buyerInfo['buyerInfo'])
        return jsonify(
            {
                "code": 201,
                "message": "Successfully added buyer"
            }
        )
    except:
        return jsonify(
            {
                "code": 500,
                "message": "Error occured when adding buyer"
            }
        )

#GET BUYER INFO BY ID
@app.route("/getBuyerById/<string:buyerID>", methods=["GET","POST"]) 
@cross_origin()
def getSellerById(buyerID):
    # sellerData = request.get_json()
    sellerDetail = db.collection('buyers').document(buyerID).get()
    return sellerDetail.to_dict()


#UPDATE BUYER INFO
@app.route("/updateBuyer/<string:buyerID>", methods=["POST", "GET", "PUT"])
@cross_origin()
def update_buyer(buyerID):
    buyerRef = db.collection('buyers').document(buyerID)
    print(buyerRef)
    buyerInfo = request.get_json()
    print(buyerInfo)
    if buyerInfo['buyerInfo']["uid"] != buyerID:
        try: #CREATE NEW
            db.collection("buyers").document(buyerInfo['buyerInfo']["uid"]).set(buyerInfo['buyerInfo'])
             
             #DELETE OLD
            db.collection('buyers').document(buyerID).delete()
        except:
            return jsonify({"code": 500, "message": "Error occured when updating buyer"})
        
        return jsonify({"code": 200, "message": "Successfully Updated Email Address and Information"})
    else:
        try:
            buyerRef.update(buyerInfo['buyerInfo'])

        except:
            return jsonify({"code": 500, "message": "Error occured when updating buyer info"})
            
        return jsonify({"code": 200, "message": "Successfully Updated Information"})
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5055, debug=True)