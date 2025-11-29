# MLOps Pipeline Assignment

## Project Overview

This project demonstrates a complete MLOps workflow for a **housing price prediction** problem using the California Housing dataset. The pipeline implements:

- **Data Versioning**: DVC for tracking dataset versions
- **Experiment Tracking**: MLflow for logging experiments, parameters, and metrics
- **Pipeline Orchestration**: Python-based pipeline with modular components
- **CI/CD**: Jenkins for automated testing and deployment
- **Containerization**: Docker for reproducible environments

**ML Problem**: Predict median house values (MEDHOUSEVAL) based on features like median income, house age, average rooms, location, etc.

**Model**: Random Forest Regressor

## Project Structure

```
mlops-kubeflow-assignment/
├── src/
│   ├── pipeline_components.py    # Core pipeline functions
│   └── model_training.py          # Legacy training script
├── data/
│   └── raw_data.csv              # California Housing dataset
├── models/                        # Trained model artifacts
├── metrics/                       # Evaluation metrics
├── mlruns/                        # MLflow experiment tracking data
├── main.py                        # Pipeline orchestration script
├── Jenkinsfile                    # CI/CD pipeline definition
├── Dockerfile                     # Jenkins with Python environment
├── docker-compose.yml             # Docker orchestration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Setup Instructions

### Prerequisites

- **Docker & Docker Compose**: For running Jenkins
- **Python 3.9+**: For local development
- **Git**: For version control
- **DVC** (optional): For data versioning

### 1. Clone the Repository

```bash
git clone https://github.com/Ayyan18709/mlops-kubeflow-assignment.git
cd mlops-kubeflow-assignment
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `mlflow`: Experiment tracking and model registry
- `pandas`: Data manipulation
- `scikit-learn`: Machine learning algorithms
- `dvc`: Data version control
- `joblib`: Model serialization

### 3. DVC Setup (Optional)

If you want to use DVC for data versioning:

```bash
# Initialize DVC
dvc init

# Add remote storage (example: S3)
dvc remote add -d myremote s3://your-bucket/path

# Pull data
dvc pull
```

**Note**: The pipeline includes a fallback mechanism. If DVC is not available, it will use the existing data in the `data/` directory.

### 4. Jenkins Setup with Docker

#### Build and Start Jenkins

```bash
docker-compose up -d --build
```

This will:
- Build a custom Jenkins image with Python 3.13 and all dependencies
- Start Jenkins on port 8080
- Create a persistent volume for Jenkins data

#### Access Jenkins

1. Open browser: **http://localhost:8080**
2. If prompted for password, run:
   ```bash
   docker exec mlops-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Complete the setup wizard (or skip if disabled)

#### Create Pipeline Job

**Option 1: Blue Ocean UI (Recommended)**
1. Click "Open Blue Ocean"
2. Click "New Pipeline"
3. Select "Git" and enter your repository URL
4. Jenkins will auto-detect the `Jenkinsfile`

**Option 2: Classic UI**
1. Click "New Item"
2. Name: `mlops-pipeline`
3. Type: "Pipeline"
4. Under "Pipeline" section:
   - Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: your repo URL
   - Script Path: `Jenkinsfile`
5. Save and click "Build Now"

## Pipeline Walkthrough

### Pipeline Components

The pipeline consists of four main components defined in `src/pipeline_components.py`:

#### 1. Data Extraction
```python
data_extraction(dvc_remote_url, output_path)
```
- Fetches versioned data from DVC remote
- Fallback: Uses existing data if DVC fails
- **Output**: `data/raw_data.csv`

#### 2. Data Preprocessing
```python
data_preprocessing(input_csv, output_dir, test_size=0.2)
```
- Loads and cleans data
- Scales features using StandardScaler
- Splits into train/test sets (80/20)
- **Output**: `processed/train.csv`, `processed/test.csv`

#### 3. Model Training
```python
model_training(train_csv, model_dir, n_estimators=100)
```
- Trains Random Forest Regressor
- Logs parameters and metrics to MLflow
- Uses MLflow autologging for automatic tracking
- **Output**: `models/model.pkl`

#### 4. Model Evaluation
```python
model_evaluation(model_path, test_csv, metrics_dir)
```
- Evaluates model on test set
- Calculates MSE and R² score
- Logs metrics to MLflow
- **Output**: `metrics/metrics.json`

### Running the Pipeline Locally

#### Basic Execution

```bash
python main.py
```

#### With Custom Parameters

```bash
python main.py --n_estimators 200 --test_size 0.3
```

**Available Parameters:**
- `--dvc_url`: DVC remote URL (default: GitHub repo)
- `--n_estimators`: Number of trees in Random Forest (default: 100)
- `--test_size`: Test set proportion (default: 0.2)

### Viewing Results in MLflow

#### Start MLflow UI

```bash
mlflow ui
```

Then open: **http://localhost:5000**

#### What You'll See

- **Experiments**: "MLOps_Assignment_Flow"
- **Runs**: Each pipeline execution
- **Parameters**: n_estimators, test_size, etc.
- **Metrics**: MSE, R² score
- **Artifacts**: Model files, metrics

### CI/CD Pipeline (Jenkins)

The `Jenkinsfile` defines a 4-stage pipeline:

#### Stage 1: Environment Setup
- Checks Python version
- Verifies installed packages

#### Stage 2: Install Dependencies
- Installs/updates packages from `requirements.txt`

#### Stage 3: Pipeline Execution
- Runs `python main.py`
- Executes full ML pipeline

#### Stage 4: Verify Artifacts
- Lists generated models and metrics
- Displays metrics content

#### Post Actions
- Archives `models/*.pkl` and `metrics/*.json`
- Displays success/failure messages

### Expected Results

After running the pipeline, you should see:

```
Extracting data...
Preprocessing data...
Training model with n_estimators=100...
Evaluating model...
MSE: 0.255, R2: 0.805
```

**Artifacts Generated:**
- `models/model.pkl` (~145 MB)
- `metrics/metrics.json`
- MLflow runs in `mlruns/` directory

## Troubleshooting

### DVC Issues

**Problem**: `dvc: command not found`
**Solution**: Install DVC or let pipeline use existing data

### MLflow Issues

**Problem**: "Filesystem tracking backend deprecated"
**Solution**: This is just a warning. For production, use:
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db
```

### Jenkins Issues

**Problem**: Port 8080 already in use
**Solution**: Edit `docker-compose.yml`:
```yaml
ports:
  - "9090:8080"  # Use different port
```

**Problem**: Pipeline fails with "Python not found"
**Solution**: Rebuild Docker image:
```bash
docker-compose down
docker-compose up -d --build
```

### Permission Issues

**Problem**: Cannot write to directories
**Solution**: Check file permissions or run with appropriate user

## Performance Metrics

**Typical Results:**
- **MSE**: ~0.25
- **R² Score**: ~0.80
- **Training Time**: ~10-30 seconds (depending on n_estimators)

## Additional Resources

- **MLflow Documentation**: https://mlflow.org/docs/latest/
- **DVC Documentation**: https://dvc.org/doc
- **Jenkins Documentation**: https://www.jenkins.io/doc/
- **Scikit-learn**: https://scikit-learn.org/

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes.

## Contact

For questions or issues, please open an issue on GitHub.
