#!/usr/bin/env sh
set -e

echo "Starting Material Design Add-on..."

# Print environment info
echo "Python version: $(python3 --version)"
echo "Node version: $(node --version 2>/dev/null || echo 'Not available')"

# Check if Supervisor API is accessible
if [ -n "$SUPERVISOR_TOKEN" ]; then
    echo "Supervisor token found"
else
    echo "Warning: SUPERVISOR_TOKEN not set"
fi

# Start supervisord
echo "Starting services..."
exec /usr/bin/supervisord -c /etc/supervisord.conf

