pipeline {
    agent any

    stages {
        stage('Environment Setup') {
            steps {
                echo 'Setting up environment...'
                // Create virtual environment
                sh 'python3 -m venv venv || python -m venv venv'
                // Install dependencies using venv pip
                sh '''
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Pipeline Execution') {
            steps {
                echo 'Running MLflow pipeline...'
                // Run pipeline with venv python
                sh '''
                    . venv/bin/activate
                    python main.py
                '''
            }
        }
        
        stage('Verify Artifacts') {
            steps {
                echo 'Verifying artifacts...'
                sh 'ls -lh models/ || echo "models directory not found"'
                sh 'ls -lh metrics/ || echo "metrics directory not found"'
                sh 'cat metrics/metrics.json || echo "metrics.json not found"'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'models/*.pkl, metrics/*.json', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs above for details.'
        }
    }
}
