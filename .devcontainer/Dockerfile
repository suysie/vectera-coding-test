# Use backend as base
FROM backend AS base

# Install Node for frontend
USER root
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Switch back to app user
USER app
WORKDIR /workspace
