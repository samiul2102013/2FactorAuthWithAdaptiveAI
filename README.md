# Blockchain-Based 2FA Authentication with Adaptive ML

## Features
- Blockchain-based secure login
- Adaptive ML model checks user behavior
- Random hashes stored and verified on-chain

## Run the Project

### 1. Train ML model
```
cd ml_model
python3 train_model.py
```

### 2. Compile and deploy smart contract
Use Truffle or Remix to deploy `Auth.sol`. Update the contract address and ABI in `app.py`.

### 3. Start Flask backend
```
cd backend
pip install -r ../requirements.txt
python3 app.py
```

## Sample API
POST /login — Login using adaptive model  
POST /verify — Verify stored hash
#   2 F a c t o r A u t h W i t h A d a p t i v e A I  
 