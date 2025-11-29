# MLOps Pipeline Assignment (MLflow Edition)

## Project Overview
This project demonstrates an MLOps pipeline using **MLflow** for orchestration and tracking, DVC for data versioning, and Jenkins for CI/CD. The pipeline performs the following steps:
1.  **Data Extraction**: Fetches versioned data from a DVC remote.
2.  **Data Preprocessing**: Cleans, scales, and splits the data.
3.  **Model Training**: Trains a Random Forest Regressor and logs it with MLflow.
4.  **Model Evaluation**: Evaluates the model and logs metrics.

## Setup Instructions

### Prerequisites
-   Python 3.8+
-   MLflow
-   DVC

### 1. Installation
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 2. DVC Setup
This project uses DVC to manage data.
```bash
dvc pull
```
*Note: If you don't have access to the remote, the pipeline will generate dummy data for demonstration.*

## Pipeline Walkthrough

### Run the Pipeline
To run the entire pipeline, execute the `main.py` script:
```bash
python main.py
```
You can customize parameters:
```bash
python main.py --n_estimators 200 --test_size 0.3
```

### View Results in MLflow
Start the MLflow UI to view runs, parameters, and metrics:
```bash
mlflow ui
```
Open `http://localhost:5000` in your browser.

## CI/CD
A `Jenkinsfile` is provided to automate the pipeline execution. It includes stages for:
-   Environment Setup
-   Pipeline Execution (running `main.py`)
-   Artifact Verification
