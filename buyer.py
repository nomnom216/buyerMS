from flask import Flask, request, jsonify, render_template

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

# @app.route("/addbuyer", methods=["POST", "GET"])
# def home():
#     if request.method == "POST":
#         pass
#     return render_template('home.html')


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
    app.run(port=5000, debug=True)