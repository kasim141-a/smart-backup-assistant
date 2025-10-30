# Installation Guide - Smart Backup & Restore Assistant

## For Users: How to Install This Add-on

### Step 1: Add the Repository to Home Assistant

1. Open your Home Assistant instance
2. Navigate to **Settings** → **Add-ons** → **Add-on Store**
3. Click the **⋮** (three dots) menu in the top right corner
4. Select **Repositories**
5. In the text box, add this URL:
   ```
   https://github.com/YOUR_USERNAME/smart-backup-assistant
   ```
6. Click **Add**
7. Click **Close**

### Step 2: Install the Add-on

1. Refresh the Add-on Store page (press F5 or pull down to refresh)
2. Scroll down to find **Smart Backup & Restore Assistant**
3. Click on the add-on
4. Click **Install**
5. Wait 2-5 minutes for installation to complete

### Step 3: Configure and Start

1. After installation completes, configure the add-on:
   - Click the **Configuration** tab
   - Review and adjust settings as needed
   - Click **Save**

2. Start the add-on:
   - Go back to the **Info** tab
   - Toggle **Start on boot** to ON (recommended)
   - Click **Start**
   - Wait 30-60 seconds for startup

3. Open the interface:
   - Click **Open Web UI**
   - The add-on dashboard will open

### Step 4: Create Your First Backup

1. In the Web UI, click **Backup Now**
2. Confirm the action
3. Wait for the backup to complete
4. You're all set!

## For Repository Owners: How to Upload to GitHub

### Prerequisites

- GitHub account
- Git installed on your computer
- This add-on repository folder

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `smart-backup-assistant`
   - **Description**: "A powerful Home Assistant add-on that validates backups and checks for compatibility issues before restoration"
   - **Visibility**: **Public** (required for users to access)
   - **Initialize**: Do NOT check any boxes
3. Click **Create repository**

### Step 2: Prepare Local Repository

```bash
# Navigate to the repository folder
cd /path/to/addon-repo

# Initialize Git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Smart Backup & Restore Assistant v1.0.0"
```

### Step 3: Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/smart-backup-assistant.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Create Initial Release

1. Go to your repository on GitHub
2. Click **Releases** (right sidebar)
3. Click **Create a new release**
4. Fill in:
   - **Tag**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**: Copy from CHANGELOG.md
5. Click **Publish release**

### Step 5: Update Personal Information

Replace `YOUR_USERNAME` in these files:
- `README.md` (repository root)
- `smart-backup-assistant/README.md`
- `repository.yaml`

```bash
# On Linux/Mac:
find . -type f -name "*.md" -o -name "*.yaml" | xargs sed -i 's/YOUR_USERNAME/your-actual-username/g'

# On Windows (PowerShell):
Get-ChildItem -Recurse -Include *.md,*.yaml | ForEach-Object {
    (Get-Content $_) -replace 'YOUR_USERNAME', 'your-actual-username' | Set-Content $_
}
```

Then commit and push:
```bash
git add .
git commit -m "Update repository URLs with actual username"
git push
```

### Step 6: Test Installation

1. In your Home Assistant, add your repository:
   - Settings → Add-ons → Add-on Store
   - ⋮ → Repositories
   - Add: `https://github.com/YOUR_USERNAME/smart-backup-assistant`

2. Verify the add-on appears in the store
3. Install and test

## Repository Structure

Your GitHub repository should have this structure:

```
smart-backup-assistant/  (repository root)
│
├── repository.yaml  ← Required for add-on repository
│
├── smart-backup-assistant/  ← Add-on directory
│   ├── config.yaml
│   ├── Dockerfile
│   ├── build.yaml
│   ├── icon.png
│   ├── logo.png
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── LICENSE
│   ├── rootfs/
│   ├── frontend/
│   ├── docs/
│   └── images/
│
└── README.md  ← Repository README
```

## Important Notes

### ❌ This is NOT a HACS Repository

**Important:** Home Assistant add-ons are NOT distributed through HACS!

- HACS is for integrations, Lovelace cards, themes, and scripts
- Add-ons are installed through the Supervisor Add-on Store
- Users add your repository URL to their add-on repositories

### ✅ This IS an Add-on Repository

Users install by:
1. Adding your repository URL to Supervisor
2. Installing from the Add-on Store
3. NOT through HACS

## Troubleshooting

### Add-on Not Showing After Adding Repository

**Possible causes:**

1. **Missing repository.yaml**
   - Ensure `repository.yaml` exists at repository root
   - Check it has correct format

2. **Wrong directory structure**
   - Add-on folder must be at: `smart-backup-assistant/`
   - `config.yaml` must be at: `smart-backup-assistant/config.yaml`

3. **Repository not refreshed**
   - Refresh the Add-on Store page
   - Wait a few minutes and try again

4. **Invalid config.yaml**
   - Check `config.yaml` syntax
   - Ensure all required fields are present

### Repository Added But Add-on Won't Install

1. Check logs: Settings → System → Logs
2. Verify `Dockerfile` exists
3. Ensure `build.yaml` has correct architecture
4. Check for syntax errors in configuration files

### Users Can't Access Repository

1. Ensure repository is **Public** on GitHub
2. Verify URL is correct
3. Check repository.yaml is at root

## Support

If you need help:

- **GitHub Issues**: https://github.com/YOUR_USERNAME/smart-backup-assistant/issues
- **Home Assistant Community**: https://community.home-assistant.io/
- **Documentation**: See README.md in the add-on folder

## Updating Your Add-on

When you make changes:

1. Update version in `smart-backup-assistant/config.yaml`
2. Update `smart-backup-assistant/CHANGELOG.md`
3. Commit and push changes
4. Create new GitHub release with new version tag

Users will see the update in their Add-on Store!

---

**Questions?** See the full documentation in the `smart-backup-assistant/` folder.

