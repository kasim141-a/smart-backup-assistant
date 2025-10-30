# Quick Start Guide - Smart Backup & Restore Assistant

**Get up and running in 5 minutes!** ⚡

---

## 1. Install (2 minutes)

1. Go to **Settings** → **Add-ons** → **Add-on Store**
2. Search for "Smart Backup & Restore Assistant"
3. Click **Install**
4. Toggle **Start on boot** to ON
5. Click **Start**
6. Click **Open Web UI**

✅ **Done!** The add-on is now running.

---

## 2. Create Your First Backup (1 minute)

1. In the **Quick Actions** card, click **Backup Now**
2. Click **Confirm** in the dialog
3. Wait 2-5 minutes for completion
4. You'll see "Backup created successfully!"

✅ **Done!** Your first backup is ready.

---

## 3. Enable Automatic Backups (2 minutes)

1. Go to **Settings** → **Add-ons** → **Smart Backup & Restore Assistant**
2. Click the **Configuration** tab
3. Set these options:
   ```
   ☑ Enable Automatic Backups
   Backup Schedule: Daily
   Backup Time: 03:00
   Backup Retention Days: 7
   ☑ Enable Notifications
   ```
4. Click **Save**

✅ **Done!** Automatic backups will run every night at 3 AM.

---

## 4. Validate a Backup (30 seconds)

**Before restoring, always validate!**

1. In the **Quick Actions** card, click **Validate**
2. Wait 10-30 seconds
3. Review the results:
   - ✅ **Compatible** = Safe to restore
   - ⚠️ **Compatible with Warnings** = Proceed with caution
   - ❌ **Incompatible** = Don't restore

✅ **Done!** You know if the backup is safe.

---

## 5. Restore a Backup (10-15 minutes)

**⚠️ Warning: This will restart Home Assistant!**

1. **Validate the backup first** (see step 4)
2. In the **Quick Actions** card, click **Restore**
3. Read the warning carefully
4. Click **Confirm**
5. Wait 5-15 minutes
6. Refresh your browser and log in again

✅ **Done!** Your system is restored.

---

## Essential Tips

### 📅 Backup Schedule
- **Daily** - Recommended for most users
- **Weekly** - Minimum acceptable
- **Before updates** - Always!

### 💾 Storage
- Each backup: 500 MB - 2 GB
- Keep 7 days of backups
- Delete old backups if space is low

### 🔔 Notifications
- Enable all notifications
- Check your mobile app
- Verify backups are running

### ⚠️ Before Restoring
1. Validate the backup
2. Check compatibility
3. Warn family members
4. Allow 15-30 minutes

---

## Common Actions

### Create a Manual Backup
**Quick Actions** → **Backup Now** → **Confirm**

### Check Last Backup
Look at **System Status** → **Last Backup**

### Delete Old Backups
**Settings** → **System** → **Backups** → Select → **Delete**

### Download a Backup
**Settings** → **System** → **Backups** → Select → **Download**

### View Logs
**Settings** → **Add-ons** → **Smart Backup & Restore Assistant** → **Log**

---

## Troubleshooting

### Add-on Won't Start
1. Check logs for errors
2. Restart the add-on
3. Ensure you have free disk space (1 GB+)

### Backup Takes Too Long
1. Schedule during low usage times
2. Delete old backups to free space
3. Increase timeout in Configuration

### Restore Failed
1. Validate the backup first
2. Try a more recent backup
3. Check logs for error messages

### No Notifications
1. Verify notification service is set correctly
2. Test with Developer Tools → Services
3. Check mobile app permissions

---

## Need More Help?

📖 **Full Tutorial**: See USER_TUTORIAL.md for detailed instructions

💬 **Community**: [Home Assistant Forum](https://community.home-assistant.io/)

🐛 **Bug Reports**: [GitHub Issues](https://github.com/your-username/smart-backup-assistant/issues)

---

## Summary

You now know how to:
- ✅ Install the add-on
- ✅ Create backups
- ✅ Enable automatic backups
- ✅ Validate backups
- ✅ Restore safely

**Remember:** Backup regularly, validate before restoring, and keep multiple copies!

**Happy backing up!** 🎉

