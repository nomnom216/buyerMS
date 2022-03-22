from flask import Flask, request, jsonify, render_template

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "nomnom-db",
        "private_key_id": "fdb67a9818e1c2ea5d01b176f7cb245de51fbc3e",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCYROhduezfEq1A\n1qyY5/4zLhHVnwcBWp9LdyHngbZAs7oxxQ8zLc56wZJ8kdO+TXsO7WiAxdZcGqRr\nOnldtkkg/DXSTu8PyW6lfVGub04KUD1ZmyZhy2yr9DJpVF+0yTSzhYH6O1Hwf7QR\ny1OmOo764Rxo7ACKUd6e/ssvA63yzfNEc28xwIgymqghYrMa22WBlK/ADeaDmCKh\nMfqNk2vIsifyzj24AMiB0rfNhe2232n3vvVDA1Bjx/nDh6gRFvLYu+68oZ5Ga7Qs\ns8jyl81VCIdT4QNNmIEt4z7gFOTAXXYzAeCKXzeeCJbRIG986/I9ykgXSEmaACig\njsKwXDTXAgMBAAECggEAOVBWllDRU/XXuLwVI0jPabxBgkLlhCD0LJee72DnlNsR\njoI6Am2Pdq090h2hsdPAKhI6b54H3Ys5sBLGc/uU8xF7wLltSmfreeb9w8apfUBO\nl1fKzqyfLuovv22+yHGjoJ70GZgSc4/d24TI65zHDK+G3gdW/LlsLjSBjiS4aNd/\nupUuMiLe7Sk6xlL4Zc9uV7Dzwz+y6w+0dEkksEtzVe1CI30Eu2PULoJlP0NrzBqD\nmcxmG/6LXeyksKMaRWXtzi3AnHge06NGrl8tlGIklVs84baNoEwjBXIwIfJ45OLu\nT4yVByaVzGYK3mJKN5XHg+c3QngF1AXzBmMS3dyQIQKBgQDJ4SR5AIbB4/Lu+7e5\n7lfbkQoAgkaOAdu6+oLN2GwNIx8DTpeSxO9o7olrqnXIk6kMkpbvi2Vfpku4x7S2\nxEDY/wHl8YTk8eZu+1b4AlNdTnRwxD86b0Cg8hQF8cyf7F5IqSisc3zS+VSSx+2h\n6AmXaGI5JzKzmXmDAjyq4gylAwKBgQDBFwr1ST/oQ1zLylMwtTZThwcENnpxwiz9\nDN5SQqoNEBYm6rVbngFlXNaas1lsFdJeA7q5X7sWgrSOuJPwltlOPJHSjn+HL+LF\nZ261QUzatwDTDcpjt62P7zVoILEDiZxDzeWb/q/ydNej2ZKwFtCDqcqSwphtJ4yC\nibWVHmRWnQKBgD0XHGphdmYGDOW01ow1S/DtmxE8Ww1uEogqdprD+y6eiiv+BHAt\nmCUwyfUCyFHCHU3orjQfArZHJHLuPAlyqg0AXhqvU3/Uk97RwCeczI1XyHS3bkrI\nj84kc1q5KSrb5EwopF5LNGLDgIxKY+ayyPRAajjRW85tiw/SBXnQnfLxAoGADFeJ\ntsX41MLBgrErAhkDIPGnjChjSTQtJfuVllJ2hiE6GUC1WObPlggKG5dNJvB6ItJA\nNCsfTUALhHfd1On/d9W9SGUdV6nC5/VFiUZkQDKkVdkyz47lBCc5Fa/JQL2iBF97\nxq3P10KKqgl1K9Y5e8D1ls3jak61134v4hkwNq0CgYATrDYUyCDvSlEgMFU/qQgy\nYBv5U4pHj56QDsO1Qe7F+J97CJyuDfKYMUdcdbKYI4p6xL+xSlPIAPSwuov6MKny\n63A7Ga5v5wZay4p2l9MpsieIE7PnO4HF7OBAwoTwZMh5o6TkFBbocYlEHhu0UY7p\nGEPrIlkeA1/oaBrKjN9FJA==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-bhktu@nomnom-db.iam.gserviceaccount.com",
        "client_id": "108783214540036148659",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-bhktu%40nomnom-db.iam.gserviceaccount.com"
    }   
)

# cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

#GET ALL BUYER
@app.route("/buyers")
def get_all_buyer():
    result  = []
    buyer_doc = db.collection('users').stream()
    for buyer in buyer_doc:
        result.append(buyer.to_dict())
    
    if len(result) == 0:
        return jsonify(
            {
                "code": 401,
                "message": "buyer db is empty"
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
                "message": "congratz buyer addeded"
            }
        )
    except:
        return jsonify(
            {
                "code": 404,
                "message": "error while adding buyer :/"
            }
        )

#UPDATE BUYER INFO
@app.route("/buyer/update/<string:buyerEmail>", methods=["POST", "GET"])
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
    app.run(host='0.0.0.0', port=5000, debug=True)