# GitHub Setup Instructions

Follow these steps to upload your Smart Backup & Restore Assistant add-on to GitHub and make it available through HACS.

## Prerequisites

- GitHub account
- Git installed on your computer
- The add-on files (this directory)

## Step 1: Create GitHub Repository

1. Go to https://github.com
2. Click the **+** icon in the top right
3. Select **New repository**
4. Fill in the details:
   - **Repository name**: `smart-backup-assistant` (or your preferred name)
   - **Description**: "A powerful Home Assistant add-on that validates backups and checks for compatibility issues before restoration"
   - **Visibility**: Public (required for HACS)
   - **Initialize**: Do NOT check any boxes (we have files already)
5. Click **Create repository**

## Step 2: Prepare Your Local Repository

Open a terminal and navigate to this directory:

```bash
cd /path/to/hacs-addon
```

Initialize Git repository:

```bash
git init
git add .
git commit -m "Initial commit: Smart Backup & Restore Assistant v1.0.0"
```

## Step 3: Connect to GitHub

Replace `kasim141-a` with your actual GitHub username:

```bash
git remote add origin https://github.com/kasim141-a/smart-backup-assistant.git
git branch -M main
git push -u origin main
```

If prompted, enter your GitHub credentials or use a personal access token.

## Step 4: Create Initial Release

1. Go to your repository on GitHub
2. Click **Releases** (right sidebar)
3. Click **Create a new release**
4. Fill in the release details:
   - **Tag**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**: Copy from CHANGELOG.md
5. Click **Publish release**

## Step 5: Add Repository to HACS

### Option A: Submit to HACS Default Repository (Recommended)

1. Go to https://github.com/hacs/default
2. Fork the repository
3. Edit `repositories.json`
4. Add your repository:
   ```json
   {
    "name": "kasim141-a/smart-backup-assistant",
     "category": "addon"
   }
   ```
5. Create a pull request
6. Wait for approval (may take a few days)

### Option B: Add as Custom Repository

Users can add your repository manually:

1. Open HACS in Home Assistant
2. Click the three dots (⋮) in the top right
3. Select **Custom repositories**
4. Add your repository URL: `https://github.com/kasim141-a/smart-backup-assistant`
5. Select category: **Add-on**
6. Click **Add**

## Step 6: Update README.md

Replace all instances of `kasim141-a` in README.md with your actual GitHub username:

```bash
# On Linux/Mac:
sed -i 's/kasim141-a/your-actual-username/g' README.md

# On Windows (PowerShell):
(Get-Content README.md) -replace 'kasim141-a', 'your-actual-username' | Set-Content README.md
```

Commit and push the changes:

```bash
git add README.md
git commit -m "Update README with correct GitHub username"
git push
```

## Step 7: Add Repository Badges (Optional)

Update the badge URLs in README.md with your repository information.

## Step 8: Create Icon and Screenshots

1. Create an icon (256x256 PNG) and save as `images/icon.png`
2. Create screenshots and save in `images/` directory
3. Commit and push:
   ```bash
   git add images/
   git commit -m "Add icon and screenshots"
   git push
   ```

## Step 9: Enable GitHub Actions

GitHub Actions will automatically run on every push to validate your add-on.

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Enable workflows if prompted

## Step 10: Test Installation

Test that users can install your add-on:

1. Open Home Assistant
2. Go to HACS → Add-ons
3. Add your repository as a custom repository
4. Search for "Smart Backup & Restore Assistant"
5. Install and test

## Updating Your Add-on

When you make changes:

1. **Update version** in `config.yaml`:
   ```yaml
   version: "1.1.0"
   ```

2. **Update CHANGELOG.md**:
   ```markdown
   ## [1.1.0] - 2024-10-27
   ### Added
   - New feature description
   ```

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Version 1.1.0: Add new feature"
   git push
   ```

4. **Create new release**:
   - Go to GitHub → Releases
   - Click "Create a new release"
   - Tag: `v1.1.0`
   - Publish release

HACS will automatically detect the new version!

## Repository Structure

Your GitHub repository should look like this:

```
smart-backup-assistant/
├── .github/
│   └── workflows/
│       ├── validate.yml
│       └── release.yml
├── docs/
│   ├── USER_TUTORIAL.md
│   ├── QUICK_START_GUIDE.md
│   ├── DEVELOPER.md
│   └── CONFIGURATION.md
├── frontend/
│   ├── src/
│   ├── package.json
│   └── rollup.config.js
├── images/
│   ├── icon.png
│   ├── logo.png
│   └── screenshots/
├── rootfs/
│   └── app/
│       ├── app.py
│       ├── supervisor_api.py
│       ├── backup_manager.py
│       └── config_manager.py
├── .gitignore
├── build.yaml
├── CHANGELOG.md
├── config.yaml
├── CONTRIBUTING.md
├── Dockerfile
├── hacs.json
├── LICENSE
├── README.md
└── repository.json
```

## Troubleshooting

### Push Rejected

If you get "push rejected":

```bash
git pull origin main --rebase
git push
```

### Authentication Failed

Use a Personal Access Token instead of password:

1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`
4. Copy the token
5. Use token as password when pushing

### HACS Not Detecting Repository

Ensure:
- Repository is public
- `hacs.json` exists
- `config.yaml` exists
- Repository has at least one release

## Support

If you need help:

- GitHub Discussions: https://github.com/kasim141-a/smart-backup-assistant/discussions
- HACS Discord: https://discord.gg/apgchf8
- Home Assistant Community: https://community.home-assistant.io/

## Next Steps

After setup:

1. ✅ Test installation from HACS
2. ✅ Create documentation videos (optional)
3. ✅ Announce on Home Assistant Community Forum
4. ✅ Share on Reddit r/homeassistant
5. ✅ Monitor issues and respond to users

Congratulations! Your add-on is now available to the Home Assistant community! 🎉

