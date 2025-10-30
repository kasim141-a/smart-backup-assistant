# Contributing to Smart Backup & Restore Assistant

Thank you for considering contributing to this project! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

1. **Clear title** - Describe the issue briefly
2. **Description** - Explain what happened and what you expected
3. **Steps to reproduce** - How can we recreate the issue?
4. **Environment** - Home Assistant version, add-on version, hardware
5. **Logs** - Include relevant error messages from logs

### Suggesting Features

We love new ideas! To suggest a feature:

1. Check if it's already been suggested in Issues
2. Create a new issue with the "enhancement" label
3. Describe the feature and why it would be useful
4. Include examples of how it would work

### Submitting Pull Requests

1. **Fork the repository**
2. **Create a branch** - `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly** - Ensure nothing breaks
5. **Commit with clear messages** - Explain what and why
6. **Push to your fork** - `git push origin feature/your-feature-name`
7. **Create a Pull Request** - Describe your changes

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions focused and small

**JavaScript:**
- Use ES6+ features
- Add comments for complex logic
- Follow existing code style

**CSS:**
- Use meaningful class names
- Keep selectors simple
- Comment sections

### Testing

Before submitting:

- Test on a real Home Assistant instance
- Verify all features work
- Check for errors in logs
- Test on different browsers (for frontend changes)

### Documentation

If your change affects usage:

- Update README.md
- Update relevant documentation in `docs/`
- Add examples if applicable
- Update CHANGELOG.md

## Development Setup

### Prerequisites

- Home Assistant OS or Supervised installation
- Git
- Text editor or IDE
- Basic knowledge of Python and JavaScript

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/kasim141-a/smart-backup-assistant.git
   cd smart-backup-assistant
   ```

2. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Build frontend**
   ```bash
   npm run build
   ```

4. **Test locally**
   - Copy to Home Assistant addons directory
   - Install and start the add-on
   - Test your changes

### Project Structure

```
smart-backup-assistant/
├── config.yaml           # Add-on configuration
├── Dockerfile           # Container definition
├── rootfs/             # Root filesystem
│   └── app/           # Backend Python code
├── frontend/          # Frontend code
│   ├── src/          # Source files
│   └── dist/         # Built files
├── docs/             # Documentation
└── images/           # Screenshots
```

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated promptly and fairly.

## Questions?

Feel free to ask questions in:
- GitHub Discussions
- Home Assistant Community Forum
- Issue comments

Thank you for contributing! 🎉

