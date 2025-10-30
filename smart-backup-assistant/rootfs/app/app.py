"""
Main Flask application for Material Design Add-on Backend
Provides REST API endpoints for the frontend
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

from supervisor_api import SupervisorAPI
from backup_manager import BackupManager
from config_manager import ConfigManager
from backup_analyzer import BackupAnalyzer
from breaking_changes import BreakingChangesDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize managers
supervisor_api = SupervisorAPI()
backup_manager = BackupManager(supervisor_api)
config_manager = ConfigManager()
backup_analyzer = BackupAnalyzer()
breaking_changes_db = BreakingChangesDB()

# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    try:
        # Get Home Assistant info
        ha_info = supervisor_api.get_homeassistant_info()
        supervisor_info = supervisor_api.get_supervisor_info()
        
        return jsonify({
            'success': True,
            'data': {
                'homeassistant': {
                    'version': ha_info.get('version', 'Unknown'),
                    'state': ha_info.get('state', 'Unknown'),
                    'update_available': ha_info.get('update_available', False)
                },
                'supervisor': {
                    'version': supervisor_info.get('version', 'Unknown'),
                    'healthy': supervisor_info.get('healthy', False)
                },
                'addon': {
                    'status': 'running',
                    'uptime': get_uptime()
                }
            }
        })
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# Configuration Endpoints
# ============================================================================

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    try:
        config = config_manager.get_config()
        return jsonify({
            'success': True,
            'data': config
        })
    except Exception as e:
        logger.error(f"Error getting config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/config', methods=['POST'])
def save_config():
    """Save configuration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Save configuration
        config_manager.save_config(data)
        
        return jsonify({
            'success': True,
            'message': 'Configuration saved successfully'
        })
    except Exception as e:
        logger.error(f"Error saving config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/config/reset', methods=['POST'])
def reset_config():
    """Reset configuration to defaults"""
    try:
        config_manager.reset_to_defaults()
        return jsonify({
            'success': True,
            'message': 'Configuration reset to defaults'
        })
    except Exception as e:
        logger.error(f"Error resetting config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# Backup Endpoints
# ============================================================================

@app.route('/api/backups', methods=['GET'])
def get_backups():
    """Get list of all backups"""
    try:
        backups = backup_manager.get_backups()
        return jsonify({
            'success': True,
            'data': backups
        })
    except Exception as e:
        logger.error(f"Error getting backups: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/backups/<backup_id>', methods=['GET'])
def get_backup_details(backup_id):
    """Get details of a specific backup"""
    try:
        backup = backup_manager.get_backup_details(backup_id)
        if not backup:
            return jsonify({
                'success': False,
                'error': 'Backup not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': backup
        })
    except Exception as e:
        logger.error(f"Error getting backup details: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/backups/create', methods=['POST'])
def create_backup():
    """Create a new backup"""
    try:
        data = request.get_json() or {}
        name = data.get('name', f"Backup {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        logger.info(f"Creating backup: {name}")
        result = backup_manager.create_backup(name)
        
        return jsonify({
            'success': True,
            'message': 'Backup created successfully',
            'data': result
        })
    except Exception as e:
        logger.error(f"Error creating backup: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/backups/<backup_id>/validate', methods=['POST'])
def validate_backup(backup_id):
    """Validate a backup before restoration"""
    try:
        logger.info(f"Validating backup: {backup_id}")
        result = backup_manager.validate_backup(backup_id)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        logger.error(f"Error validating backup: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/backups/<backup_id>/restore', methods=['POST'])
def restore_backup(backup_id):
    """Restore from a backup"""
    try:
        logger.info(f"Restoring backup: {backup_id}")
        result = backup_manager.restore_backup(backup_id)
        
        return jsonify({
            'success': True,
            'message': 'Backup restored successfully',
            'data': result
        })
    except Exception as e:
        logger.error(f"Error restoring backup: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/backups/<backup_id>', methods=['DELETE'])
def delete_backup(backup_id):
    """Delete a backup"""
    try:
        logger.info(f"Deleting backup: {backup_id}")
        backup_manager.delete_backup(backup_id)
        
        return jsonify({
            'success': True,
            'message': 'Backup deleted successfully'
        })
    except Exception as e:
        logger.error(f"Error deleting backup: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# Activity Log Endpoints
# ============================================================================

@app.route('/api/activity', methods=['GET'])
def get_activity_log():
    """Get recent activity log"""
    try:
        limit = request.args.get('limit', 10, type=int)
        activities = get_recent_activities(limit)
        
        return jsonify({
            'success': True,
            'data': activities
        })
    except Exception as e:
        logger.error(f"Error getting activity log: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# System Information Endpoints
# ============================================================================

@app.route('/api/system/info', methods=['GET'])
def get_system_info():
    """Get system information"""
    try:
        info = supervisor_api.get_system_info()
        return jsonify({
            'success': True,
            'data': info
        })
    except Exception as e:
        logger.error(f"Error getting system info: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/system/storage', methods=['GET'])
def get_storage_info():
    """Get storage information"""
    try:
        storage = supervisor_api.get_storage_info()
        return jsonify({
            'success': True,
            'data': storage
        })
    except Exception as e:
        logger.error(f"Error getting storage info: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# Helper Functions
# ============================================================================

def get_uptime():
    """Get application uptime"""
    # In a real implementation, you would track the start time
    return "Running"

def get_recent_activities(limit=10):
    """Get recent activities"""
    # This would typically read from a database or log file
    # For now, return sample data
    return [
        {
            'id': 1,
            'type': 'backup',
            'message': 'Backup completed successfully',
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'success'
        },
        {
            'id': 2,
            'type': 'config',
            'message': 'Configuration updated',
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'success'
        },
        {
            'id': 3,
            'type': 'validation',
            'message': 'Backup validation passed',
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'success'
        }
    ][:limit]

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Material Design Add-on Backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

