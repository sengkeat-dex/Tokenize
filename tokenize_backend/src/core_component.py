#!/usr/bin/env python3
"""
Core component module for the Tokenization Platform

This module provides the main functionality for managing tokenized assets and digital wallets.
It includes core operations such as asset tokenization, wallet management, and compliance checks.
"""

import json
import time
from typing import Dict, List, Optional, Union
from enum import Enum
from threading import RLock


class AssetType(Enum):
    EQUITY = "equity"
    DEBT = "debt"
    REAL_ESTATE = "real_estate"
    COMMODITY = "commodity"
    FUND = "fund"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    ART = "art"
    CARBON_CREDIT = "carbon_credit"
    OTHER = "other"


class ComplianceStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    UNDER_REVIEW = "under_review"


class WalletType(Enum):
    CUSTODIAL = "custodial"
    NON_CUSTODIAL = "non_custodial"
    HYBRID = "hybrid"


class TokenizedAsset:
    def __init__(self, asset_id: str, name: str, asset_type: Union[AssetType, str], value: float, 
                 owner: str, metadata: Optional[Dict[str, str]] = None):
        self.id = asset_id
        self.name = name
        self.asset_type = asset_type if isinstance(asset_type, AssetType) else self._parse_asset_type(asset_type)
        self.value = value
        self.owner = owner
        self.metadata = metadata or {}
        self.compliance_status = ComplianceStatus.PENDING
        self.created_at = int(time.time())
        self.updated_at = int(time.time())

    def _parse_asset_type(self, asset_type_str: str) -> AssetType:
        """Parse a string into an AssetType enum, defaulting to OTHER if not found"""
        try:
            return AssetType(asset_type_str)
        except ValueError:
            return AssetType.OTHER

    def to_dict(self) -> Dict:
        # Handle both enum and string asset types
        asset_type_value = self.asset_type.value if isinstance(self.asset_type, AssetType) else self.asset_type
        compliance_status_value = self.compliance_status.value if isinstance(self.compliance_status, ComplianceStatus) else self.compliance_status
        
        return {
            "id": self.id,
            "name": self.name,
            "asset_type": asset_type_value,
            "value": self.value,
            "owner": self.owner,
            "metadata": self.metadata,
            "compliance_status": compliance_status_value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TokenizedAsset':
        asset = cls(
            asset_id=data["id"],
            name=data["name"],
            asset_type=data["asset_type"],
            value=data["value"],
            owner=data["owner"],
            metadata=data.get("metadata", {})
        )
        # Handle both enum and string compliance status
        compliance_status_value = data["compliance_status"]
        if isinstance(compliance_status_value, str):
            try:
                asset.compliance_status = ComplianceStatus(compliance_status_value)
            except ValueError:
                asset.compliance_status = ComplianceStatus.PENDING
        else:
            asset.compliance_status = compliance_status_value
        asset.created_at = data["created_at"]
        asset.updated_at = data["updated_at"]
        return asset


class DigitalWallet:
    def __init__(self, wallet_id: str, owner: str, wallet_type: Union[WalletType, str]):
        self.id = wallet_id
        self.owner = owner
        self.assets: List[str] = []  # Asset IDs
        self.balance = 0.0
        self.wallet_type = wallet_type if isinstance(wallet_type, WalletType) else self._parse_wallet_type(wallet_type)
        self.created_at = int(time.time())
        self.updated_at = int(time.time())

    def _parse_wallet_type(self, wallet_type_str: str) -> WalletType:
        """Parse a string into a WalletType enum, defaulting to CUSTODIAL if not found"""
        try:
            return WalletType(wallet_type_str)
        except ValueError:
            return WalletType.CUSTODIAL

    def to_dict(self) -> Dict:
        # Handle both enum and string wallet types
        wallet_type_value = self.wallet_type.value if isinstance(self.wallet_type, WalletType) else self.wallet_type
        
        return {
            "id": self.id,
            "owner": self.owner,
            "assets": self.assets,
            "balance": self.balance,
            "wallet_type": wallet_type_value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'DigitalWallet':
        wallet = cls(
            wallet_id=data["id"],
            owner=data["owner"],
            wallet_type=data["wallet_type"]
        )
        wallet.assets = data["assets"]
        wallet.balance = data["balance"]
        wallet.created_at = data["created_at"]
        wallet.updated_at = data["updated_at"]
        return wallet


class TokenizationCore:
    def __init__(self):
        self._assets: Dict[str, TokenizedAsset] = {}
        self._wallets: Dict[str, DigitalWallet] = {}
        self._lock = RLock()

    def create_asset(self, asset: TokenizedAsset) -> str:
        """Create a new tokenized asset"""
        with self._lock:
            self._assets[asset.id] = asset
            return asset.id

    def get_asset(self, asset_id: str) -> Optional[TokenizedAsset]:
        """Get an asset by ID"""
        with self._lock:
            return self._assets.get(asset_id)

    def update_asset(self, asset_id: str, updated_asset: TokenizedAsset) -> bool:
        """Update an asset"""
        with self._lock:
            if asset_id in self._assets:
                self._assets[asset_id] = updated_asset
                return True
            return False

    def delete_asset(self, asset_id: str) -> bool:
        """Delete an asset"""
        with self._lock:
            if asset_id in self._assets:
                del self._assets[asset_id]
                # Remove asset from any wallets that contain it
                for wallet in self._wallets.values():
                    if asset_id in wallet.assets:
                        wallet.assets.remove(asset_id)
                        # Update wallet balance
                        asset = self._assets.get(asset_id)
                        if asset:
                            wallet.balance -= asset.value
                return True
            return False

    def create_wallet(self, wallet: DigitalWallet) -> str:
        """Create a new digital wallet"""
        with self._lock:
            self._wallets[wallet.id] = wallet
            return wallet.id

    def get_wallet(self, wallet_id: str) -> Optional[DigitalWallet]:
        """Get a wallet by ID"""
        with self._lock:
            return self._wallets.get(wallet_id)

    def add_asset_to_wallet(self, wallet_id: str, asset_id: str) -> bool:
        """Add an asset to a wallet"""
        with self._lock:
            wallet = self._wallets.get(wallet_id)
            asset = self._assets.get(asset_id)
            
            if wallet and asset:
                if asset_id not in wallet.assets:
                    wallet.assets.append(asset_id)
                    # Update wallet balance
                    wallet.balance += asset.value
                    wallet.updated_at = int(time.time())
                    return True
                else:
                    # Asset already in wallet
                    return False
            else:
                # Wallet or asset not found
                return False

    def remove_asset_from_wallet(self, wallet_id: str, asset_id: str) -> bool:
        """Remove an asset from a wallet"""
        with self._lock:
            wallet = self._wallets.get(wallet_id)
            asset = self._assets.get(asset_id)
            
            if wallet and asset:
                if asset_id in wallet.assets:
                    wallet.assets.remove(asset_id)
                    # Update wallet balance
                    wallet.balance -= asset.value
                    wallet.updated_at = int(time.time())
                    return True
                else:
                    # Asset not in wallet
                    return False
            else:
                # Wallet or asset not found
                return False

    def perform_compliance_check(self, asset_id: str) -> Optional[ComplianceStatus]:
        """Perform compliance check on an asset"""
        with self._lock:
            asset = self._assets.get(asset_id)
            if asset:
                asset.compliance_status = ComplianceStatus.APPROVED
                asset.updated_at = int(time.time())
                return asset.compliance_status
            return None

    def get_assets_by_type(self, asset_type: Union[AssetType, str]) -> List[TokenizedAsset]:
        """Get all assets of a specific type"""
        with self._lock:
            # Handle both enum and string asset types
            asset_type_value = asset_type.value if isinstance(asset_type, AssetType) else asset_type
            return [asset for asset in self._assets.values() if 
                   (isinstance(asset.asset_type, AssetType) and asset.asset_type.value == asset_type_value) or
                   (isinstance(asset.asset_type, str) and asset.asset_type == asset_type_value)]

    def get_wallet_value(self, wallet_id: str) -> Optional[float]:
        """Get total value of assets in a wallet"""
        with self._lock:
            wallet = self._wallets.get(wallet_id)
            if wallet:
                return wallet.balance
            return None

    def to_dict(self) -> Dict:
        """Serialize the core state to a dictionary"""
        return {
            "assets": {aid: asset.to_dict() for aid, asset in self._assets.items()},
            "wallets": {wid: wallet.to_dict() for wid, wallet in self._wallets.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TokenizationCore':
        """Deserialize the core state from a dictionary"""
        core = cls()
        core._assets = {aid: TokenizedAsset.from_dict(asset_data) 
                       for aid, asset_data in data.get("assets", {}).items()}
        core._wallets = {wid: DigitalWallet.from_dict(wallet_data) 
                        for wid, wallet_data in data.get("wallets", {}).items()}
        return core


# Example usage
if __name__ == "__main__":
    # Create a new tokenization core instance
    core = TokenizationCore()
    
    # Create a sample tokenized asset
    asset = TokenizedAsset(
        asset_id="asset_001",
        name="Tech Company Equity Shares",
        asset_type=AssetType.EQUITY,
        value=50000.0,
        owner="user_001",
        metadata={
            "issuer": "Example Corp",
            "country": "USA"
        }
    )
    
    # Create the asset in the system
    asset_id = core.create_asset(asset)
    print(f"✓ Created asset with ID: {asset_id}")
    
    # Retrieve the asset
    retrieved_asset = core.get_asset("asset_001")
    if retrieved_asset:
        print(f"✓ Retrieved asset: {retrieved_asset.name}")
        print(f"  Type: {retrieved_asset.asset_type.value if isinstance(retrieved_asset.asset_type, AssetType) else retrieved_asset.asset_type}")
        print(f"  Value: ${retrieved_asset.value}")
        print(f"  Owner: {retrieved_asset.owner}")
    
    # Create a digital wallet
    wallet = DigitalWallet(
        wallet_id="wallet_001",
        owner="user_001",
        wallet_type=WalletType.CUSTODIAL
    )
    
    # Create the wallet in the system
    wallet_id = core.create_wallet(wallet)
    print(f"✓ Created wallet with ID: {wallet_id}")
    
    # Add asset to wallet
    success = core.add_asset_to_wallet("wallet_001", "asset_001")
    if success:
        print("✓ Added asset to wallet")
    else:
        print("✗ Failed to add asset to wallet")
    
    # Check wallet value
    wallet_value = core.get_wallet_value("wallet_001")
    if wallet_value is not None:
        print(f"✓ Wallet total value: ${wallet_value}")
    
    # Perform compliance check
    compliance_status = core.perform_compliance_check("asset_001")
    if compliance_status:
        print(f"✓ Compliance check completed: {compliance_status.value}")
    
    # Retrieve updated asset
    updated_asset = core.get_asset("asset_001")
    if updated_asset:
        compliance_value = updated_asset.compliance_status.value if isinstance(updated_asset.compliance_status, ComplianceStatus) else updated_asset.compliance_status
        print(f"✓ Asset compliance status: {compliance_value}")
    
    print("\nExample completed successfully!")