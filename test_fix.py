import urllib.request
import urllib.parse
import json

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

# Test getting the asset we just created
try:
    req = urllib.request.Request('http://localhost:3032/api/core/assets/asset_001')
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode())
    print("Get asset result:", data)
except Exception as e:
    print("Error getting asset:", e)

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

# Test getting all assets
try:
    req = urllib.request.Request('http://localhost:3032/api/core/assets')
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode())
    print("All assets:", data)
except Exception as e:
    print("Error getting all assets:", e)