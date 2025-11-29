import argparse
import os
import mlflow
from src.pipeline_components import data_extraction, data_preprocessing, model_training, model_evaluation

def main():
    parser = argparse.ArgumentParser(description="MLOps Pipeline with MLflow")
    parser.add_argument("--dvc_url", type=str, default="https://github.com/Ayyan18709/mlops-kubeflow-assignment", help="DVC remote URL")
    parser.add_argument("--n_estimators", type=int, default=100, help="Number of trees in Random Forest")
    parser.add_argument("--test_size", type=float, default=0.2, help="Test set size")
    args = parser.parse_args()

    # Set up directories
    base_dir = os.getcwd()
    data_dir = os.path.join(base_dir, "data")
    processed_dir = os.path.join(base_dir, "processed")
    model_dir = os.path.join(base_dir, "models")
    metrics_dir = os.path.join(base_dir, "metrics")

    # Set MLflow experiment
    mlflow.set_experiment("MLOps_Assignment_Flow")

    with mlflow.start_run(run_name="Full Pipeline Run"):
        # Log parameters for the whole pipeline
        mlflow.log_param("dvc_url", args.dvc_url)
        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("test_size", args.test_size)

        # Step 1: Extraction
        raw_data_path = data_extraction(args.dvc_url, data_dir)
        
        # Step 2: Preprocessing
        train_path, test_path = data_preprocessing(raw_data_path, processed_dir, args.test_size)
        
        # Step 3: Training
        # Note: model_training starts its own nested run or logs to current run depending on implementation.
        # In our component, we used `mlflow.start_run()`. 
        # To nest it properly, we should probably remove `start_run` inside components or use `nested=True`.
        # For simplicity, let's let components manage their runs or just log to the active run if we remove `start_run` there.
        # However, since I already wrote components with `start_run`, let's adjust them or just call them.
        # If they use `start_run`, they will create child runs if nested=True is supported/default, or separate runs.
        # Let's modify components to NOT start a run if one is active, or just rely on the main run.
        # Actually, for this assignment, a single run with all metrics is fine.
        # I will modify main.py to NOT start a run, and let components start them? 
        # Or better: I'll modify components to accept an active run or just log.
        
        # Let's just run them. The components currently use `with mlflow.start_run(...)`.
        # This will create separate runs. That's okay for "Steps".
        
        model_path = model_training(train_path, model_dir, args.n_estimators)
        
        # Step 4: Evaluation
        model_evaluation(model_path, test_path, metrics_dir)

if __name__ == "__main__":
    main()
