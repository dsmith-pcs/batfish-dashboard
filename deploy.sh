#!/bin/bash

# Batfish Dashboard Deployment Script
# This script provides multiple ways to deploy the dashboard with network connectivity

set -e

# Configuration
NETWORK_NAME="myNetwork"
IMAGE_NAME="batfish_dashboard"
CONTAINER_NAME="batfish_dashboard"
PORT="8050"

echo "🚀 Batfish Dashboard Deployment Script"
echo "======================================"

# Function to check if network exists
check_network() {
    if docker network ls | grep -q "$NETWORK_NAME"; then
        echo "✅ Network '$NETWORK_NAME' exists"
        return 0
    else
        echo "❌ Network '$NETWORK_NAME' does not exist"
        return 1
    fi
}

# Function to create network if it doesn't exist
create_network() {
    echo "🔧 Creating network '$NETWORK_NAME'..."
    docker network create "$NETWORK_NAME"
    echo "✅ Network '$NETWORK_NAME' created"
}

# Function to deploy using Docker Compose (recommended)
deploy_compose() {
    echo "🐳 Deploying using Docker Compose..."

    if ! check_network; then
        echo "⚠️  Network '$NETWORK_NAME' not found. Creating it..."
        create_network
    fi

    echo "📦 Building and starting services..."
    docker-compose up --build -d

    echo "✅ Dashboard deployed successfully!"
    echo "🌐 Access at: http://localhost:$PORT"
    echo "📊 Monitor logs: docker-compose logs -f batfish-dashboard"
}

# Function to deploy using direct Docker commands
deploy_docker() {
    echo "🐳 Deploying using direct Docker commands..."

    if ! check_network; then
        echo "⚠️  Network '$NETWORK_NAME' not found. Creating it..."
        create_network
    fi

    echo "🔨 Building Docker image..."
    docker build -t "$IMAGE_NAME" .

    echo "🗑️  Removing existing container if present..."
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

    echo "🚀 Starting new container..."
    docker run -d \
        --name "$CONTAINER_NAME" \
        --network "$NETWORK_NAME" \
        -p "$PORT:$PORT" \
        --restart unless-stopped \
        "$IMAGE_NAME"

    echo "✅ Dashboard deployed successfully!"
    echo "🌐 Access at: http://localhost:$PORT"
    echo "📊 Monitor logs: docker logs -f $CONTAINER_NAME"
}

# Function to stop and remove deployment
cleanup() {
    echo "🧹 Cleaning up deployment..."

    # Stop and remove via compose if compose file exists
    if [ -f "docker-compose.yml" ]; then
        docker-compose down 2>/dev/null || true
    fi

    # Stop and remove direct container
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

    # Remove image
    docker rmi "$IMAGE_NAME" 2>/dev/null || true

    echo "✅ Cleanup completed"
}

# Main menu
case "${1:-}" in
    "compose"|"")
        deploy_compose
        ;;
    "docker")
        deploy_docker
        ;;
    "cleanup"|"clean")
        cleanup
        ;;
    "status")
        echo "📊 Deployment Status:"
        echo "Network: $(docker network ls | grep $NETWORK_NAME || echo 'Not found')"
        echo "Container: $(docker ps | grep $CONTAINER_NAME || echo 'Not running')"
        ;;
    *)
        echo "Usage: $0 [compose|docker|cleanup|status]"
        echo ""
        echo "Commands:"
        echo "  compose  - Deploy using Docker Compose (recommended)"
        echo "  docker   - Deploy using direct Docker commands"
        echo "  cleanup  - Stop and remove deployment"
        echo "  status   - Check deployment status"
        echo ""
        echo "Examples:"
        echo "  $0                # Deploy using Docker Compose"
        echo "  $0 compose        # Deploy using Docker Compose"
        echo "  $0 docker         # Deploy using direct Docker"
        echo "  $0 cleanup        # Clean up deployment"
        exit 1
        ;;
esac