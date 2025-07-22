#!/bin/bash

# FosterDogs Development Scripts

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Help function
show_help() {
    echo "FosterDogs Development Scripts"
    echo ""
    echo "Usage: ./dev-scripts.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup       - Initial setup (build and start services)"
    echo "  start       - Start all services"
    echo "  stop        - Stop all services"
    echo "  restart     - Restart all services"
    echo "  build       - Build all containers"
    echo "  logs        - Show logs from all services"
    echo "  logs-f      - Follow logs from all services"
    echo "  logs-fe     - Show frontend logs"
    echo "  logs-be     - Show backend logs"
    echo "  init-db     - Initialize database with sample data"
    echo "  reset-db    - Reset database (WARNING: deletes all data)"
    echo "  shell-be    - Access backend container shell"
    echo "  shell-fe    - Access frontend container shell"
    echo "  clean       - Clean up containers and volumes"
    echo "  status      - Show containers status"
    echo "  test-be     - Run backend tests"
    echo "  help        - Show this help message"
}

# Setup function
setup() {
    print_status "Setting up FosterDogs development environment..."
    
    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    print_status "Building containers..."
    docker-compose build
    
    print_status "Starting services..."
    docker-compose up -d
    
    print_status "Waiting for services to start..."
    sleep 10
    
    print_status "Initializing database..."
    docker-compose exec backend python app/init_db.py
    
    print_success "Setup complete!"
    print_status "Access the application at:"
    echo "  Frontend: http://localhost"
    echo "  Backend API: http://localhost/api"
    echo "  API Docs: http://localhost/api/docs"
}

# Start services
start() {
    print_status "Starting FosterDogs services..."
    docker-compose up -d
    print_success "Services started!"
}

# Stop services
stop() {
    print_status "Stopping FosterDogs services..."
    docker-compose down
    print_success "Services stopped!"
}

# Restart services
restart() {
    print_status "Restarting FosterDogs services..."
    docker-compose restart
    print_success "Services restarted!"
}

# Build containers
build() {
    print_status "Building containers..."
    docker-compose build
    print_success "Build complete!"
}

# Show logs
logs() {
    docker-compose logs
}

# Follow logs
logs_follow() {
    docker-compose logs -f
}

# Frontend logs
logs_frontend() {
    docker-compose logs frontend
}

# Backend logs
logs_backend() {
    docker-compose logs backend
}

# Initialize database
init_db() {
    print_status "Initializing database..."
    docker-compose exec backend python app/init_db.py
    print_success "Database initialized!"
}

# Reset database
reset_db() {
    print_warning "This will delete ALL data in the database!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Resetting database..."
        docker-compose exec backend rm -f foster_dogs.db
        docker-compose exec backend python app/init_db.py
        print_success "Database reset complete!"
    else
        print_status "Database reset cancelled."
    fi
}

# Backend shell
shell_backend() {
    print_status "Accessing backend container shell..."
    docker-compose exec backend bash
}

# Frontend shell
shell_frontend() {
    print_status "Accessing frontend container shell..."
    docker-compose exec frontend sh
}

# Clean up
clean() {
    print_warning "This will remove all containers, networks, and volumes!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleaning up..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_success "Cleanup complete!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Show status
status() {
    print_status "Container status:"
    docker-compose ps
    echo ""
    print_status "System information:"
    docker system df
}

# Run backend tests
test_backend() {
    print_status "Running backend tests..."
    docker-compose exec backend pytest
    print_success "Tests completed!"
}

# Main script logic
case "${1:-help}" in
    setup)
        setup
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    build)
        build
        ;;
    logs)
        logs
        ;;
    logs-f)
        logs_follow
        ;;
    logs-fe)
        logs_frontend
        ;;
    logs-be)
        logs_backend
        ;;
    init-db)
        init_db
        ;;
    reset-db)
        reset_db
        ;;
    shell-be)
        shell_backend
        ;;
    shell-fe)
        shell_frontend
        ;;
    clean)
        clean
        ;;
    status)
        status
        ;;
    test-be)
        test_backend
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac