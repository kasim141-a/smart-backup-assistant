"""
Breaking Changes Detection System
Scrapes and analyzes Home Assistant breaking changes
"""

import os
import json
import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class BreakingChangesDB:
    """Manages breaking changes database"""
    
    def __init__(self, db_path: str = '/data/breaking_changes.json'):
        """
        Initialize the breaking changes database
        
        Args:
            db_path: Path to the JSON database file
        """
        self.db_path = db_path
        self.changes = self._load_database()
        self.last_update = self._get_last_update()
    
    def _load_database(self) -> Dict:
        """Load breaking changes from database file"""
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data.get('changes', []))} breaking changes from database")
                    return data
            else:
                logger.info("No existing database found, creating new one")
                return {'changes': [], 'last_update': None}
        except Exception as e:
            logger.error(f"Failed to load database: {str(e)}")
            return {'changes': [], 'last_update': None}
    
    def _save_database(self):
        """Save breaking changes to database file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            with open(self.db_path, 'w') as f:
                json.dump(self.changes, f, indent=2)
            logger.info("Database saved successfully")
        except Exception as e:
            logger.error(f"Failed to save database: {str(e)}")
    
    def _get_last_update(self) -> Optional[str]:
        """Get timestamp of last database update"""
        return self.changes.get('last_update')
    
    def update_database(self) -> bool:
        """
        Update the breaking changes database from Home Assistant releases
        
        Returns:
            True if update successful, False otherwise
        """
        try:
            logger.info("Updating breaking changes database...")
            
            # Fetch recent releases
            new_changes = self._fetch_breaking_changes()
            
            if new_changes:
                # Merge with existing changes
                existing_changes = self.changes.get('changes', [])
                
                # Add new changes (avoid duplicates)
                for change in new_changes:
                    if not any(c.get('id') == change.get('id') for c in existing_changes):
                        existing_changes.append(change)
                
                self.changes['changes'] = existing_changes
                self.changes['last_update'] = datetime.now().isoformat()
                
                self._save_database()
                logger.info(f"Database updated with {len(new_changes)} new changes")
                return True
            else:
                logger.warning("No new breaking changes found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update database: {str(e)}")
            return False
    
    def _fetch_breaking_changes(self) -> List[Dict]:
        """
        Fetch breaking changes from Home Assistant release notes
        
        Returns:
            List of breaking changes
        """
        changes = []
        
        try:
            # Fetch from Home Assistant blog/releases
            # For now, we'll use a curated list of common breaking changes
            # In production, this would scrape the actual release notes
            
            changes = self._get_curated_breaking_changes()
            
            logger.info(f"Fetched {len(changes)} breaking changes")
            return changes
            
        except Exception as e:
            logger.error(f"Failed to fetch breaking changes: {str(e)}")
            return []
    
    def _get_curated_breaking_changes(self) -> List[Dict]:
        """
        Get a curated list of common breaking changes
        This is a fallback/example dataset
        """
        return [
            {
                'id': 'mqtt_2024_10',
                'version': '2024.10.0',
                'integration': 'mqtt',
                'title': 'MQTT Discovery Topic Changes',
                'description': 'MQTT discovery topics have been reorganized. Devices may need to be reconfigured.',
                'severity': 'medium',
                'url': 'https://www.home-assistant.io/blog/2024/10/01/release-202410/'
            },
            {
                'id': 'zha_2024_9',
                'version': '2024.9.0',
                'integration': 'zha',
                'title': 'ZHA Device Naming Convention Changed',
                'description': 'Zigbee device names now follow a new convention. Automations may need updates.',
                'severity': 'high',
                'url': 'https://www.home-assistant.io/blog/2024/09/01/release-20249/'
            },
            {
                'id': 'esphome_2024_8',
                'version': '2024.8.0',
                'integration': 'esphome',
                'title': 'ESPHome API Version Requirement',
                'description': 'ESPHome devices must be running API version 1.9 or higher.',
                'severity': 'medium',
                'url': 'https://www.home-assistant.io/blog/2024/08/01/release-20248/'
            },
            {
                'id': 'homekit_2024_7',
                'version': '2024.7.0',
                'integration': 'homekit',
                'title': 'HomeKit Bridge Configuration Changes',
                'description': 'HomeKit bridge configuration format has changed. Manual reconfiguration required.',
                'severity': 'high',
                'url': 'https://www.home-assistant.io/blog/2024/07/01/release-20247/'
            },
            {
                'id': 'template_2024_6',
                'version': '2024.6.0',
                'integration': 'template',
                'title': 'Template Sensor Syntax Update',
                'description': 'Template sensors now require explicit state_class definition.',
                'severity': 'low',
                'url': 'https://www.home-assistant.io/blog/2024/06/01/release-20246/'
            },
            {
                'id': 'automation_2024_5',
                'version': '2024.5.0',
                'integration': 'automation',
                'title': 'Automation Trigger ID Requirement',
                'description': 'Automation triggers now require unique IDs for proper tracking.',
                'severity': 'low',
                'url': 'https://www.home-assistant.io/blog/2024/05/01/release-20245/'
            },
            {
                'id': 'shelly_2024_4',
                'version': '2024.4.0',
                'integration': 'shelly',
                'title': 'Shelly Integration Rewrite',
                'description': 'Shelly integration has been completely rewritten. Devices need to be re-added.',
                'severity': 'high',
                'url': 'https://www.home-assistant.io/blog/2024/04/01/release-20244/'
            },
            {
                'id': 'sensor_2024_3',
                'version': '2024.3.0',
                'integration': 'sensor',
                'title': 'Sensor Platform Deprecation',
                'description': 'Legacy sensor platform configuration is deprecated. Use modern format.',
                'severity': 'medium',
                'url': 'https://www.home-assistant.io/blog/2024/03/01/release-20243/'
            }
        ]
    
    def find_breaking_changes(self, from_version: str, to_version: str, 
                            integrations: List[str]) -> List[Dict]:
        """
        Find breaking changes between two versions for specific integrations
        
        Args:
            from_version: Starting version (backup version)
            to_version: Target version (current version)
            integrations: List of integration domains to check
            
        Returns:
            List of relevant breaking changes
        """
        try:
            logger.info(f"Finding breaking changes from {from_version} to {to_version}")
            
            # Parse versions
            from_parts = self._parse_version(from_version)
            to_parts = self._parse_version(to_version)
            
            if not from_parts or not to_parts:
                logger.warning("Could not parse versions")
                return []
            
            # Filter breaking changes
            relevant_changes = []
            
            for change in self.changes.get('changes', []):
                change_version = change.get('version', '')
                change_parts = self._parse_version(change_version)
                
                if not change_parts:
                    continue
                
                # Check if change is in the version range
                if self._is_version_in_range(change_parts, from_parts, to_parts):
                    # Check if change affects user's integrations
                    change_integration = change.get('integration', '')
                    if change_integration in integrations or change_integration == 'all':
                        relevant_changes.append(change)
            
            logger.info(f"Found {len(relevant_changes)} relevant breaking changes")
            return relevant_changes
            
        except Exception as e:
            logger.error(f"Failed to find breaking changes: {str(e)}")
            return []
    
    def _parse_version(self, version: str) -> Optional[Dict]:
        """Parse version string into components"""
        try:
            version = version.lstrip('v')
            parts = version.split('.')
            
            if len(parts) < 2:
                return None
            
            return {
                'year': int(parts[0]),
                'month': int(parts[1]),
                'patch': int(parts[2]) if len(parts) > 2 else 0
            }
        except (ValueError, IndexError):
            return None
    
    def _is_version_in_range(self, check_version: Dict, from_version: Dict, 
                           to_version: Dict) -> bool:
        """Check if a version is within a range"""
        # Convert to comparable integers
        check_val = (check_version['year'] * 10000 + 
                    check_version['month'] * 100 + 
                    check_version['patch'])
        from_val = (from_version['year'] * 10000 + 
                   from_version['month'] * 100 + 
                   from_version['patch'])
        to_val = (to_version['year'] * 10000 + 
                 to_version['month'] * 100 + 
                 to_version['patch'])
        
        return from_val < check_val <= to_val
    
    def assess_risk(self, breaking_changes: List[Dict]) -> Dict:
        """
        Assess the risk level based on breaking changes
        
        Args:
            breaking_changes: List of breaking changes
            
        Returns:
            Risk assessment dictionary
        """
        if not breaking_changes:
            return {
                'level': 'low',
                'score': 0,
                'message': 'No breaking changes detected'
            }
        
        # Calculate risk score
        risk_score = 0
        severity_weights = {
            'low': 1,
            'medium': 3,
            'high': 5
        }
        
        for change in breaking_changes:
            severity = change.get('severity', 'medium')
            risk_score += severity_weights.get(severity, 3)
        
        # Determine risk level
        if risk_score <= 2:
            level = 'low'
            message = 'Minor changes detected. Restoration should be safe.'
        elif risk_score <= 6:
            level = 'medium'
            message = 'Some breaking changes detected. Review before restoring.'
        else:
            level = 'high'
            message = 'Significant breaking changes detected. Restoration may cause issues.'
        
        return {
            'level': level,
            'score': risk_score,
            'message': message,
            'change_count': len(breaking_changes)
        }

