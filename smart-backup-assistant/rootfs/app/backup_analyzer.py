"""
Backup Analyzer
Extracts and analyzes Home Assistant backup files
"""

import os
import json
import tarfile
import tempfile
import logging
from typing import Dict, List, Optional
from io import BytesIO

logger = logging.getLogger(__name__)


class BackupAnalyzer:
    """Analyzes Home Assistant backup files"""
    
    def __init__(self):
        """Initialize the backup analyzer"""
        self.temp_dir = tempfile.gettempdir()
    
    def analyze_backup(self, backup_data: bytes) -> Dict:
        """
        Analyze a backup file and extract key information
        
        Args:
            backup_data: The backup file content as bytes
            
        Returns:
            Dictionary containing backup analysis results
        """
        try:
            logger.info("Starting backup analysis...")
            
            # Extract manifest from backup
            manifest = self._extract_manifest(backup_data)
            
            if not manifest:
                logger.error("Failed to extract manifest from backup")
                return {
                    'success': False,
                    'error': 'Could not extract manifest from backup file'
                }
            
            # Parse manifest
            analysis = self._parse_manifest(manifest)
            
            logger.info(f"Backup analysis complete: {analysis.get('homeassistant_version', 'unknown')}")
            
            return {
                'success': True,
                **analysis
            }
            
        except Exception as e:
            logger.error(f"Backup analysis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_manifest(self, backup_data: bytes) -> Optional[Dict]:
        """
        Extract manifest.json from backup tar file
        
        Args:
            backup_data: The backup file content as bytes
            
        Returns:
            Manifest dictionary or None if extraction fails
        """
        try:
            # Create BytesIO object from backup data
            backup_file = BytesIO(backup_data)
            
            # Open as tar file
            with tarfile.open(fileobj=backup_file, mode='r:*') as tar:
                # Look for manifest.json
                for member in tar.getmembers():
                    if member.name.endswith('manifest.json') or member.name == 'manifest.json':
                        logger.debug(f"Found manifest: {member.name}")
                        
                        # Extract and parse manifest
                        manifest_file = tar.extractfile(member)
                        if manifest_file:
                            manifest_content = manifest_file.read()
                            return json.loads(manifest_content)
                
                logger.warning("manifest.json not found in backup")
                return None
                
        except tarfile.TarError as e:
            logger.error(f"Failed to open backup as tar file: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse manifest JSON: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error extracting manifest: {str(e)}")
            return None
    
    def _parse_manifest(self, manifest: Dict) -> Dict:
        """
        Parse manifest and extract relevant information
        
        Args:
            manifest: The manifest dictionary
            
        Returns:
            Parsed backup information
        """
        # Extract version information
        homeassistant_version = manifest.get('homeassistant', 'unknown')
        supervisor_version = manifest.get('supervisor', 'unknown')
        
        # Extract backup metadata
        backup_name = manifest.get('name', 'Unknown')
        backup_date = manifest.get('date', 'unknown')
        backup_type = manifest.get('type', 'unknown')
        backup_size = manifest.get('size', 0)
        
        # Extract addon information
        addons = manifest.get('addons', [])
        addon_list = []
        for addon in addons:
            if isinstance(addon, dict):
                addon_list.append({
                    'name': addon.get('name', 'unknown'),
                    'slug': addon.get('slug', 'unknown'),
                    'version': addon.get('version', 'unknown')
                })
            else:
                addon_list.append({'slug': str(addon)})
        
        # Extract folder information
        folders = manifest.get('folders', [])
        
        # Extract integration information from homeassistant.json if available
        integrations = self._extract_integrations(manifest)
        
        return {
            'homeassistant_version': homeassistant_version,
            'supervisor_version': supervisor_version,
            'backup_name': backup_name,
            'backup_date': backup_date,
            'backup_type': backup_type,
            'backup_size': backup_size,
            'addons': addon_list,
            'folders': folders,
            'integrations': integrations,
            'addon_count': len(addon_list),
            'integration_count': len(integrations)
        }
    
    def _extract_integrations(self, manifest: Dict) -> List[str]:
        """
        Extract list of integrations from manifest
        
        Args:
            manifest: The manifest dictionary
            
        Returns:
            List of integration domain names
        """
        integrations = []
        
        # Try to get from homeassistant section
        ha_data = manifest.get('homeassistant_data', {})
        if isinstance(ha_data, dict):
            # Look for integrations in various possible locations
            if 'integrations' in ha_data:
                integrations = ha_data['integrations']
            elif 'components' in ha_data:
                integrations = ha_data['components']
        
        # If no integrations found, try to infer from addons
        if not integrations and 'addons' in manifest:
            # Some common addon -> integration mappings
            addon_integration_map = {
                'mosquitto': 'mqtt',
                'mariadb': 'mysql',
                'influxdb': 'influxdb',
                'grafana': 'grafana',
                'node-red': 'node_red',
                'esphome': 'esphome',
                'zigbee2mqtt': 'mqtt'
            }
            
            for addon in manifest['addons']:
                addon_slug = addon.get('slug', '') if isinstance(addon, dict) else str(addon)
                if addon_slug in addon_integration_map:
                    integrations.append(addon_integration_map[addon_slug])
        
        # Always include some core integrations
        core_integrations = ['homeassistant', 'default_config', 'system_health']
        for core in core_integrations:
            if core not in integrations:
                integrations.append(core)
        
        return sorted(list(set(integrations)))
    
    def compare_versions(self, backup_version: str, current_version: str) -> Dict:
        """
        Compare backup version with current version
        
        Args:
            backup_version: Version from backup
            current_version: Current Home Assistant version
            
        Returns:
            Comparison result dictionary
        """
        try:
            # Parse versions
            backup_parts = self._parse_version(backup_version)
            current_parts = self._parse_version(current_version)
            
            if not backup_parts or not current_parts:
                return {
                    'compatible': False,
                    'reason': 'Could not parse version numbers',
                    'backup_version': backup_version,
                    'current_version': current_version
                }
            
            # Compare versions
            if backup_parts['year'] < current_parts['year']:
                version_diff = 'older'
            elif backup_parts['year'] > current_parts['year']:
                version_diff = 'newer'
            elif backup_parts['month'] < current_parts['month']:
                version_diff = 'older'
            elif backup_parts['month'] > current_parts['month']:
                version_diff = 'newer'
            elif backup_parts['patch'] < current_parts['patch']:
                version_diff = 'older'
            elif backup_parts['patch'] > current_parts['patch']:
                version_diff = 'newer'
            else:
                version_diff = 'same'
            
            # Determine compatibility
            # Generally, restoring older backups is safer than newer ones
            compatible = version_diff in ['same', 'older']
            
            # Calculate version distance
            year_diff = abs(current_parts['year'] - backup_parts['year'])
            month_diff = abs(current_parts['month'] - backup_parts['month'])
            
            return {
                'compatible': compatible,
                'version_diff': version_diff,
                'backup_version': backup_version,
                'current_version': current_version,
                'year_diff': year_diff,
                'month_diff': month_diff,
                'total_months_diff': (year_diff * 12) + month_diff
            }
            
        except Exception as e:
            logger.error(f"Version comparison failed: {str(e)}")
            return {
                'compatible': False,
                'reason': f'Version comparison error: {str(e)}',
                'backup_version': backup_version,
                'current_version': current_version
            }
    
    def _parse_version(self, version: str) -> Optional[Dict]:
        """
        Parse Home Assistant version string
        
        Args:
            version: Version string (e.g., "2024.10.1")
            
        Returns:
            Dictionary with version components or None if parsing fails
        """
        try:
            # Remove any prefix (like 'v')
            version = version.lstrip('v')
            
            # Split by dots
            parts = version.split('.')
            
            if len(parts) < 2:
                return None
            
            return {
                'year': int(parts[0]),
                'month': int(parts[1]),
                'patch': int(parts[2]) if len(parts) > 2 else 0
            }
            
        except (ValueError, IndexError) as e:
            logger.error(f"Failed to parse version '{version}': {str(e)}")
            return None

