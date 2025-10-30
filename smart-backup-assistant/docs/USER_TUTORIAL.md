# Smart Backup & Restore Assistant - User Tutorial

**Welcome!** This tutorial will guide you through installing and using the Smart Backup & Restore Assistant add-on for Home Assistant. No technical knowledge required!

---

## 📖 Table of Contents

1. [What is This Add-on?](#what-is-this-add-on)
2. [Installation](#installation)
3. [First Time Setup](#first-time-setup)
4. [Creating Your First Backup](#creating-your-first-backup)
5. [Validating a Backup](#validating-a-backup)
6. [Restoring from a Backup](#restoring-from-a-backup)
7. [Configuring Automatic Backups](#configuring-automatic-backups)
8. [Understanding the Dashboard](#understanding-the-dashboard)
9. [Troubleshooting](#troubleshooting)
10. [Frequently Asked Questions](#frequently-asked-questions)

---

## What is This Add-on?

The **Smart Backup & Restore Assistant** is a tool that helps you:

✅ **Create backups** of your Home Assistant system  
✅ **Validate backups** before restoring them  
✅ **Check compatibility** between backup versions  
✅ **Restore safely** with confidence  
✅ **Schedule automatic backups** to protect your data  

### Why Do I Need This?

Think of backups like insurance for your smart home:

- 🛡️ **Protection** - If something goes wrong, you can restore everything
- ⏰ **Time-saving** - Automatic backups run while you sleep
- ✅ **Peace of mind** - Know your configuration is safe
- 🔍 **Smart validation** - Check if a backup is safe to restore before you do it

---

## Installation

### Step 1: Open the Add-on Store

1. Open your Home Assistant web interface
2. Click on **Settings** in the sidebar
3. Click on **Add-ons**
4. Click the **Add-on Store** button (bottom right)

### Step 2: Find the Add-on

**Option A: If you have the repository URL**
1. Click the three dots (⋮) in the top right
2. Select **Repositories**
3. Paste the repository URL
4. Click **Add**

**Option B: If it's in the official store**
1. Search for "Smart Backup & Restore Assistant"
2. Click on it when it appears

### Step 3: Install

1. Click the **Install** button
2. Wait for installation to complete (this may take a few minutes)
3. You'll see a success message when done

### Step 4: Start the Add-on

1. Toggle **Start on boot** to ON (recommended)
2. Toggle **Watchdog** to ON (recommended)
3. Click **Start**
4. Wait for the add-on to start (status will show "Running")

### Step 5: Open the Interface

1. Click **Open Web UI** at the top
2. The add-on interface will open in a new window

**Congratulations!** The add-on is now installed and running! 🎉

---

## First Time Setup

When you first open the add-on, you'll see a beautiful purple interface with several cards.

### Understanding the Interface

The dashboard has 5 main sections:

1. **Welcome Card** - Introduction and quick start
2. **Configuration Card** - Settings and preferences
3. **System Status Card** - Current system information
4. **Quick Actions Card** - Common tasks
5. **Progress Card** - Shows when operations are running

### Initial Configuration

1. **Click "Get Started"** in the Welcome card
2. The page will scroll to the Configuration section
3. Review the default settings:
   - ✅ **Enable automatic backups** - Recommended
   - ✅ **Send notifications** - Get alerts about backups
   - ⚠️ **Debug mode** - Leave OFF unless troubleshooting

4. Click **Save Configuration** when done

**Tip:** You can always change these settings later!

---

## Creating Your First Backup

### Why Create a Backup?

Before making any changes to your Home Assistant setup, create a backup. This lets you undo changes if something goes wrong.

### Step-by-Step Instructions

1. **Locate the Quick Actions Card**
   - It's the fourth card on the page
   - Has four purple buttons with icons

2. **Click "Backup Now"**
   - The button has a backup icon (📦)
   - A confirmation dialog will appear

3. **Confirm the Action**
   - Read the message: "Are you sure you want to create a backup now?"
   - Click **Confirm** to proceed
   - Click **Cancel** if you changed your mind

4. **Wait for Completion**
   - A progress bar will appear
   - You'll see "Backing up your Home Assistant configuration..."
   - This typically takes 2-5 minutes depending on your system size

5. **Success!**
   - You'll see a notification: "Backup created successfully!"
   - The backup will appear in your backup list

### What Gets Backed Up?

A full backup includes:
- ✅ Your Home Assistant configuration
- ✅ All add-ons and their settings
- ✅ Automations and scripts
- ✅ Dashboards and UI customizations
- ✅ User accounts and permissions
- ✅ Integration settings

**Note:** Media files and large databases may not be included to save space.

---

## Validating a Backup

### What is Backup Validation?

**Validation** checks if a backup is safe to restore. It's like a health check for your backup!

The add-on checks:
- ✅ Version compatibility (is the backup from a similar HA version?)
- ✅ Breaking changes (will anything stop working?)
- ✅ Missing add-ons (are all add-ons still available?)
- ✅ Risk assessment (how safe is it to restore?)

### When Should I Validate?

**Always validate before restoring!** Especially if:
- The backup is old (more than a few months)
- You've updated Home Assistant since creating the backup
- You're restoring to a different device
- You want to check what's in the backup

### How to Validate

1. **Select a Backup**
   - In the System Status card, you'll see "Last Backup"
   - Note the backup name and date

2. **Click "Validate"**
   - In the Quick Actions card
   - The button has a checkmark icon (✓)

3. **Wait for Validation**
   - This takes 10-30 seconds
   - The add-on is analyzing the backup

4. **Review the Results**
   - A detailed report will appear with:
     - **Status**: Compatible, Compatible with Warnings, or Incompatible
     - **Risk Level**: Low, Medium, or High
     - **Version Info**: Backup version vs. current version
     - **Issues**: Problems that might occur
     - **Warnings**: Things to be aware of

### Understanding Validation Results

#### ✅ Compatible (Low Risk)
```
Status: Compatible
Risk Level: Low
Backup Version: 2024.10.1
Current Version: 2024.10.2

✓ Backup is safe to restore!
```

**What this means:** Go ahead! The backup is from a similar version and should restore without issues.

#### ⚠️ Compatible with Warnings (Medium Risk)
```
Status: Compatible with Warnings
Risk Level: Medium
Backup Version: 2024.9.1
Current Version: 2024.10.1

Warnings:
- Minor version difference detected
- 2 add-ons from backup are not currently installed

⚠ Backup can be restored but proceed with caution.
```

**What this means:** The backup should work, but there might be minor issues. Read the warnings carefully.

#### ❌ Incompatible (High Risk)
```
Status: Incompatible
Risk Level: High
Backup Version: 2023.12.1
Current Version: 2024.10.1

Issues:
- Major version mismatch
- Breaking changes detected in 3 integrations

✗ Backup restoration is not recommended.
```

**What this means:** Don't restore this backup! It's too old or incompatible. You might break your system.

---

## Restoring from a Backup

### ⚠️ Important Warning

**Restoring a backup will:**
- Replace your current configuration
- Restart Home Assistant
- Take 5-15 minutes
- Temporarily disconnect all devices

**Before restoring:**
1. ✅ Validate the backup first
2. ✅ Make sure you have time (15-30 minutes)
3. ✅ Warn family members (devices will be offline)
4. ✅ Save any unsaved work

### Step-by-Step Restore Process

#### Step 1: Validate the Backup
Follow the [Validating a Backup](#validating-a-backup) section first!

#### Step 2: Initiate Restore

1. **Click "Restore"** in the Quick Actions card
   - The button has a restore icon (↻)
   
2. **Read the Confirmation Dialog Carefully**
   ```
   Restore Backup
   
   Are you sure you want to restore from "Backup 2024-10-25"?
   This will overwrite your current configuration and restart
   Home Assistant.
   ```

3. **Double-Check**
   - Is this the correct backup?
   - Did you validate it?
   - Do you have time to wait?

4. **Click "Confirm"** to proceed

#### Step 3: Wait for Restore

1. **Progress Bar Appears**
   - "Restore started..."
   - This takes 5-15 minutes

2. **Home Assistant Restarts**
   - You'll lose connection temporarily
   - This is normal!

3. **Reconnection**
   - Wait 2-3 minutes
   - Refresh your browser
   - Log in again if needed

#### Step 4: Verify Everything Works

After restore completes:

1. **Check the Dashboard**
   - Are all your devices showing?
   - Are automations working?

2. **Test Key Functions**
   - Turn on a light
   - Check a sensor
   - Run an automation

3. **Review Logs**
   - Go to Settings → System → Logs
   - Look for any errors (red text)

### What If Something Goes Wrong?

If the restore fails or things don't work:

1. **Don't Panic!** 
   - Home Assistant has built-in recovery

2. **Check Logs**
   - Settings → System → Logs
   - Look for error messages

3. **Try Again**
   - Sometimes a second restore works

4. **Restore a Different Backup**
   - Use a more recent backup
   - Or restore the automatic backup from before

5. **Ask for Help**
   - Home Assistant Community Forum
   - Include error messages from logs

---

## Configuring Automatic Backups

### Why Use Automatic Backups?

**Set it and forget it!** Automatic backups:
- 🌙 Run while you sleep
- 📅 Happen on schedule (daily, weekly, etc.)
- 🗑️ Delete old backups automatically
- 📧 Notify you when complete

### Setting Up Automatic Backups

1. **Open the Add-on Configuration**
   - Go to Settings → Add-ons
   - Click "Smart Backup & Restore Assistant"
   - Click the **Configuration** tab

2. **Configure Backup Settings**

   **Enable Automatic Backups**
   ```
   ☑ Enable Automatic Backups
   ```
   Toggle this ON

   **Backup Schedule**
   ```
   Backup Schedule: [Daily ▼]
   ```
   Choose how often:
   - **Hourly** - Every hour (for critical systems)
   - **Daily** - Once per day (recommended)
   - **Weekly** - Once per week
   - **Monthly** - Once per month

   **Backup Time**
   ```
   Backup Time: [03:00]
   ```
   Choose when backups run (24-hour format)
   - **03:00** (3:00 AM) - Recommended, least disruptive
   - **02:00** (2:00 AM) - Alternative
   - Avoid peak usage times!

   **Backup Retention**
   ```
   Backup Retention Days: [7]
   ```
   How many days to keep backups:
   - **7 days** - Recommended for most users
   - **14 days** - If you have space
   - **30 days** - For extra safety

3. **Configure Notifications**

   **Enable Notifications**
   ```
   ☑ Enable Notifications
   ☑ Notify on Backup Complete
   ☑ Notify on Backup Failed
   ☑ Notify on Validation Warning
   ```

   **Notification Service**
   ```
   Notification Service: [notify.notify]
   ```
   - Use `notify.notify` for mobile app
   - Or specify a custom service

4. **Advanced Settings (Optional)**

   **Compression**
   ```
   ☑ Enable Compression
   ```
   Saves storage space (recommended)

   **Password Protection**
   ```
   ☐ Password Protected Backups
   Backup Password: [________]
   ```
   Add a password for extra security (optional)

5. **Save Configuration**
   - Click **Save** at the bottom
   - The add-on will restart
   - Automatic backups will start on schedule

### Checking Automatic Backup Status

**In the Dashboard:**
- Look at the "Last Backup" in System Status
- Check the date/time
- Verify it matches your schedule

**In Notifications:**
- You should receive notifications when backups complete
- Check your Home Assistant mobile app

**In Logs:**
- Settings → Add-ons → Smart Backup & Restore Assistant → Log
- Look for "Backup created successfully"

---

## Understanding the Dashboard

Let's explore each section of the add-on interface in detail.

### 1. Welcome Card

```
┌─────────────────────────────────────┐
│ Welcome                             │
├─────────────────────────────────────┤
│ This is an example Home Assistant   │
│ add-on using Material Design Web    │
│ Components...                       │
│                                     │
│ [Get Started] [Learn More]         │
└─────────────────────────────────────┘
```

**What it does:**
- Introduces the add-on
- **Get Started** - Scrolls to configuration
- **Learn More** - Opens documentation

### 2. Configuration Card

```
┌─────────────────────────────────────┐
│ Configuration                       │
├─────────────────────────────────────┤
│ Server URL: [http://homeassistant...│
│ API Token:  [••••••••••••••••••••] │
│                                     │
│ ☑ Enable automatic backups          │
│ ☐ Send notifications                │
│ ⚪ Debug mode                        │
│                                     │
│ [Save Configuration] [Reset]        │
└─────────────────────────────────────┘
```

**What it does:**
- Configure add-on settings
- Enable/disable features
- Save or reset to defaults

### 3. System Status Card

```
┌─────────────────────────────────────┐
│ System Status                       │
├─────────────────────────────────────┤
│ ● Connection Status                 │
│   Connected to Home Assistant       │
│                                     │
│ 📦 Last Backup                      │
│   2 hours ago                       │
│                                     │
│ 💾 Storage Used                     │
│   2.4 GB / 10 GB                    │
└─────────────────────────────────────┘
```

**What it shows:**
- ● **Connection Status** - Green = connected, Red = disconnected
- 📦 **Last Backup** - When the most recent backup was created
- 💾 **Storage Used** - How much space backups are using

**Tip:** If storage is getting full, delete old backups or increase retention days.

### 4. Quick Actions Card

```
┌─────────────────────────────────────┐
│ Quick Actions                       │
├─────────────────────────────────────┤
│ [📦 Backup Now] [↻ Restore]        │
│ [✓ Validate]    [⚙ Settings]       │
└─────────────────────────────────────┘
```

**What each button does:**
- **📦 Backup Now** - Create a backup immediately
- **↻ Restore** - Restore from a backup
- **✓ Validate** - Check if a backup is safe to restore
- **⚙ Settings** - Jump to configuration section

### 5. Progress Card

```
┌─────────────────────────────────────┐
│ Operation in Progress               │
├─────────────────────────────────────┤
│ Backing up your Home Assistant      │
│ configuration...                    │
│ [████████░░░░░░░░░░░░] 40%         │
└─────────────────────────────────────┘
```

**What it shows:**
- Current operation status
- Progress bar (when available)
- Only visible during operations

---

## Troubleshooting

### Problem: Add-on Won't Start

**Symptoms:**
- Status shows "Stopped" or "Error"
- Can't open Web UI

**Solutions:**

1. **Check Logs**
   - Settings → Add-ons → Smart Backup & Restore Assistant → Log
   - Look for error messages in red

2. **Restart the Add-on**
   - Click **Stop**
   - Wait 10 seconds
   - Click **Start**

3. **Check System Resources**
   - Settings → System → Hardware
   - Ensure you have free disk space (at least 1 GB)
   - Ensure CPU isn't maxed out

4. **Reinstall**
   - Uninstall the add-on
   - Restart Home Assistant
   - Reinstall the add-on

### Problem: Backup Takes Too Long

**Symptoms:**
- Backup runs for more than 30 minutes
- Progress bar stuck

**Solutions:**

1. **Check System Load**
   - Don't run backups during heavy usage
   - Wait for automations to finish

2. **Free Up Space**
   - Delete old backups
   - Remove unused add-ons

3. **Increase Timeout**
   - Configuration → Backup Timeout Minutes
   - Increase from 60 to 120

### Problem: Can't Restore Backup

**Symptoms:**
- Restore fails with error
- Home Assistant won't start after restore

**Solutions:**

1. **Validate First**
   - Always validate before restoring
   - Check for compatibility issues

2. **Check Backup Integrity**
   - Try a different backup
   - Recent backups are more reliable

3. **Safe Mode Restore**
   - Settings → System → Backups
   - Use built-in restore as fallback

### Problem: Notifications Not Working

**Symptoms:**
- No notifications when backups complete
- Enabled in settings but not receiving

**Solutions:**

1. **Check Notification Service**
   - Configuration → Notification Service
   - Ensure it's set correctly (usually `notify.notify`)

2. **Test Notifications**
   - Developer Tools → Services
   - Call `notify.notify` with a test message

3. **Check Mobile App**
   - Ensure Home Assistant mobile app is installed
   - Check app notification permissions

### Problem: Storage Full

**Symptoms:**
- "Not enough space" error
- Backups failing

**Solutions:**

1. **Delete Old Backups**
   - Settings → System → Backups
   - Delete backups you don't need

2. **Reduce Retention**
   - Configuration → Backup Retention Days
   - Lower from 7 to 3 days

3. **Enable Compression**
   - Configuration → Enable Compression
   - Saves 30-50% space

### Problem: Web UI Won't Load

**Symptoms:**
- Blank page
- Loading forever
- Error messages

**Solutions:**

1. **Clear Browser Cache**
   - Press Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
   - Clear cache and cookies
   - Refresh page

2. **Try Different Browser**
   - Chrome, Firefox, or Safari
   - Disable browser extensions

3. **Check Add-on Status**
   - Ensure add-on is running
   - Check logs for errors

---

## Frequently Asked Questions

### General Questions

**Q: Is this add-on safe to use?**  
A: Yes! It uses Home Assistant's official Supervisor API and follows all security best practices.

**Q: Will backups slow down my system?**  
A: Slightly, but only while creating a backup. Schedule them at night to avoid impact.

**Q: How much space do backups use?**  
A: Typically 500 MB to 2 GB per backup, depending on your configuration size.

**Q: Can I use this with Home Assistant Cloud?**  
A: Yes! It works with any Home Assistant installation.

### Backup Questions

**Q: How often should I create backups?**  
A: Daily is recommended. Weekly minimum. Before any major changes.

**Q: What's the difference between full and partial backups?**  
A: Full backups include everything. Partial backups let you choose specific add-ons or folders. This add-on creates full backups.

**Q: Can I download backups to my computer?**  
A: Yes! Go to Settings → System → Backups, click a backup, then click Download.

**Q: Are backups encrypted?**  
A: You can enable password protection in Configuration for encrypted backups.

**Q: Can I restore to a different device?**  
A: Yes, but validate first! Hardware differences may cause issues.

### Validation Questions

**Q: Do I really need to validate before restoring?**  
A: Strongly recommended! Validation catches problems before they break your system.

**Q: What if validation shows "Medium Risk"?**  
A: Read the warnings carefully. Usually safe, but be prepared for minor issues.

**Q: Can I restore an "Incompatible" backup?**  
A: Not recommended. You might break your system. Try updating first or use a newer backup.

**Q: How long does validation take?**  
A: Usually 10-30 seconds.

### Configuration Questions

**Q: What's the best backup schedule?**  
A: Daily at 3:00 AM for most users. Adjust based on your usage patterns.

**Q: How many backups should I keep?**  
A: 7 days is good. 14 days if you have space. At least 3 days minimum.

**Q: Should I enable password protection?**  
A: Optional. Use it if you're concerned about backup security or storing backups off-site.

**Q: What does Debug Mode do?**  
A: Creates detailed logs for troubleshooting. Leave OFF unless asked by support.

### Technical Questions

**Q: Where are backups stored?**  
A: In Home Assistant's backup folder: `/backup/`

**Q: Can I access backups via SSH?**  
A: Yes, if you have the SSH add-on installed.

**Q: Does this replace Home Assistant's built-in backups?**  
A: No, it enhances them! It adds validation and smart features.

**Q: Can I use this with Google Drive backup?**  
A: Yes! This add-on works alongside other backup solutions.

---

## Tips & Best Practices

### 🎯 Backup Strategy

1. **3-2-1 Rule**
   - Keep **3** copies of your data
   - On **2** different storage types
   - With **1** copy off-site

2. **Regular Schedule**
   - Daily backups at night
   - Weekly backups downloaded to computer
   - Monthly backups to cloud storage

3. **Before Major Changes**
   - Always backup before updating Home Assistant
   - Backup before installing new add-ons
   - Backup before changing core configuration

### 🔒 Security Tips

1. **Password Protection**
   - Use strong passwords for encrypted backups
   - Store password securely (password manager)

2. **Off-Site Storage**
   - Download important backups
   - Store on external drive or cloud

3. **Regular Testing**
   - Validate backups monthly
   - Test restore process yearly

### ⚡ Performance Tips

1. **Schedule Wisely**
   - Run backups during low usage times
   - Avoid peak hours (evening)

2. **Storage Management**
   - Delete old backups regularly
   - Enable compression
   - Monitor storage usage

3. **Retention Balance**
   - Keep enough backups for safety
   - Don't keep so many that storage fills up

### 📱 Notification Setup

1. **Enable All Notifications**
   - Backup complete
   - Backup failed
   - Validation warnings

2. **Test Notifications**
   - Verify they work
   - Check they're not too noisy

3. **Review Regularly**
   - Check notification history
   - Ensure backups are running

---

## Getting Help

### Support Resources

**📚 Documentation**
- [Home Assistant Documentation](https://www.home-assistant.io/docs/)
- [Add-on GitHub Repository](https://github.com/your-username/smart-backup-assistant)

**💬 Community**
- [Home Assistant Community Forum](https://community.home-assistant.io/)
- [Home Assistant Discord](https://discord.gg/home-assistant)
- [Reddit r/homeassistant](https://reddit.com/r/homeassistant)

**🐛 Bug Reports**
- [GitHub Issues](https://github.com/your-username/smart-backup-assistant/issues)

### Before Asking for Help

When requesting support, include:

1. **Home Assistant Version**
   - Settings → About → Version

2. **Add-on Version**
   - Settings → Add-ons → Smart Backup & Restore Assistant → Version

3. **Error Messages**
   - Copy from logs
   - Include full error text

4. **What You Tried**
   - List troubleshooting steps
   - What worked/didn't work

5. **System Information**
   - Installation type (Home Assistant OS, Container, etc.)
   - Hardware (Raspberry Pi, NUC, etc.)

---

## Conclusion

Congratulations! You now know how to:

✅ Install the Smart Backup & Restore Assistant  
✅ Create backups manually and automatically  
✅ Validate backups before restoring  
✅ Restore safely with confidence  
✅ Configure automatic backups  
✅ Troubleshoot common issues  

### Remember the Golden Rules

1. **Backup regularly** - Daily is best
2. **Validate before restoring** - Always!
3. **Test your backups** - Make sure they work
4. **Keep multiple copies** - Don't rely on just one

### Stay Safe!

Your smart home is important. With regular backups, you can experiment, update, and customize with confidence knowing you can always restore if something goes wrong.

**Happy backing up!** 🎉

---

*Last updated: October 2024*  
*Add-on version: 1.0.0*  
*For the latest version of this tutorial, visit the GitHub repository.*

