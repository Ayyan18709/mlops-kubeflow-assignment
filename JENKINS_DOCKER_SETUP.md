# Running Jenkins with Docker

## Quick Start

### 1. Build and Start Jenkins
```bash
docker-compose up -d --build
```

### 2. Get Initial Admin Password
```bash
docker exec mlops-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 3. Access Jenkins
Open your browser and go to: **http://localhost:8080**

### 4. Setup Jenkins
1. Enter the initial admin password from step 2
2. Install suggested plugins (or skip if already installed via Dockerfile)
3. Create your first admin user
4. Start using Jenkins!

## Creating Your Pipeline Job

### Option 1: Using Blue Ocean (Recommended)
1. Click "Open Blue Ocean" in the sidebar
2. Click "New Pipeline"
3. Select "Git"
4. Enter your repository URL
5. Jenkins will automatically detect the Jenkinsfile

### Option 2: Classic UI
1. Click "New Item"
2. Enter job name: `mlops-assignment`
3. Select "Pipeline"
4. Click OK
5. Under "Pipeline" section:
   - Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: your git repo URL (or use local path)
   - Script Path: `Jenkinsfile`
6. Save and click "Build Now"

## Useful Commands

### View Jenkins Logs
```bash
docker logs -f mlops-jenkins
```

### Stop Jenkins
```bash
docker-compose down
```

### Restart Jenkins
```bash
docker-compose restart
```

### Access Jenkins Container Shell
```bash
docker exec -it mlops-jenkins bash
```

### Remove Everything (including volumes)
```bash
docker-compose down -v
```

## Troubleshooting

### Port Already in Use
If port 8080 is already in use, edit `docker-compose.yml` and change:
```yaml
ports:
  - "9090:8080"  # Use port 9090 instead
```

### Permission Issues
The Dockerfile runs Jenkins as root to avoid permission issues with Docker and Python.

### Pipeline Fails
1. Check Jenkins logs: `docker logs mlops-jenkins`
2. Verify Python is installed: `docker exec mlops-jenkins python --version`
3. Check if dependencies are installed: `docker exec mlops-jenkins pip list`

## Notes
- Jenkins data persists in the `jenkins_home` Docker volume
- Your project files are mounted at `/workspace` inside the container
- Python 3 and all requirements are pre-installed in the image
