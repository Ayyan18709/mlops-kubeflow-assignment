from kfp import dsl
from kfp import compiler
from src.pipeline_components import data_extraction, data_preprocessing, model_training, model_evaluation

@dsl.pipeline(
    name='MLOps Assignment Pipeline',
    description='A pipeline that extracts data, preprocesses it, trains a model, and evaluates it.'
)
def mlops_pipeline(
    dvc_remote_url: str = "https://github.com/Ayyan18709/mlops-kubeflow-assignment",
    n_estimators: int = 100,
    test_size: float = 0.2
):
    # Step 1: Data Extraction
    extraction_task = data_extraction(dvc_remote_url=dvc_remote_url)
    
    # Step 2: Data Preprocessing
    preprocessing_task = data_preprocessing(
        input_csv=extraction_task.outputs['output_csv'],
        test_size=test_size
    )
    
    # Step 3: Model Training
    training_task = model_training(
        train_csv=preprocessing_task.outputs['train_csv'],
        n_estimators=n_estimators
    )
    
    # Step 4: Model Evaluation
    evaluation_task = model_evaluation(
        model_pkl=training_task.outputs['model_pkl'],
        test_csv=preprocessing_task.outputs['test_csv']
    )

if __name__ == "__main__":
    compiler.Compiler().compile(mlops_pipeline, 'pipeline.yaml')
    print("Pipeline compiled to pipeline.yaml")
