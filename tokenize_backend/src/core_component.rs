//! Core component module for the Tokenization Platform
//! 
//! This module provides the main functionality for managing tokenized assets and digital wallets.
//! It includes core operations such as asset tokenization, wallet management, and compliance checks.

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

/// Represents a tokenized asset with all its properties
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TokenizedAsset {
    pub id: String,
    pub name: String,
    pub asset_type: AssetType,
    pub value: f64,
    pub owner: String,
    pub metadata: HashMap<String, String>,
    pub compliance_status: ComplianceStatus,
    pub created_at: u64,
    pub updated_at: u64,
}

/// Enum representing different types of tokenized assets
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum AssetType {
    Equity,
    Debt,
    RealEstate,
    Commodity,
    Fund,
    IntellectualProperty,
    Art,
    CarbonCredit,
    Other(String),
}

/// Enum representing compliance status of an asset
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ComplianceStatus {
    Pending,
    Approved,
    Rejected,
    UnderReview,
}

/// Represents a digital wallet for holding tokenized assets
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DigitalWallet {
    pub id: String,
    pub owner: String,
    pub assets: Vec<String>, // Asset IDs
    pub balance: f64,
    pub wallet_type: WalletType,
    pub created_at: u64,
    pub updated_at: u64,
}

/// Enum representing different types of wallets
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum WalletType {
    Custodial,
    NonCustodial,
    Hybrid,
}

/// Core component that manages tokenized assets and wallets
pub struct TokenizationCore {
    assets: Arc<RwLock<HashMap<String, TokenizedAsset>>>,
    wallets: Arc<RwLock<HashMap<String, DigitalWallet>>>,
}

impl TokenizationCore {
    /// Create a new TokenizationCore instance
    pub fn new() -> Self {
        Self {
            assets: Arc::new(RwLock::new(HashMap::new())),
            wallets: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    /// Create a new tokenized asset
    pub fn create_asset(&self, asset: TokenizedAsset) -> Result<String, String> {
        let mut assets = self.assets.write().map_err(|_| "Failed to acquire write lock")?;
        let asset_id = asset.id.clone();
        assets.insert(asset_id.clone(), asset);
        Ok(asset_id)
    }

    /// Get an asset by ID
    pub fn get_asset(&self, asset_id: &str) -> Result<Option<TokenizedAsset>, String> {
        let assets = self.assets.read().map_err(|_| "Failed to acquire read lock")?;
        Ok(assets.get(asset_id).cloned())
    }

    /// Update an asset
    pub fn update_asset(&self, asset_id: &str, updated_asset: TokenizedAsset) -> Result<(), String> {
        let mut assets = self.assets.write().map_err(|_| "Failed to acquire write lock")?;
        if assets.contains_key(asset_id) {
            assets.insert(asset_id.to_string(), updated_asset);
            Ok(())
        } else {
            Err("Asset not found".to_string())
        }
    }

    /// Delete an asset
    pub fn delete_asset(&self, asset_id: &str) -> Result<(), String> {
        let mut assets = self.assets.write().map_err(|_| "Failed to acquire write lock")?;
        if assets.remove(asset_id).is_some() {
            Ok(())
        } else {
            Err("Asset not found".to_string())
        }
    }

    /// Create a new digital wallet
    pub fn create_wallet(&self, wallet: DigitalWallet) -> Result<String, String> {
        let mut wallets = self.wallets.write().map_err(|_| "Failed to acquire write lock")?;
        let wallet_id = wallet.id.clone();
        wallets.insert(wallet_id.clone(), wallet);
        Ok(wallet_id)
    }

    /// Get a wallet by ID
    pub fn get_wallet(&self, wallet_id: &str) -> Result<Option<DigitalWallet>, String> {
        let wallets = self.wallets.read().map_err(|_| "Failed to acquire read lock")?;
        Ok(wallets.get(wallet_id).cloned())
    }

    /// Add an asset to a wallet
    pub fn add_asset_to_wallet(&self, wallet_id: &str, asset_id: &str) -> Result<(), String> {
        let mut wallets = self.wallets.write().map_err(|_| "Failed to acquire write lock")?;
        let mut assets = self.assets.write().map_err(|_| "Failed to acquire write lock")?;
        
        if let Some(wallet) = wallets.get_mut(wallet_id) {
            if assets.contains_key(asset_id) {
                if !wallet.assets.contains(&asset_id.to_string()) {
                    wallet.assets.push(asset_id.to_string());
                    // Update wallet balance based on asset value
                    if let Some(asset) = assets.get(asset_id) {
                        wallet.balance += asset.value;
                    }
                    Ok(())
                } else {
                    Err("Asset already in wallet".to_string())
                }
            } else {
                Err("Asset not found".to_string())
            }
        } else {
            Err("Wallet not found".to_string())
        }
    }

    /// Remove an asset from a wallet
    pub fn remove_asset_from_wallet(&self, wallet_id: &str, asset_id: &str) -> Result<(), String> {
        let mut wallets = self.wallets.write().map_err(|_| "Failed to acquire write lock")?;
        let mut assets = self.assets.write().map_err(|_| "Failed to acquire write lock")?;
        
        if let Some(wallet) = wallets.get_mut(wallet_id) {
            if let Some(index) = wallet.assets.iter().position(|x| x == asset_id) {
                wallet.assets.remove(index);
                // Update wallet balance based on asset value
                if let Some(asset) = assets.get(asset_id) {
                    wallet.balance -= asset.value;
                }
                Ok(())
            } else {
                Err("Asset not in wallet".to_string())
            }
        } else {
            Err("Wallet not found".to_string())
        }
    }

    /// Perform compliance check on an asset
    pub fn perform_compliance_check(&self, asset_id: &str) -> Result<ComplianceStatus, String> {
        // In a real implementation, this would involve complex compliance logic
        // For now, we'll just return Approved as a placeholder
        let mut assets = self.assets.write().map_err(|_| "Failed to acquire write lock")?;
        
        if let Some(asset) = assets.get_mut(asset_id) {
            asset.compliance_status = ComplianceStatus::Approved;
            asset.updated_at = std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .map(|d| d.as_secs())
                .unwrap_or(0);
            Ok(ComplianceStatus::Approved)
        } else {
            Err("Asset not found".to_string())
        }
    }

    /// Get all assets of a specific type
    pub fn get_assets_by_type(&self, asset_type: AssetType) -> Result<Vec<TokenizedAsset>, String> {
        let assets = self.assets.read().map_err(|_| "Failed to acquire read lock")?;
        let filtered_assets: Vec<TokenizedAsset> = assets
            .values()
            .filter(|asset| asset.asset_type == asset_type)
            .cloned()
            .collect();
        Ok(filtered_assets)
    }

    /// Get total value of assets in a wallet
    pub fn get_wallet_value(&self, wallet_id: &str) -> Result<f64, String> {
        let wallets = self.wallets.read().map_err(|_| "Failed to acquire read lock")?;
        let assets = self.assets.read().map_err(|_| "Failed to acquire read lock")?;
        
        if let Some(wallet) = wallets.get(wallet_id) {
            let mut total_value = 0.0;
            for asset_id in &wallet.assets {
                if let Some(asset) = assets.get(asset_id) {
                    total_value += asset.value;
                }
            }
            Ok(total_value)
        } else {
            Err("Wallet not found".to_string())
        }
    }
}

impl Default for TokenizationCore {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_and_get_asset() {
        let core = TokenizationCore::new();
        
        let asset = TokenizedAsset {
            id: "asset1".to_string(),
            name: "Test Asset".to_string(),
            asset_type: AssetType::Equity,
            value: 100.0,
            owner: "user1".to_string(),
            metadata: HashMap::new(),
            compliance_status: ComplianceStatus::Pending,
            created_at: 0,
            updated_at: 0,
        };
        
        let result = core.create_asset(asset.clone());
        assert!(result.is_ok());
        
        let retrieved_asset = core.get_asset("asset1").unwrap();
        assert!(retrieved_asset.is_some());
        assert_eq!(retrieved_asset.unwrap().name, "Test Asset");
    }

    #[test]
    fn test_create_and_get_wallet() {
        let core = TokenizationCore::new();
        
        let wallet = DigitalWallet {
            id: "wallet1".to_string(),
            owner: "user1".to_string(),
            assets: vec![],
            balance: 0.0,
            wallet_type: WalletType::Custodial,
            created_at: 0,
            updated_at: 0,
        };
        
        let result = core.create_wallet(wallet.clone());
        assert!(result.is_ok());
        
        let retrieved_wallet = core.get_wallet("wallet1").unwrap();
        assert!(retrieved_wallet.is_some());
        assert_eq!(retrieved_wallet.unwrap().owner, "user1");
    }

    #[test]
    fn test_add_asset_to_wallet() {
        let core = TokenizationCore::new();
        
        // Create asset
        let asset = TokenizedAsset {
            id: "asset1".to_string(),
            name: "Test Asset".to_string(),
            asset_type: AssetType::Equity,
            value: 100.0,
            owner: "user1".to_string(),
            metadata: HashMap::new(),
            compliance_status: ComplianceStatus::Pending,
            created_at: 0,
            updated_at: 0,
        };
        
        core.create_asset(asset).unwrap();
        
        // Create wallet
        let wallet = DigitalWallet {
            id: "wallet1".to_string(),
            owner: "user1".to_string(),
            assets: vec![],
            balance: 0.0,
            wallet_type: WalletType::Custodial,
            created_at: 0,
            updated_at: 0,
        };
        
        core.create_wallet(wallet).unwrap();
        
        // Add asset to wallet
        let result = core.add_asset_to_wallet("wallet1", "asset1");
        assert!(result.is_ok());
        
        // Check that asset is in wallet
        let wallet = core.get_wallet("wallet1").unwrap().unwrap();
        assert!(wallet.assets.contains(&"asset1".to_string()));
        assert_eq!(wallet.balance, 100.0);
    }
}