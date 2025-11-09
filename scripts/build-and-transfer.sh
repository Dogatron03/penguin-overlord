#!/bin/bash
# Build Docker image locally and transfer to remote host (e.g., Raspberry Pi)
# Usage: ./build-and-transfer.sh [remote-host] [remote-user]
#   Example: ./build-and-transfer.sh 192.168.1.100 chiefgyk3d
#   Example: ./build-and-transfer.sh pi.local pi

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
IMAGE_NAME="penguin-overlord"
BRANCH=$(cd "$PROJECT_DIR" && git branch --show-current)

# Parse arguments
REMOTE_HOST="${1}"
REMOTE_USER="${2:-$USER}"

if [ -z "$REMOTE_HOST" ]; then
    echo -e "${YELLOW}Usage: $0 <remote-host> [remote-user]${NC}"
    echo ""
    echo "Examples:"
    echo "  $0 192.168.1.100 chiefgyk3d"
    echo "  $0 pi.local pi"
    echo "  $0 raspberrypi.local"
    exit 1
fi

echo -e "${BLUE}=== Penguin Overlord - Build and Transfer ===${NC}"
echo "Project: $PROJECT_DIR"
echo "Target: $REMOTE_USER@$REMOTE_HOST"
echo ""

# Ask for target architecture
echo -e "${BLUE}Select target architecture:${NC}"
echo "  1) AMD64/x86_64 (Intel/AMD processors)"
echo "  2) ARM64/aarch64 (Raspberry Pi, Apple Silicon)"
echo ""
read -p "Select [1-2] (default: 2 for Pi): " -n 1 -r ARCH_CHOICE
echo ""
ARCH_CHOICE="${ARCH_CHOICE:-2}"

if [ "$ARCH_CHOICE" = "1" ]; then
    PLATFORM="linux/amd64"
    ARCH_NAME="amd64"
    TARBALL="penguin-overlord-amd64.tar.gz"
elif [ "$ARCH_CHOICE" = "2" ]; then
    PLATFORM="linux/arm64"
    ARCH_NAME="arm64"
    TARBALL="penguin-overlord-arm64.tar.gz"
else
    echo -e "${RED}Invalid choice, defaulting to ARM64 for Raspberry Pi${NC}"
    PLATFORM="linux/arm64"
    ARCH_NAME="arm64"
    TARBALL="penguin-overlord-arm64.tar.gz"
fi

echo -e "${GREEN}Building for: $ARCH_NAME${NC}"
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}ERROR: Docker not found${NC}"
    exit 1
fi

# Check if Dockerfile exists
if [ ! -f "$PROJECT_DIR/Dockerfile" ]; then
    echo -e "${RED}ERROR: Dockerfile not found at $PROJECT_DIR/Dockerfile${NC}"
    exit 1
fi

# Detect current platform
CURRENT_ARCH=$(uname -m)
if [ "$CURRENT_ARCH" = "x86_64" ]; then
    CURRENT_PLATFORM="amd64"
elif [ "$CURRENT_ARCH" = "aarch64" ] || [ "$CURRENT_ARCH" = "arm64" ]; then
    CURRENT_PLATFORM="arm64"
else
    CURRENT_PLATFORM="unknown"
fi

echo "Current machine: $CURRENT_PLATFORM"

# Check if we need cross-compilation
if [ "$ARCH_NAME" != "$CURRENT_PLATFORM" ]; then
    echo -e "${YELLOW}Cross-compilation required: $CURRENT_PLATFORM → $ARCH_NAME${NC}"
    
    # Check if buildx is available
    if ! docker buildx version &> /dev/null; then
        echo -e "${YELLOW}Docker buildx not available - cannot cross-compile${NC}"
        echo ""
        echo "Would you like to transfer the code and build on the target machine instead?"
        echo "  Pro: No buildx needed, native ARM64 build"
        echo "  Con: Takes 15-30 minutes on Raspberry Pi"
        echo ""
        read -p "Transfer code and build on target? (Y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            echo ""
            echo "To enable cross-compilation, install docker buildx:"
            echo "  1. Update Docker to version 19.03+"
            echo "  2. Or install: https://github.com/docker/buildx"
            exit 1
        fi
        
        # Transfer code instead
        echo -e "${BLUE}Transferring code to $REMOTE_HOST...${NC}"
        
        # Ensure target has latest code
        ssh "$REMOTE_USER@$REMOTE_HOST" "cd ~/penguin-overlord && git fetch origin $BRANCH && git checkout $BRANCH && git pull origin $BRANCH" || {
            echo -e "${RED}Failed to update code on target${NC}"
            exit 1
        }
        
        echo -e "${GREEN}✓${NC} Code updated on target"
        echo ""
        echo -e "${BLUE}Building on $REMOTE_HOST (this will take 15-30 minutes)...${NC}"
        
        ssh "$REMOTE_USER@$REMOTE_HOST" "cd ~/penguin-overlord && docker build --no-cache -t penguin-overlord ." || {
            echo -e "${RED}Build failed on target${NC}"
            exit 1
        }
        
        echo -e "${GREEN}✓${NC} Build complete on target"
        echo ""
        echo -e "${GREEN}=== Next Steps ===${NC}"
        echo ""
        echo "Run the installer on target:"
        echo -e "  ${YELLOW}ssh $REMOTE_USER@$REMOTE_HOST${NC}"
        echo -e "  ${YELLOW}cd ~/penguin-overlord${NC}"
        echo -e "  ${YELLOW}sudo bash scripts/install-systemd.sh${NC}"
        echo ""
        exit 0
    fi
    
    USE_BUILDX=true
else
    echo "Native build (no cross-compilation needed)"
    USE_BUILDX=false
fi

# Build the image
echo -e "${BLUE}Step 1: Building Docker image for $ARCH_NAME...${NC}"
cd "$PROJECT_DIR"

if [ "$USE_BUILDX" = true ]; then
    # Use buildx for cross-platform builds
    echo "Using docker buildx for cross-platform build..."
    
    # Create builder instance if it doesn't exist
    if ! docker buildx ls | grep -q "multiarch"; then
        echo "Creating buildx builder instance..."
        docker buildx create --name multiarch --use
    else
        docker buildx use multiarch
    fi
    
    docker buildx build --platform $PLATFORM --load --no-cache --pull -t $IMAGE_NAME .
else
    # Standard build (native platform only)
    docker build --no-cache --pull -t $IMAGE_NAME .
fi

echo -e "${GREEN}✓${NC} Build complete"
echo ""

# Save to tarball
echo -e "${BLUE}Step 2: Saving image to tarball...${NC}"
echo "This may take a few minutes..."
docker save $IMAGE_NAME:latest | gzip > "$PROJECT_DIR/$TARBALL"
SIZE=$(du -h "$PROJECT_DIR/$TARBALL" | cut -f1)
echo -e "${GREEN}✓${NC} Saved to $TARBALL ($SIZE)"
echo ""

# Transfer to remote host
echo -e "${BLUE}Step 3: Transferring to $REMOTE_HOST...${NC}"
scp "$PROJECT_DIR/$TARBALL" "$REMOTE_USER@$REMOTE_HOST:~/"
echo -e "${GREEN}✓${NC} Transfer complete"
echo ""

# Generate load commands
echo -e "${GREEN}=== Next Steps on Remote Host ===${NC}"
echo ""
echo "SSH to your remote host:"
echo -e "  ${YELLOW}ssh $REMOTE_USER@$REMOTE_HOST${NC}"
echo ""
echo "Then load the image:"
echo -e "  ${YELLOW}gunzip -c ~/$TARBALL | docker load${NC}"
echo ""
echo "Verify the image:"
echo -e "  ${YELLOW}docker images | grep penguin-overlord${NC}"
echo ""
echo "Run the installer (it will detect and use existing image):"
echo -e "  ${YELLOW}cd ~/penguin-overlord${NC}"
echo -e "  ${YELLOW}sudo bash scripts/install-systemd.sh${NC}"
echo ""

# Ask if we should clean up local tarball
read -p "Delete local tarball? (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    rm "$PROJECT_DIR/$TARBALL"
    echo -e "${GREEN}✓${NC} Local tarball deleted"
else
    echo -e "${YELLOW}Tarball kept at: $PROJECT_DIR/$TARBALL${NC}"
fi

echo ""
echo -e "${GREEN}Done!${NC}"
