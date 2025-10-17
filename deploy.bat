@echo off
REM Batfish Dashboard Deployment Script for Windows
REM This script provides multiple ways to deploy the dashboard with network connectivity

setlocal EnableDelayedExpansion

REM Configuration
set NETWORK_NAME=myNetwork
set IMAGE_NAME=batfish_dashboard
set CONTAINER_NAME=batfish_dashboard
set PORT=8050

echo 🚀 Batfish Dashboard Deployment Script
echo ======================================

if "%1"=="" goto deploy_compose
if "%1"=="compose" goto deploy_compose
if "%1"=="docker" goto deploy_docker
if "%1"=="cleanup" goto cleanup
if "%1"=="clean" goto cleanup
if "%1"=="status" goto status
goto usage

:check_network
docker network ls | findstr %NETWORK_NAME% >nul
if %errorlevel%==0 (
    echo ✅ Network '%NETWORK_NAME%' exists
    exit /b 0
) else (
    echo ❌ Network '%NETWORK_NAME%' does not exist
    exit /b 1
)

:create_network
echo 🔧 Creating network '%NETWORK_NAME%'...
docker network create %NETWORK_NAME%
echo ✅ Network '%NETWORK_NAME%' created
goto :eof

:deploy_compose
echo 🐳 Deploying using Docker Compose...

call :check_network
if %errorlevel%==1 (
    echo ⚠️  Network '%NETWORK_NAME%' not found. Creating it...
    call :create_network
)

echo 📦 Building and starting services...
docker-compose up --build -d

echo ✅ Dashboard deployed successfully!
echo 🌐 Access at: http://localhost:%PORT%
echo 📊 Monitor logs: docker-compose logs -f batfish-dashboard
goto end

:deploy_docker
echo 🐳 Deploying using direct Docker commands...

call :check_network
if %errorlevel%==1 (
    echo ⚠️  Network '%NETWORK_NAME%' not found. Creating it...
    call :create_network
)

echo 🔨 Building Docker image...
docker build -t %IMAGE_NAME% .

echo 🗑️  Removing existing container if present...
docker rm -f %CONTAINER_NAME% 2>nul

echo 🚀 Starting new container...
docker run -d --name %CONTAINER_NAME% --network %NETWORK_NAME% -p %PORT%:%PORT% --restart unless-stopped %IMAGE_NAME%

echo ✅ Dashboard deployed successfully!
echo 🌐 Access at: http://localhost:%PORT%
echo 📊 Monitor logs: docker logs -f %CONTAINER_NAME%
goto end

:cleanup
echo 🧹 Cleaning up deployment...

if exist docker-compose.yml (
    docker-compose down 2>nul
)

docker rm -f %CONTAINER_NAME% 2>nul
docker rmi %IMAGE_NAME% 2>nul

echo ✅ Cleanup completed
goto end

:status
echo 📊 Deployment Status:
docker network ls | findstr %NETWORK_NAME%
if %errorlevel%==0 (
    echo Network: Found
) else (
    echo Network: Not found
)

docker ps | findstr %CONTAINER_NAME%
if %errorlevel%==0 (
    echo Container: Running
) else (
    echo Container: Not running
)
goto end

:usage
echo Usage: %0 [compose^|docker^|cleanup^|status]
echo.
echo Commands:
echo   compose  - Deploy using Docker Compose (recommended)
echo   docker   - Deploy using direct Docker commands
echo   cleanup  - Stop and remove deployment
echo   status   - Check deployment status
echo.
echo Examples:
echo   %0                # Deploy using Docker Compose
echo   %0 compose        # Deploy using Docker Compose
echo   %0 docker         # Deploy using direct Docker
echo   %0 cleanup        # Clean up deployment

:end
endlocal