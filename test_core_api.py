import urllib.request
import urllib.parse
import json

# Test getting assets (should be empty initially)
try:
    req = urllib.request.Request('http://localhost:3032/api/core/assets')
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode())
    print("Initial assets:", data)
except Exception as e:
    print("Error getting assets:", e)

# Test creating an asset
asset_data = {
    "id": "asset_001",
    "name": "Tech Company Equity Shares",
    "asset_type": "equity",
    "value": 50000.0,
    "owner": "user_001",
    "metadata": {
        "issuer": "Example Corp",
        "country": "USA"
    }
}

try:
    data = json.dumps(asset_data).encode('utf-8')
    req = urllib.request.Request(
        'http://localhost:3032/api/core/assets',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    print("Create asset result:", result)
except Exception as e:
    print("Error creating asset:", e)

# Test creating a wallet
wallet_data = {
    "id": "wallet_001",
    "owner": "user_001",
    "wallet_type": "custodial"
}

try:
    data = json.dumps(wallet_data).encode('utf-8')
    req = urllib.request.Request(
        'http://localhost:3032/api/core/wallets',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    print("Create wallet result:", result)
except Exception as e:
    print("Error creating wallet:", e)

# Test getting assets again
try:
    req = urllib.request.Request('http://localhost:3032/api/core/assets')
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode())
    print("Assets after creation:", data)
except Exception as e:
    print("Error getting assets:", e)

# Test getting wallets
try:
    req = urllib.request.Request('http://localhost:3032/api/core/wallets')
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode())
    print("Wallets:", data)
except Exception as e:
    print("Error getting wallets:", e)