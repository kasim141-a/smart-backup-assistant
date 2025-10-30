"""
Home Assistant Supervisor API Client
Handles communication with the Supervisor API
"""

import os
import logging
import requests
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class SupervisorAPI:
    """Client for interacting with Home Assistant Supervisor API"""
    
    def __init__(self):
        """Initialize the Supervisor API client"""
        self.base_url = os.environ.get('SUPERVISOR_URL', 'http://supervisor')
        self.token = os.environ.get('SUPERVISOR_TOKEN', '')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        if not self.token:
            logger.warning("SUPERVISOR_TOKEN not found in environment")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Make a request to the Supervisor API
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint (without base URL)
            data: Optional data to send with request
            
        Returns:
            Response data as dictionary
            
        Raises:
            requests.exceptions.RequestException: If request fails
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            logger.debug(f"Making {method} request to {url}")
            
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            response.raise_for_status()
            
            if response.text:
                return response.json()
            return {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise
    
    # ========================================================================
    # Home Assistant Endpoints
    # ========================================================================
    
    def get_homeassistant_info(self) -> Dict:
        """Get Home Assistant information"""
        return self._make_request('GET', 'core/info')
    
    def restart_homeassistant(self) -> Dict:
        """Restart Home Assistant"""
        return self._make_request('POST', 'core/restart')
    
    def stop_homeassistant(self) -> Dict:
        """Stop Home Assistant"""
        return self._make_request('POST', 'core/stop')
    
    def update_homeassistant(self) -> Dict:
        """Update Home Assistant to latest version"""
        return self._make_request('POST', 'core/update')
    
    # ========================================================================
    # Supervisor Endpoints
    # ========================================================================
    
    def get_supervisor_info(self) -> Dict:
        """Get Supervisor information"""
        return self._make_request('GET', 'supervisor/info')
    
    def get_supervisor_logs(self) -> str:
        """Get Supervisor logs"""
        response = self._make_request('GET', 'supervisor/logs')
        return response.get('data', '')
    
    # ========================================================================
    # Backup Endpoints
    # ========================================================================
    
    def get_backups(self) -> List[Dict]:
        """
        Get list of all backups
        
        Returns:
            List of backup information dictionaries
        """
        response = self._make_request('GET', 'backups')
        return response.get('data', {}).get('backups', [])
    
    def get_backup_info(self, backup_id: str) -> Dict:
        """
        Get information about a specific backup
        
        Args:
            backup_id: The backup slug/ID
            
        Returns:
            Backup information dictionary
        """
        response = self._make_request('GET', f'backups/{backup_id}/info')
        return response.get('data', {})
    
    def create_backup(self, name: str, password: Optional[str] = None, 
                     compressed: bool = True) -> Dict:
        """
        Create a new full backup
        
        Args:
            name: Name for the backup
            password: Optional password to encrypt the backup
            compressed: Whether to compress the backup
            
        Returns:
            Backup creation response
        """
        data = {
            'name': name,
            'compressed': compressed
        }
        
        if password:
            data['password'] = password
        
        return self._make_request('POST', 'backups/new/full', data)
    
    def create_partial_backup(self, name: str, addons: Optional[List[str]] = None,
                            folders: Optional[List[str]] = None,
                            password: Optional[str] = None) -> Dict:
        """
        Create a partial backup
        
        Args:
            name: Name for the backup
            addons: List of addon slugs to include
            folders: List of folders to include
            password: Optional password to encrypt the backup
            
        Returns:
            Backup creation response
        """
        data = {
            'name': name,
            'addons': addons or [],
            'folders': folders or []
        }
        
        if password:
            data['password'] = password
        
        return self._make_request('POST', 'backups/new/partial', data)
    
    def restore_backup(self, backup_id: str, password: Optional[str] = None) -> Dict:
        """
        Restore from a backup
        
        Args:
            backup_id: The backup slug/ID to restore
            password: Password if backup is encrypted
            
        Returns:
            Restore response
        """
        data = {}
        if password:
            data['password'] = password
        
        return self._make_request('POST', f'backups/{backup_id}/restore/full', data)
    
    def restore_partial_backup(self, backup_id: str, 
                              homeassistant: bool = True,
                              addons: Optional[List[str]] = None,
                              folders: Optional[List[str]] = None,
                              password: Optional[str] = None) -> Dict:
        """
        Restore partial backup
        
        Args:
            backup_id: The backup slug/ID to restore
            homeassistant: Whether to restore Home Assistant
            addons: List of addon slugs to restore
            folders: List of folders to restore
            password: Password if backup is encrypted
            
        Returns:
            Restore response
        """
        data = {
            'homeassistant': homeassistant,
            'addons': addons or [],
            'folders': folders or []
        }
        
        if password:
            data['password'] = password
        
        return self._make_request('POST', f'backups/{backup_id}/restore/partial', data)
    
    def delete_backup(self, backup_id: str) -> Dict:
        """
        Delete a backup
        
        Args:
            backup_id: The backup slug/ID to delete
            
        Returns:
            Delete response
        """
        return self._make_request('DELETE', f'backups/{backup_id}')
    
    def download_backup(self, backup_id: str) -> bytes:
        """
        Download a backup file
        
        Args:
            backup_id: The backup slug/ID to download
            
        Returns:
            Backup file content as bytes
        """
        url = f"{self.base_url}/backups/{backup_id}/download"
        
        response = requests.get(
            url,
            headers=self.headers,
            timeout=300  # 5 minutes for large backups
        )
        
        response.raise_for_status()
        return response.content
    
    # ========================================================================
    # System Endpoints
    # ========================================================================
    
    def get_system_info(self) -> Dict:
        """Get system information"""
        response = self._make_request('GET', 'os/info')
        return response.get('data', {})
    
    def get_host_info(self) -> Dict:
        """Get host information"""
        response = self._make_request('GET', 'host/info')
        return response.get('data', {})
    
    def get_storage_info(self) -> Dict:
        """Get storage information"""
        response = self._make_request('GET', 'supervisor/info')
        data = response.get('data', {})
        
        return {
            'used': data.get('disk_used', 0),
            'total': data.get('disk_total', 0),
            'free': data.get('disk_free', 0),
            'percentage': round((data.get('disk_used', 0) / data.get('disk_total', 1)) * 100, 2)
        }
    
    # ========================================================================
    # Add-on Endpoints
    # ========================================================================
    
    def get_addons(self) -> List[Dict]:
        """Get list of installed add-ons"""
        response = self._make_request('GET', 'addons')
        return response.get('data', {}).get('addons', [])
    
    def get_addon_info(self, addon_slug: str) -> Dict:
        """
        Get information about a specific add-on
        
        Args:
            addon_slug: The add-on slug
            
        Returns:
            Add-on information dictionary
        """
        response = self._make_request('GET', f'addons/{addon_slug}/info')
        return response.get('data', {})
    
    def start_addon(self, addon_slug: str) -> Dict:
        """Start an add-on"""
        return self._make_request('POST', f'addons/{addon_slug}/start')
    
    def stop_addon(self, addon_slug: str) -> Dict:
        """Stop an add-on"""
        return self._make_request('POST', f'addons/{addon_slug}/stop')
    
    def restart_addon(self, addon_slug: str) -> Dict:
        """Restart an add-on"""
        return self._make_request('POST', f'addons/{addon_slug}/restart')
    
    # ========================================================================
    # Network Endpoints
    # ========================================================================
    
    def get_network_info(self) -> Dict:
        """Get network information"""
        response = self._make_request('GET', 'network/info')
        return response.get('data', {})
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def ping(self) -> bool:
        """
        Check if Supervisor API is accessible
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            self.get_supervisor_info()
            return True
        except Exception as e:
            logger.error(f"Supervisor API ping failed: {str(e)}")
            return False

