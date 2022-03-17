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

# add buyer
@app.route("/add/<string:buyerName>/<string:buyerID>", methods=["POST", "GET"])
def add_buyer(buyerName, buyerID):
    allBuyers = db.collection('buyers').get()
    for buyer in allBuyers:
        buyer = buyer.to_dict()
        if buyer['id'] == buyerID:
            return jsonify(
                {
                    "code":  404,
                    "message": "buyer already exists"
                }
            )
    try:
        db.collection('buyers').add({'name':buyerName,'id':buyerID})
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


if __name__ == "__main__":
    app.run(port=5000, debug=True)