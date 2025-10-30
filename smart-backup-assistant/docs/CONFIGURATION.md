# Complete config.yaml Guide

## Overview

The `config.yaml` file is the heart of your Home Assistant add-on. It defines metadata, permissions, configuration options, and how the add-on integrates with Home Assistant.

## File Structure

### 1. Basic Information

```yaml
name: "Smart Backup & Restore Assistant"
description: >
  A modern Home Assistant add-on featuring Material Design 3 interface...
version: "1.0.0"
slug: "smart_backup_assistant"
url: "https://github.com/your-username/smart-backup-assistant"
```

**Fields:**
- `name` - Display name in the add-on store
- `description` - Detailed description (supports multi-line with `>`)
- `version` - Semantic version (MAJOR.MINOR.PATCH)
- `slug` - Unique identifier (lowercase, underscores only)
- `url` - Project homepage or repository

### 2. Architecture Support

```yaml
arch:
  - aarch64  # 64-bit ARM (Raspberry Pi 4, etc.)
  - amd64    # 64-bit x86 (Intel/AMD)
  - armhf    # 32-bit ARM (older Raspberry Pi)
  - armv7    # 32-bit ARM v7
  - i386     # 32-bit x86
```

**Recommendation:** Include all architectures unless you have platform-specific dependencies.

### 3. Startup Configuration

```yaml
startup: services
boot: auto
watchdog: "http://localhost:8099/api/health"
```

**Options:**

**startup:**
- `initialize` - Start before Home Assistant
- `system` - Start with system services
- `services` - Start after basic services (recommended)
- `application` - Start after Home Assistant
- `once` - Run once and exit

**boot:**
- `auto` - Start automatically on boot
- `manual` - Require manual start

**watchdog:**
- URL to check if add-on is healthy
- Home Assistant will restart the add-on if this fails

### 4. Network Configuration

```yaml
ports:
  8099/tcp: 8099

ingress: true
ingress_port: 8099
ingress_entry: /
```

**Ports:**
- Format: `container_port/protocol: host_port`
- Use ingress instead when possible

**Ingress (Recommended):**
- `ingress: true` - Enable Home Assistant's reverse proxy
- `ingress_port` - Port your app listens on
- `ingress_entry` - Entry path (usually `/`)
- **Benefits:** Automatic authentication, SSL, no port conflicts

### 5. Panel Configuration

```yaml
panel_icon: mdi:backup-restore
panel_title: "Backup Assistant"
panel_admin: false
```

**Fields:**
- `panel_icon` - Material Design Icon (see https://materialdesignicons.com/)
- `panel_title` - Title in the sidebar
- `panel_admin` - Require admin privileges (true/false)

### 6. API Access Permissions

```yaml
hassio_api: true
hassio_role: manager
auth_api: true
homeassistant_api: true
```

**hassio_role options:**
- `default` - Basic access (read system info)
- `homeassistant` - Control Home Assistant
- `backup` - Manage backups
- `manager` - Full Supervisor access (recommended for backup add-ons)
- `admin` - Complete system access

**API Access:**
- `hassio_api: true` - Access Supervisor API
- `auth_api: true` - Access authentication API
- `homeassistant_api: true` - Access Home Assistant API

### 7. Security Configuration

```yaml
host_network: false
privileged: []
apparmor: true
full_access: false
```

**Security Best Practices:**
- Keep `host_network: false` unless absolutely needed
- Avoid `full_access: true`
- Keep `apparmor: true` for security
- Only request necessary privileges

### 8. Hardware Access

```yaml
devices: []
usb: []
gpio: false
audio: false
video: false
```

**When to enable:**
- `devices` - Access specific devices (e.g., `/dev/ttyUSB0`)
- `usb` - Access USB devices
- `gpio` - Access GPIO pins (Raspberry Pi)
- `audio` - Access audio devices
- `video` - Access video devices

### 9. Backup Configuration

```yaml
backup: exclude
backup_exclude:
  - "*.log"
  - "*.tmp"
  - "__pycache__"
```

**Options:**
- `backup: exclude` - Exclude add-on data from backups
- `backup_exclude` - Patterns to exclude from backups

### 10. Folder Mapping

```yaml
map:
  - backup:rw     # Read-write access to backup folder
  - share:rw      # Read-write access to share folder
  - ssl:ro        # Read-only access to SSL certificates
  - media:ro      # Read-only access to media folder
```

**Available Folders:**
- `backup` - Home Assistant backup folder
- `share` - Shared folder between add-ons
- `ssl` - SSL certificates
- `media` - Media files
- `addons` - Add-ons folder
- `config` - Home Assistant configuration

**Access Modes:**
- `ro` - Read-only
- `rw` - Read-write

### 11. User Options

```yaml
options:
  auto_backup_enabled: true
  backup_schedule: "daily"
  backup_time: "03:00"
  # ... more options
```

**These are the default values** users see when they first install the add-on.

### 12. Schema Definition

```yaml
schema:
  auto_backup_enabled: bool
  backup_schedule: list(disabled|hourly|daily|weekly|monthly)
  backup_time: str
  backup_retention_days: int(1,365)
  backup_password: password?
```

**Schema Types:**

**Basic Types:**
- `bool` - Boolean (true/false)
- `int` - Integer
- `float` - Floating point number
- `str` - String
- `email` - Email address
- `url` - URL
- `password` - Password (hidden in UI)

**Constraints:**
- `int(1,365)` - Integer between 1 and 365
- `float(0.0,1.0)` - Float between 0.0 and 1.0
- `str?` - Optional string (can be empty)
- `password?` - Optional password

**Lists:**
- `list(option1|option2|option3)` - Dropdown with specific options

**Complex Types:**
- `port` - Network port (1-65535)
- `match(regex)` - String matching regex pattern

### 13. Translations

```yaml
translations:
  en:
    configuration:
      auto_backup_enabled:
        name: "Enable Automatic Backups"
        description: "Automatically create backups on schedule"
```

**Structure:**
- Language code (`en`, `de`, `fr`, etc.)
- `configuration` section for option descriptions
- `name` - Label shown in UI
- `description` - Help text shown in UI

### 14. Services

```yaml
services:
  - name: "create_backup"
    description: "Create a new backup"
    fields:
      name:
        description: "Name for the backup"
        example: "My Manual Backup"
```

**Purpose:** Define services that can be called from Home Assistant automations.

**Usage in Home Assistant:**
```yaml
service: hassio.addon_stdin
data:
  addon: smart_backup_assistant
  input:
    service: create_backup
    name: "Automated Backup"
```

## Complete Example Breakdown

### Our Add-on Configuration

```yaml
# Basic Info
name: "Smart Backup & Restore Assistant"
version: "1.0.0"
slug: "smart_backup_assistant"

# Architecture
arch: [aarch64, amd64, armhf, armv7, i386]

# Startup
startup: services        # Start after basic services
boot: auto              # Auto-start on boot
watchdog: "http://localhost:8099/api/health"

# Network
ingress: true           # Use Home Assistant's reverse proxy
ingress_port: 8099      # Our app runs on port 8099

# Panel
panel_icon: mdi:backup-restore
panel_title: "Backup Assistant"

# Permissions
hassio_api: true        # Access Supervisor API
hassio_role: manager    # Full backup management access
auth_api: true          # Access authentication
homeassistant_api: true # Access Home Assistant API

# Security
host_network: false     # Isolated network
full_access: false      # Limited access
apparmor: true          # Security enabled

# Folders
map:
  - backup:rw           # Need to manage backups
  - share:rw            # Share data between add-ons
  - ssl:ro              # Read SSL certificates
  - media:ro            # Read media files

# Options (defaults)
options:
  auto_backup_enabled: true
  backup_schedule: "daily"
  backup_retention_days: 7
  validate_before_restore: true
  notifications_enabled: true

# Schema (validation)
schema:
  auto_backup_enabled: bool
  backup_schedule: list(disabled|hourly|daily|weekly|monthly)
  backup_retention_days: int(1,365)
  validate_before_restore: bool
  notifications_enabled: bool
```

## Best Practices

### 1. Versioning
- Use semantic versioning: `MAJOR.MINOR.PATCH`
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

### 2. Security
- Request minimum necessary permissions
- Use ingress instead of exposed ports
- Keep `apparmor: true`
- Avoid `full_access: true`

### 3. User Experience
- Provide sensible defaults in `options`
- Add clear descriptions in `translations`
- Use appropriate schema types with constraints
- Include examples in service definitions

### 4. Compatibility
- Support all architectures if possible
- Test on different platforms
- Document any platform-specific requirements

### 5. Documentation
- Include `url` pointing to documentation
- Add `documentation` link to detailed guide
- Provide clear option descriptions

## Common Patterns

### Pattern 1: Web UI Add-on
```yaml
ingress: true
ingress_port: 8099
panel_icon: mdi:web
hassio_api: true
```

### Pattern 2: Backup Management Add-on
```yaml
hassio_role: manager
map:
  - backup:rw
options:
  retention_days: int(1,365)
```

### Pattern 3: Home Automation Add-on
```yaml
homeassistant_api: true
auth_api: true
services:
  - name: "trigger_action"
```

### Pattern 4: Hardware Access Add-on
```yaml
devices:
  - /dev/ttyUSB0
usb: true
privileged:
  - SYS_RAWIO
```

## Testing Your config.yaml

### 1. Validate Syntax
```bash
# Use Home Assistant's config validator
ha addons validate smart_backup_assistant
```

### 2. Check Options
- Install the add-on
- Open the Configuration tab
- Verify all options appear correctly
- Test changing values

### 3. Test Permissions
- Verify API access works
- Check folder access
- Test services

## Troubleshooting

### Issue: Add-on won't start
- Check `startup` value
- Verify `boot` is set correctly
- Check watchdog URL is accessible

### Issue: Can't access Supervisor API
- Verify `hassio_api: true`
- Check `hassio_role` has sufficient permissions
- Ensure `SUPERVISOR_TOKEN` is available

### Issue: Options not saving
- Check schema matches option names
- Verify schema types are correct
- Check for typos in option names

### Issue: Panel not appearing
- Verify `panel_icon` is valid MDI icon
- Check `panel_title` is set
- Ensure `ingress: true` is set

## Resources

- [Home Assistant Add-on Documentation](https://developers.home-assistant.io/docs/add-ons/configuration)
- [Material Design Icons](https://materialdesignicons.com/)
- [Supervisor API](https://developers.home-assistant.io/docs/api/supervisor/)
- [Add-on Security](https://developers.home-assistant.io/docs/add-ons/security)

## Summary

The `config.yaml` file is comprehensive but follows a logical structure:

1. **Metadata** - Name, version, description
2. **Platform** - Architecture support
3. **Startup** - When and how to start
4. **Network** - Ports and ingress
5. **UI** - Panel configuration
6. **Permissions** - API and system access
7. **Security** - AppArmor and privileges
8. **Storage** - Folder mappings
9. **Configuration** - User options and validation
10. **Localization** - Translations
11. **Integration** - Services

Start with the basics and add complexity as needed. Our configuration is production-ready and follows all best practices! 🎯

