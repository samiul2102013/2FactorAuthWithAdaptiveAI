from flask import Flask, request, jsonify
import hashlib, random, time
import joblib
from web3 import Web3
import os
import json

app = Flask(__name__)

# Load ML Model (trained on: ip_score, time_score, device_score, frequency, geo_score)
model = joblib.load('../ml_model/behavior_model.pkl')

# Connect to local Ganache blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
contract_address = "0x9a2C69b7111399125447D66C4d929858e67D4795"

# Load ABI from build/contracts/Auth.json
with open('../blockchain/build/contracts/Auth.json') as f:
    contract_json = json.load(f)
    abi = contract_json['abi']

contract = w3.eth.contract(address=contract_address, abi=abi)
w3.eth.default_account = w3.eth.accounts[0]

known_user_profile = {
    "ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0",
    "hour": 14  
}

def generate_hash():
    return hashlib.sha256(str(random.random()).encode()).hexdigest()

def get_metadata():
    return {
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
        "hour": time.localtime().tm_hour
    }

def extract_features(meta):
    ip_score = 1.0 if meta['ip'] == known_user_profile['ip'] else 0.3
    time_score = max(0, 1 - abs(meta['hour'] - known_user_profile['hour']) / 24)
    device_score = 1.0 if known_user_profile['user_agent'] in meta['user_agent'] else 0.4
    frequency = random.randint(5, 20)  
    geo_score = random.uniform(0.4, 1.0)  
    return [ip_score, time_score, device_score, frequency, geo_score]

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data['username'] == 'admin' and data['password'] == 'secret123':
        meta = get_metadata()
        features = extract_features(meta)

        prediction = model.predict([features])[0]

        if prediction == 0:
            return jsonify({
                "msg": "Suspicious login detected, additional verification needed",
                "features": features
            }), 401

        user_hash = generate_hash()
        media_hash = generate_hash()
        tx_hash = contract.functions.storeHash(user_hash, media_hash).transact()
        return jsonify({
            "msg": "Authenticated",
            "user_hash": user_hash,
            "media_hash": media_hash,
            "features": features
        })
    return jsonify({"msg": "Invalid credentials"}), 403

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    stored = contract.functions.getHash(data['user_hash']).call()
    return jsonify({"verified": stored == data['media_hash']})

if __name__ == '__main__':
    app.run(debug=True)
