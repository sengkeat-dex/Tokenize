use rusqlite::{Connection, Result, params, Row};
use crate::models::{TokenizationComponent, NewTokenizationComponent};

pub struct Database {
    conn: Connection,
}

impl Database {
    pub fn new(db_path: &str) -> Result<Self> {
        let conn = Connection::open(db_path)?;
        Ok(Database { conn })
    }
    
    pub fn init(&self) -> Result<()> {
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS tokenization_components (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                main_type TEXT NOT NULL,
                sub_type TEXT NOT NULL,
                components TEXT NOT NULL
            )",
            [],
        )?;
        
        Ok(())
    }
    
    pub fn insert_component(&self, component: &NewTokenizationComponent) -> Result<i32> {
        self.conn.execute(
            "INSERT INTO tokenization_components (main_type, sub_type, components) VALUES (?1, ?2, ?3)",
            params![component.main_type, component.sub_type, component.components],
        )?;
        
        let id = self.conn.last_insert_rowid() as i32;
        Ok(id)
    }
    
    pub fn get_all_components(&self) -> Result<Vec<TokenizationComponent>> {
        let mut stmt = self.conn.prepare(
            "SELECT id, main_type, sub_type, components FROM tokenization_components"
        )?;
        
        let components = stmt.query_map([], |row| {
            Ok(TokenizationComponent {
                id: row.get(0)?,
                main_type: row.get(1)?,
                sub_type: row.get(2)?,
                components: row.get(3)?,
            })
        })?;
        
        let mut result = Vec::new();
        for component in components {
            result.push(component?);
        }
        
        Ok(result)
    }
    
    pub fn get_components_by_type(&self, main_type: &str) -> Result<Vec<TokenizationComponent>> {
        let mut stmt = self.conn.prepare(
            "SELECT id, main_type, sub_type, components FROM tokenization_components WHERE main_type = ?1"
        )?;
        
        let components = stmt.query_map(params![main_type], |row| {
            Ok(TokenizationComponent {
                id: row.get(0)?,
                main_type: row.get(1)?,
                sub_type: row.get(2)?,
                components: row.get(3)?,
            })
        })?;
        
        let mut result = Vec::new();
        for component in components {
            result.push(component?);
        }
        
        Ok(result)
    }
    
    pub fn get_components_by_subtype(&self, main_type: &str, sub_type: &str) -> Result<Vec<TokenizationComponent>> {
        let mut stmt = self.conn.prepare(
            "SELECT id, main_type, sub_type, components FROM tokenization_components WHERE main_type = ?1 AND sub_type = ?2"
        )?;
        
        let components = stmt.query_map(params![main_type, sub_type], |row| {
            Ok(TokenizationComponent {
                id: row.get(0)?,
                main_type: row.get(1)?,
                sub_type: row.get(2)?,
                components: row.get(3)?,
            })
        })?;
        
        let mut result = Vec::new();
        for component in components {
            result.push(component?);
        }
        
        Ok(result)
    }
}