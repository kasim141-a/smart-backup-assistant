"""
Configuration Manager
Handles add-on configuration storage and retrieval
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manager for add-on configuration"""
    
    # Default configuration
    DEFAULT_CONFIG = {
        'auto_backup': True,
        'backup_schedule': 'daily',
        'backup_retention': 7,
        'notifications_enabled': True,
        'debug_mode': False,
        'validate_before_restore': True,
        'compression_enabled': True
    }
    
    def __init__(self, config_path: str = '/data/config.json'):
        """
        Initialize the Configuration Manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing config or create default
        if not self.config_path.exists():
            self._save_config(self.DEFAULT_CONFIG)
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get current configuration
        
        Returns:
            Configuration dictionary
        """
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            merged_config = self.DEFAULT_CONFIG.copy()
            merged_config.update(config)
            
            return merged_config
            
        except FileNotFoundError:
            logger.warning("Config file not found, returning defaults")
            return self.DEFAULT_CONFIG.copy()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config file: {str(e)}")
            return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error reading config: {str(e)}")
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """
        Save configuration
        
        Args:
            config: Configuration dictionary to save
        """
        try:
            # Validate config
            validated_config = self._validate_config(config)
            
            # Save to file
            self._save_config(validated_config)
            
            logger.info("Configuration saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
            raise
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """
        Update specific configuration values
        
        Args:
            updates: Dictionary of values to update
        """
        try:
            # Get current config
            config = self.get_config()
            
            # Update with new values
            config.update(updates)
            
            # Save updated config
            self.save_config(config)
            
        except Exception as e:
            logger.error(f"Error updating config: {str(e)}")
            raise
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values"""
        try:
            self._save_config(self.DEFAULT_CONFIG)
            logger.info("Configuration reset to defaults")
            
        except Exception as e:
            logger.error(f"Error resetting config: {str(e)}")
            raise
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get a specific configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        config = self.get_config()
        return config.get(key, default)
    
    def set_value(self, key: str, value: Any) -> None:
        """
        Set a specific configuration value
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.update_config({key: value})
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """
        Save configuration to file
        
        Args:
            config: Configuration dictionary
        """
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize configuration
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            Validated configuration dictionary
        """
        validated = {}
        
        # Validate auto_backup
        validated['auto_backup'] = bool(config.get('auto_backup', True))
        
        # Validate backup_schedule
        valid_schedules = ['hourly', 'daily', 'weekly', 'monthly']
        schedule = config.get('backup_schedule', 'daily')
        validated['backup_schedule'] = schedule if schedule in valid_schedules else 'daily'
        
        # Validate backup_retention (1-365 days)
        retention = config.get('backup_retention', 7)
        try:
            retention = int(retention)
            validated['backup_retention'] = max(1, min(365, retention))
        except (ValueError, TypeError):
            validated['backup_retention'] = 7
        
        # Validate notifications_enabled
        validated['notifications_enabled'] = bool(config.get('notifications_enabled', True))
        
        # Validate debug_mode
        validated['debug_mode'] = bool(config.get('debug_mode', False))
        
        # Validate validate_before_restore
        validated['validate_before_restore'] = bool(config.get('validate_before_restore', True))
        
        # Validate compression_enabled
        validated['compression_enabled'] = bool(config.get('compression_enabled', True))
        
        return validated
    
    def export_config(self) -> str:
        """
        Export configuration as JSON string
        
        Returns:
            JSON string of configuration
        """
        config = self.get_config()
        return json.dumps(config, indent=2)
    
    def import_config(self, config_json: str) -> None:
        """
        Import configuration from JSON string
        
        Args:
            config_json: JSON string containing configuration
        """
        try:
            config = json.loads(config_json)
            self.save_config(config)
            logger.info("Configuration imported successfully")
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {str(e)}")
            raise ValueError("Invalid configuration JSON")
        except Exception as e:
            logger.error(f"Error importing config: {str(e)}")
            raise

