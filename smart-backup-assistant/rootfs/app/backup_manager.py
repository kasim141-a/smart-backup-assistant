"""
Backup Manager
Handles backup operations, validation, and analysis
"""

import logging
import tarfile
import json
import tempfile
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

from backup_analyzer import BackupAnalyzer
from breaking_changes import BreakingChangesDB

logger = logging.getLogger(__name__)


class BackupManager:
    """Manager for backup operations"""
    
    def __init__(self, supervisor_api):
        """
        Initialize the Backup Manager
        
        Args:
            supervisor_api: SupervisorAPI instance
        """
        self.supervisor_api = supervisor_api
        self.backup_analyzer = BackupAnalyzer()
        self.breaking_changes_db = BreakingChangesDB()
    
    def get_backups(self) -> List[Dict]:
        """
        Get list of all backups with formatted information
        
        Returns:
            List of backup dictionaries with formatted data
        """
        try:
            backups = self.supervisor_api.get_backups()
            
            # Format backup information
            formatted_backups = []
            for backup in backups:
                formatted_backups.append({
                    'id': backup.get('slug'),
                    'name': backup.get('name'),
                    'date': backup.get('date'),
                    'size': self._format_size(backup.get('size', 0)),
                    'size_bytes': backup.get('size', 0),
                    'type': backup.get('type'),
                    'protected': backup.get('protected', False),
                    'compressed': backup.get('compressed', True)
                })
            
            # Sort by date (newest first)
            formatted_backups.sort(
                key=lambda x: x.get('date', ''),
                reverse=True
            )
            
            return formatted_backups
            
        except Exception as e:
            logger.error(f"Error getting backups: {str(e)}")
            raise
    
    def get_backup_details(self, backup_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific backup
        
        Args:
            backup_id: The backup slug/ID
            
        Returns:
            Backup details dictionary or None if not found
        """
        try:
            backup_info = self.supervisor_api.get_backup_info(backup_id)
            
            if not backup_info:
                return None
            
            # Extract detailed information
            details = {
                'id': backup_info.get('slug'),
                'name': backup_info.get('name'),
                'date': backup_info.get('date'),
                'size': self._format_size(backup_info.get('size', 0)),
                'size_bytes': backup_info.get('size', 0),
                'type': backup_info.get('type'),
                'protected': backup_info.get('protected', False),
                'compressed': backup_info.get('compressed', True),
                'homeassistant': backup_info.get('homeassistant'),
                'addons': backup_info.get('addons', []),
                'folders': backup_info.get('folders', []),
                'repositories': backup_info.get('repositories', [])
            }
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting backup details: {str(e)}")
            raise
    
    def create_backup(self, name: str, password: Optional[str] = None) -> Dict:
        """
        Create a new full backup
        
        Args:
            name: Name for the backup
            password: Optional password to encrypt the backup
            
        Returns:
            Backup creation result
        """
        try:
            logger.info(f"Creating backup: {name}")
            result = self.supervisor_api.create_backup(name, password)
            
            return {
                'backup_id': result.get('data', {}).get('slug'),
                'message': 'Backup created successfully',
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            raise
    
    def validate_backup(self, backup_id: str) -> Dict:
        """
        Validate a backup before restoration using advanced analysis
        
        Args:
            backup_id: The backup slug/ID to validate
            
        Returns:
            Validation result with compatibility information and breaking changes
        """
        try:
            logger.info(f"Validating backup: {backup_id}")
            
            # Step 1: Download backup file
            logger.info("Downloading backup file...")
            backup_data = self.supervisor_api.download_backup(backup_id)
            
            # Step 2: Analyze backup contents
            logger.info("Analyzing backup contents...")
            analysis = self.backup_analyzer.analyze_backup(backup_data)
            
            if not analysis.get('success'):
                return {
                    'backup_id': backup_id,
                    'status': 'error',
                    'risk_level': 'unknown',
                    'error': analysis.get('error', 'Failed to analyze backup'),
                    'timestamp': datetime.utcnow().isoformat()
                }
            
            # Step 3: Get current system version
            current_ha_info = self.supervisor_api.get_homeassistant_info()
            current_version = current_ha_info.get('data', {}).get('version', 'Unknown')
            
            backup_version = analysis.get('homeassistant_version', 'Unknown')
            
            # Step 4: Compare versions
            logger.info(f"Comparing versions: {backup_version} → {current_version}")
            version_comparison = self.backup_analyzer.compare_versions(
                backup_version,
                current_version
            )
            
            # Step 5: Find breaking changes
            logger.info("Checking for breaking changes...")
            integrations = analysis.get('integrations', [])
            breaking_changes = self.breaking_changes_db.find_breaking_changes(
                backup_version,
                current_version,
                integrations
            )
            
            # Step 6: Assess risk
            logger.info("Assessing risk level...")
            risk_assessment = self.breaking_changes_db.assess_risk(breaking_changes)
            
            # Step 7: Generate validation report
            issues = []
            warnings = []
            
            # Version compatibility issues
            if not version_comparison.get('compatible'):
                if version_comparison.get('version_diff') == 'newer':
                    issues.append({
                        'type': 'version',
                        'severity': 'high',
                        'message': f"Backup is from a newer version ({backup_version}) than current ({current_version}). Restoration not recommended."
                    })
                elif version_comparison.get('total_months_diff', 0) > 6:
                    warnings.append({
                        'type': 'version',
                        'severity': 'medium',
                        'message': f"Backup is {version_comparison.get('total_months_diff')} months old. Significant changes may have occurred."
                    })
            
            # Breaking changes warnings
            if breaking_changes:
                for change in breaking_changes:
                    severity = change.get('severity', 'medium')
                    if severity == 'high':
                        issues.append({
                            'type': 'breaking_change',
                            'severity': 'high',
                            'integration': change.get('integration'),
                            'message': change.get('title'),
                            'description': change.get('description'),
                            'url': change.get('url')
                        })
                    else:
                        warnings.append({
                            'type': 'breaking_change',
                            'severity': severity,
                            'integration': change.get('integration'),
                            'message': change.get('title'),
                            'description': change.get('description'),
                            'url': change.get('url')
                        })
            
            # Determine overall status
            if issues:
                status = 'incompatible'
                risk_level = 'high'
            elif risk_assessment.get('level') == 'high':
                status = 'compatible_with_warnings'
                risk_level = 'high'
            elif warnings or risk_assessment.get('level') == 'medium':
                status = 'compatible_with_warnings'
                risk_level = 'medium'
            else:
                status = 'compatible'
                risk_level = 'low'
            
            return {
                'backup_id': backup_id,
                'status': status,
                'risk_level': risk_level,
                'backup_info': {
                    'name': analysis.get('backup_name'),
                    'date': analysis.get('backup_date'),
                    'type': analysis.get('backup_type'),
                    'size': self._format_size(analysis.get('backup_size', 0))
                },
                'version_info': {
                    'backup_version': backup_version,
                    'current_version': current_version,
                    'compatible': version_comparison.get('compatible'),
                    'version_diff': version_comparison.get('version_diff'),
                    'months_difference': version_comparison.get('total_months_diff', 0)
                },
                'integrations': {
                    'count': analysis.get('integration_count', 0),
                    'list': integrations[:20]  # Limit to first 20 for display
                },
                'addons': {
                    'count': analysis.get('addon_count', 0),
                    'list': [addon.get('name') for addon in analysis.get('addons', [])][:10]
                },
                'breaking_changes': {
                    'count': len(breaking_changes),
                    'risk_score': risk_assessment.get('score', 0),
                    'risk_message': risk_assessment.get('message'),
                    'changes': breaking_changes
                },
                'issues': issues,
                'warnings': warnings,
                'recommendation': self._generate_recommendation(status, risk_level, issues, warnings),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error validating backup: {str(e)}")
            return {
                'backup_id': backup_id,
                'status': 'error',
                'risk_level': 'unknown',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _generate_recommendation(self, status: str, risk_level: str, 
                                issues: List[Dict], warnings: List[Dict]) -> str:
        """Generate a user-friendly recommendation based on validation results"""
        if status == 'incompatible':
            return "⚠️ Restoration not recommended. Critical compatibility issues detected. Please review the issues carefully before proceeding."
        elif risk_level == 'high':
            return "⚠️ Proceed with caution. Significant breaking changes detected that may affect your system. Review all warnings before restoring."
        elif risk_level == 'medium':
            return "ℹ️ Restoration should be safe, but some minor issues were detected. Review the warnings and be prepared to reconfigure affected integrations."
        else:
            return "✅ Backup appears safe to restore. No significant compatibility issues detected."


    def restore_backup(self, backup_id: str, password: Optional[str] = None) -> Dict:
        """
        Restore from a backup
        
        Args:
            backup_id: The backup slug/ID to restore
            password: Password if backup is encrypted
            
        Returns:
            Restore result
        """
        try:
            logger.info(f"Restoring backup: {backup_id}")
            
            # Validate first
            validation = self.validate_backup(backup_id)
            
            if validation['status'] == 'incompatible':
                logger.warning(f"Restoring incompatible backup: {backup_id}")
            
            # Perform restore
            result = self.supervisor_api.restore_backup(backup_id, password)
            
            return {
                'backup_id': backup_id,
                'message': 'Backup restore initiated',
                'validation': validation,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error restoring backup: {str(e)}")
            raise
    
    def delete_backup(self, backup_id: str) -> None:
        """
        Delete a backup
        
        Args:
            backup_id: The backup slug/ID to delete
        """
        try:
            logger.info(f"Deleting backup: {backup_id}")
            self.supervisor_api.delete_backup(backup_id)
            
        except Exception as e:
            logger.error(f"Error deleting backup: {str(e)}")
            raise
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _format_size(self, size_bytes: int) -> str:
        """
        Format size in bytes to human-readable format
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string (e.g., "2.5 GB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def _check_version_compatibility(self, backup_version: str, 
                                    current_version: str) -> Dict:
        """
        Check version compatibility between backup and current system
        
        Args:
            backup_version: Version from backup
            current_version: Current system version
            
        Returns:
            Compatibility information dictionary
        """
        try:
            # Parse versions
            backup_parts = self._parse_version(backup_version)
            current_parts = self._parse_version(current_version)
            
            if not backup_parts or not current_parts:
                return {
                    'status': 'unknown',
                    'message': 'Unable to parse version numbers'
                }
            
            # Compare major versions
            if backup_parts[0] != current_parts[0]:
                return {
                    'status': 'incompatible',
                    'message': 'Major version mismatch',
                    'backup_major': backup_parts[0],
                    'current_major': current_parts[0]
                }
            
            # Compare minor versions
            if abs(backup_parts[1] - current_parts[1]) > 2:
                return {
                    'status': 'warning',
                    'message': 'Significant minor version difference',
                    'backup_minor': backup_parts[1],
                    'current_minor': current_parts[1]
                }
            
            # Versions are compatible
            return {
                'status': 'compatible',
                'message': 'Versions are compatible'
            }
            
        except Exception as e:
            logger.error(f"Error checking version compatibility: {str(e)}")
            return {
                'status': 'unknown',
                'message': f'Error checking compatibility: {str(e)}'
            }
    
    def _parse_version(self, version_string: str) -> Optional[tuple]:
        """
        Parse version string into components
        
        Args:
            version_string: Version string (e.g., "2024.10.1")
            
        Returns:
            Tuple of (major, minor, patch) or None if parsing fails
        """
        try:
            # Remove any non-numeric prefixes
            version_string = version_string.lstrip('v')
            
            # Split by dots
            parts = version_string.split('.')
            
            if len(parts) >= 2:
                major = int(parts[0])
                minor = int(parts[1])
                patch = int(parts[2]) if len(parts) > 2 else 0
                return (major, minor, patch)
            
            return None
            
        except (ValueError, IndexError):
            logger.warning(f"Failed to parse version: {version_string}")
            return None

