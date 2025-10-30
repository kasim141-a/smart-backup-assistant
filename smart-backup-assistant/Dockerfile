# Multi-stage build for Smart Backup & Restore Assistant

# ============================================================================
# Stage 1: Build Frontend
# ============================================================================
ARG BUILD_FROM
FROM node:18-alpine AS frontend-builder

WORKDIR /build

# Copy frontend package files
COPY frontend/package*.json ./
COPY frontend/rollup.config.js ./

# Install dependencies
RUN npm install --production

# Copy frontend source
COPY frontend/src ./src/

# Build frontend
RUN npm run build

# ============================================================================
# Stage 2: Main Application
# ============================================================================
FROM ${BUILD_FROM}

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    nginx \
    supervisor \
    curl

# Set working directory
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY rootfs/app/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copy backend application
COPY rootfs/app/ /app/backend/

# Copy built frontend from builder stage
COPY --from=frontend-builder /build/dist /app/frontend/dist/
COPY frontend/index.html /app/frontend/
COPY frontend/src/styles.css /app/frontend/src/
COPY frontend/src/theme.css /app/frontend/src/

# Copy nginx configuration
COPY rootfs/etc/nginx/nginx.conf /etc/nginx/nginx.conf

# Copy supervisor configuration
COPY rootfs/etc/supervisor/conf.d/supervisord.conf /etc/supervisord.conf

# Copy startup script
COPY rootfs/run.sh /app/
RUN chmod +x /app/run.sh

# Create data directory
RUN mkdir -p /data

# Expose port
EXPOSE 8099

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8099/api/health || exit 1

# Set labels
LABEL \
    io.hass.name="Smart Backup & Restore Assistant" \
    io.hass.description="Intelligent backup management with validation" \
    io.hass.arch="aarch64|amd64|armhf|armv7|i386" \
    io.hass.type="addon" \
    io.hass.version="1.0.0"

# Run application
CMD ["/app/run.sh"]

