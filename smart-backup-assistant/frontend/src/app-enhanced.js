// Enhanced Frontend Application with Backend API Integration
// Import Material Web Components
import '@material/web/button/filled-button.js';
import '@material/web/button/outlined-button.js';
import '@material/web/button/text-button.js';
import '@material/web/button/filled-tonal-button.js';
import '@material/web/checkbox/checkbox.js';
import '@material/web/switch/switch.js';
import '@material/web/textfield/outlined-text-field.js';
import '@material/web/list/list.js';
import '@material/web/list/list-item.js';
import '@material/web/divider/divider.js';
import '@material/web/progress/linear-progress.js';
import '@material/web/dialog/dialog.js';

// Import Material Design typography styles
import { styles as typescaleStyles } from '@material/web/typography/md-typescale-styles.js';

// Apply typography styles globally
document.adoptedStyleSheets.push(typescaleStyles.styleSheet);

// API Configuration
const API_BASE_URL = '/api';

// Application State
const appState = {
    backups: [],
    currentBackup: null,
    systemStatus: null,
    config: null,
    isLoading: false
};

// Initialize the application
console.log('Material Web Components loaded successfully!');
document.addEventListener('DOMContentLoaded', initializeApp);

async function initializeApp() {
    console.log('Initializing Smart Backup & Restore Assistant...');
    
    // Setup event listeners
    setupEventListeners();
    
    // Load initial data
    await loadSystemStatus();
    await loadBackups();
    await loadConfig();
    
    // Update UI
    updateUI();
}

function setupEventListeners() {
    // Get references to elements
    const elements = {
        getStartedBtn: document.getElementById('get-started-btn'),
        learnMoreBtn: document.getElementById('learn-more-btn'),
        saveConfigBtn: document.getElementById('save-config-btn'),
        resetConfigBtn: document.getElementById('reset-config-btn'),
        backupNowBtn: document.getElementById('backup-now-btn'),
        restoreBtn: document.getElementById('restore-btn'),
        validateBtn: document.getElementById('validate-btn'),
        settingsBtn: document.getElementById('settings-btn'),
        refreshBtn: document.getElementById('refresh-btn'),
        confirmDialog: document.getElementById('confirm-dialog'),
        confirmActionBtn: document.getElementById('confirm-action-btn')
    };
    
    // Add event listeners
    elements.getStartedBtn?.addEventListener('click', handleGetStarted);
    elements.learnMoreBtn?.addEventListener('click', handleLearnMore);
    elements.saveConfigBtn?.addEventListener('click', handleSaveConfig);
    elements.resetConfigBtn?.addEventListener('click', handleResetConfig);
    elements.backupNowBtn?.addEventListener('click', () => showConfirmDialog('backup'));
    elements.restoreBtn?.addEventListener('click', handleRestore);
    elements.validateBtn?.addEventListener('click', handleValidate);
    elements.settingsBtn?.addEventListener('click', handleSettings);
    elements.refreshBtn?.addEventListener('click', handleRefresh);
    elements.confirmActionBtn?.addEventListener('click', handleConfirmAction);
}

// ============================================================================
// API Functions
// ============================================================================

async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showNotification(`Error: ${error.message}`, 'error');
        throw error;
    }
}

async function loadSystemStatus() {
    try {
        const response = await apiCall('/status');
        if (response.success) {
            appState.systemStatus = response.data;
            updateSystemStatusUI();
        }
    } catch (error) {
        console.error('Failed to load system status:', error);
    }
}

async function loadBackups() {
    try {
        const response = await apiCall('/backups');
        if (response.success) {
            appState.backups = response.data;
            updateBackupsUI();
        }
    } catch (error) {
        console.error('Failed to load backups:', error);
    }
}

async function loadConfig() {
    try {
        const response = await apiCall('/config');
        if (response.success) {
            appState.config = response.data;
            updateConfigUI();
        }
    } catch (error) {
        console.error('Failed to load config:', error);
    }
}

async function createBackup(name) {
    try {
        setLoading(true);
        const response = await apiCall('/backups/create', {
            method: 'POST',
            body: JSON.stringify({ name })
        });
        
        if (response.success) {
            showNotification('Backup created successfully!', 'success');
            await loadBackups();
        }
    } catch (error) {
        showNotification('Failed to create backup', 'error');
    } finally {
        setLoading(false);
    }
}

async function validateBackup(backupId) {
    try {
        setLoading(true);
        const response = await apiCall(`/backups/${backupId}/validate`, {
            method: 'POST'
        });
        
        if (response.success) {
            displayValidationResults(response.data);
        }
    } catch (error) {
        showNotification('Failed to validate backup', 'error');
    } finally {
        setLoading(false);
    }
}

async function restoreBackup(backupId) {
    try {
        setLoading(true);
        const response = await apiCall(`/backups/${backupId}/restore`, {
            method: 'POST'
        });
        
        if (response.success) {
            showNotification('Backup restore initiated. System will restart.', 'success');
        }
    } catch (error) {
        showNotification('Failed to restore backup', 'error');
    } finally {
        setLoading(false);
    }
}

async function saveConfiguration(config) {
    try {
        setLoading(true);
        const response = await apiCall('/config', {
            method: 'POST',
            body: JSON.stringify(config)
        });
        
        if (response.success) {
            showNotification('Configuration saved successfully!', 'success');
            await loadConfig();
        }
    } catch (error) {
        showNotification('Failed to save configuration', 'error');
    } finally {
        setLoading(false);
    }
}

async function resetConfiguration() {
    try {
        setLoading(true);
        const response = await apiCall('/config/reset', {
            method: 'POST'
        });
        
        if (response.success) {
            showNotification('Configuration reset to defaults', 'success');
            await loadConfig();
        }
    } catch (error) {
        showNotification('Failed to reset configuration', 'error');
    } finally {
        setLoading(false);
    }
}

// ============================================================================
// Event Handlers
// ============================================================================

function handleGetStarted() {
    console.log('Get Started clicked');
    showNotification('Welcome! Let\'s get you set up.', 'info');
    // Scroll to configuration section
    document.querySelector('.card:nth-child(2)')?.scrollIntoView({ behavior: 'smooth' });
}

function handleLearnMore() {
    console.log('Learn More clicked');
    window.open('https://developers.home-assistant.io/', '_blank');
}

async function handleSaveConfig() {
    console.log('Save Configuration clicked');
    
    // Get form values
    const autoBackup = document.querySelector('md-checkbox[id="auto-backup"]')?.checked || false;
    const notifications = document.querySelector('md-checkbox[id="notifications"]')?.checked || false;
    const debugMode = document.querySelector('md-switch[id="debug-mode"]')?.selected || false;
    
    const config = {
        auto_backup_enabled: autoBackup,
        notifications_enabled: notifications,
        debug_mode: debugMode
    };
    
    await saveConfiguration(config);
}

async function handleResetConfig() {
    console.log('Reset Configuration clicked');
    
    const confirmed = confirm('Are you sure you want to reset configuration to defaults?');
    if (confirmed) {
        await resetConfiguration();
    }
}

async function handleValidate() {
    console.log('Validate clicked');
    
    // Get selected backup
    const selectedBackup = getSelectedBackup();
    if (!selectedBackup) {
        showNotification('Please select a backup to validate', 'warning');
        return;
    }
    
    await validateBackup(selectedBackup.id);
}

function handleRestore() {
    console.log('Restore clicked');
    
    // Get selected backup
    const selectedBackup = getSelectedBackup();
    if (!selectedBackup) {
        showNotification('Please select a backup to restore', 'warning');
        return;
    }
    
    showConfirmDialog('restore', selectedBackup);
}

function handleSettings() {
    console.log('Settings clicked');
    // Scroll to configuration section
    document.querySelector('.card:nth-child(2)')?.scrollIntoView({ behavior: 'smooth' });
}

async function handleRefresh() {
    console.log('Refresh clicked');
    await loadSystemStatus();
    await loadBackups();
    showNotification('Data refreshed', 'info');
}

function showConfirmDialog(action, backup = null) {
    const dialog = document.getElementById('confirm-dialog');
    const headline = dialog.querySelector('[slot="headline"]');
    const content = dialog.querySelector('[slot="content"]');
    
    // Update dialog content based on action
    if (action === 'backup') {
        headline.textContent = 'Create Backup';
        content.textContent = 'Are you sure you want to create a backup now? This may take a few minutes.';
    } else if (action === 'restore') {
        headline.textContent = 'Restore Backup';
        content.textContent = `Are you sure you want to restore from "${backup?.name}"? This will overwrite your current configuration and restart Home Assistant.`;
    }
    
    // Store the action and backup for later
    dialog.dataset.action = action;
    if (backup) {
        dialog.dataset.backupId = backup.id;
    }
    
    // Show the dialog
    dialog.show();
}

async function handleConfirmAction() {
    const dialog = document.getElementById('confirm-dialog');
    const action = dialog.dataset.action;
    const backupId = dialog.dataset.backupId;
    
    console.log(`Confirmed action: ${action}`);
    
    if (action === 'backup') {
        const backupName = `Backup ${new Date().toLocaleString()}`;
        await createBackup(backupName);
    } else if (action === 'restore' && backupId) {
        await restoreBackup(backupId);
    }
}

// ============================================================================
// UI Update Functions
// ============================================================================

function updateUI() {
    updateSystemStatusUI();
    updateBackupsUI();
    updateConfigUI();
}

function updateSystemStatusUI() {
    if (!appState.systemStatus) return;
    
    const { homeassistant, supervisor } = appState.systemStatus;
    
    // Update connection status
    const connectionItem = document.querySelector('md-list-item:nth-child(1)');
    if (connectionItem) {
        const headline = connectionItem.querySelector('[slot="headline"]');
        const supportingText = connectionItem.querySelector('[slot="supporting-text"]');
        const icon = connectionItem.querySelector('[slot="start"]');
        
        if (homeassistant?.state === 'running') {
            headline.textContent = 'Connection Status';
            supportingText.textContent = `Connected to Home Assistant ${homeassistant.version}`;
            icon.textContent = 'check_circle';
            icon.style.color = '#4caf50';
        } else {
            headline.textContent = 'Connection Status';
            supportingText.textContent = 'Disconnected';
            icon.textContent = 'error';
            icon.style.color = '#f44336';
        }
    }
}

function updateBackupsUI() {
    if (!appState.backups || appState.backups.length === 0) return;
    
    // Update last backup info
    const lastBackup = appState.backups[0];
    const lastBackupItem = document.querySelector('md-list-item:nth-child(3)');
    
    if (lastBackupItem && lastBackup) {
        const supportingText = lastBackupItem.querySelector('[slot="supporting-text"]');
        const date = new Date(lastBackup.date);
        const timeAgo = getTimeAgo(date);
        supportingText.textContent = `${lastBackup.name} - ${timeAgo}`;
    }
}

function updateConfigUI() {
    if (!appState.config) return;
    
    // Update form fields
    const autoBackupCheckbox = document.querySelector('md-checkbox[id="auto-backup"]');
    const notificationsCheckbox = document.querySelector('md-checkbox[id="notifications"]');
    const debugModeSwitch = document.querySelector('md-switch[id="debug-mode"]');
    
    if (autoBackupCheckbox) {
        autoBackupCheckbox.checked = appState.config.auto_backup_enabled;
    }
    
    if (notificationsCheckbox) {
        notificationsCheckbox.checked = appState.config.notifications_enabled;
    }
    
    if (debugModeSwitch) {
        debugModeSwitch.selected = appState.config.debug_mode;
    }
}

function displayValidationResults(validation) {
    const { status, risk_level, backup_version, current_version, warnings, issues } = validation;
    
    let message = `Backup Version: ${backup_version}\nCurrent Version: ${current_version}\n\n`;
    message += `Status: ${status}\nRisk Level: ${risk_level}\n\n`;
    
    if (issues.length > 0) {
        message += 'Issues:\n';
        issues.forEach(issue => {
            message += `- ${issue.message}\n`;
        });
    }
    
    if (warnings.length > 0) {
        message += '\nWarnings:\n';
        warnings.forEach(warning => {
            message += `- ${warning.message}\n`;
        });
    }
    
    if (status === 'compatible') {
        message += '\n✓ Backup is safe to restore!';
    } else if (status === 'compatible_with_warnings') {
        message += '\n⚠ Backup can be restored but proceed with caution.';
    } else {
        message += '\n✗ Backup restoration is not recommended.';
    }
    
    alert(message);
}

// ============================================================================
// Helper Functions
// ============================================================================

function setLoading(loading) {
    appState.isLoading = loading;
    
    // Show/hide progress indicator
    const progressCard = document.querySelector('.card:last-child');
    if (progressCard) {
        progressCard.style.display = loading ? 'block' : 'none';
    }
}

function getSelectedBackup() {
    // In a real implementation, you would have a UI for selecting backups
    // For now, return the first backup
    return appState.backups[0] || null;
}

function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };
    
    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval > 1 ? 's' : ''} ago`;
        }
    }
    
    return 'just now';
}

function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // In a real implementation, you would use Material Design snackbar
    // For now, use alert
    alert(message);
}

// Export functions for testing
export {
    initializeApp,
    apiCall,
    loadSystemStatus,
    loadBackups,
    loadConfig,
    createBackup,
    validateBackup,
    restoreBackup,
    saveConfiguration,
    resetConfiguration,
    handleGetStarted,
    handleLearnMore,
    handleSaveConfig,
    handleResetConfig,
    handleValidate,
    handleRefresh,
    showConfirmDialog,
    handleConfirmAction,
    updateUI,
    showNotification
};

