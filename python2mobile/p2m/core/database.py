"""
P2M Local Database - Persistent storage for P2M applications
Supports key-value storage with JSON serialization
"""

import json
from typing import Dict, Any, Optional, List, Union
from abc import ABC, abstractmethod


class Database(ABC):
    """Abstract base class for database implementations"""
    
    @abstractmethod
    async def set(self, key: str, value: Any) -> bool:
        """Set a value in the database"""
        pass
    
    @abstractmethod
    async def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the database"""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete a value from the database"""
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        """Clear all data from the database"""
        pass
    
    @abstractmethod
    async def keys(self) -> List[str]:
        """Get all keys in the database"""
        pass
    
    @abstractmethod
    async def has(self, key: str) -> bool:
        """Check if a key exists in the database"""
        pass


class LocalDatabase(Database):
    """In-memory database implementation (for testing)"""
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
    
    async def set(self, key: str, value: Any) -> bool:
        """Set a value in the database"""
        try:
            # Serialize to JSON to ensure compatibility
            if isinstance(value, (dict, list)):
                self._data[key] = json.dumps(value)
            else:
                self._data[key] = str(value)
            return True
        except Exception as e:
            print(f"Error setting key {key}: {e}")
            return False
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the database"""
        try:
            value = self._data.get(key, default)
            if value is None:
                return default
            
            # Try to deserialize JSON
            try:
                return json.loads(value)
            except:
                return value
        except Exception as e:
            print(f"Error getting key {key}: {e}")
            return default
    
    async def delete(self, key: str) -> bool:
        """Delete a value from the database"""
        try:
            if key in self._data:
                del self._data[key]
                return True
            return False
        except Exception as e:
            print(f"Error deleting key {key}: {e}")
            return False
    
    async def clear(self) -> bool:
        """Clear all data from the database"""
        try:
            self._data.clear()
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
    
    async def keys(self) -> List[str]:
        """Get all keys in the database"""
        return list(self._data.keys())
    
    async def has(self, key: str) -> bool:
        """Check if a key exists in the database"""
        return key in self._data


class Table:
    """Represents a table in the database"""
    
    def __init__(self, name: str, db: Database):
        self.name = name
        self.db = db
    
    def _make_key(self, item_id: Union[str, int]) -> str:
        """Create a table-scoped key"""
        return f"{self.name}:{item_id}"
    
    async def insert(self, item_id: Union[str, int], data: Dict[str, Any]) -> bool:
        """Insert an item into the table"""
        key = self._make_key(item_id)
        return await self.db.set(key, data)
    
    async def get(self, item_id: Union[str, int], default: Any = None) -> Any:
        """Get an item from the table"""
        key = self._make_key(item_id)
        return await self.db.get(key, default)
    
    async def update(self, item_id: Union[str, int], data: Dict[str, Any]) -> bool:
        """Update an item in the table"""
        key = self._make_key(item_id)
        existing = await self.db.get(key, {})
        
        if isinstance(existing, dict):
            existing.update(data)
            return await self.db.set(key, existing)
        
        return await self.db.set(key, data)
    
    async def delete(self, item_id: Union[str, int]) -> bool:
        """Delete an item from the table"""
        key = self._make_key(item_id)
        return await self.db.delete(key)
    
    async def all(self) -> List[Dict[str, Any]]:
        """Get all items from the table"""
        items = []
        all_keys = await self.db.keys()
        
        for key in all_keys:
            if key.startswith(f"{self.name}:"):
                item = await self.db.get(key)
                if isinstance(item, dict):
                    items.append(item)
        
        return items
    
    async def clear(self) -> bool:
        """Clear all items from the table"""
        all_keys = await self.db.keys()
        
        for key in all_keys:
            if key.startswith(f"{self.name}:"):
                await self.db.delete(key)
        
        return True


# Global database instance
_database: Optional[Database] = None


def init_database(db: Optional[Database] = None) -> Database:
    """Initialize global database"""
    global _database
    _database = db or LocalDatabase()
    return _database


def get_database() -> Database:
    """Get global database"""
    global _database
    if _database is None:
        _database = LocalDatabase()
    return _database


def get_table(name: str) -> Table:
    """Get a table from the global database"""
    db = get_database()
    return Table(name, db)
