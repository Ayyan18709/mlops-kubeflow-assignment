pipeline {
    agent any

    stages {
        stage('Environment Setup') {
            steps {
                echo 'Checking Python environment...'
                sh '''
                    python --version
                    pip --version
                    pip list | grep -E "(pandas|scikit-learn|mlflow|dvc)" || echo "Some packages may need installation"
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing/Updating dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Pipeline Execution') {
            steps {
                echo 'Running MLflow pipeline...'
                sh 'python main.py'
            }
        }
        
        stage('Verify Artifacts') {
            steps {
                echo 'Verifying artifacts...'
                sh '''
                    echo "=== Models Directory ==="
                    ls -lh models/ || echo "models directory not found"
                    echo ""
                    echo "=== Metrics Directory ==="
                    ls -lh metrics/ || echo "metrics directory not found"
                    echo ""
                    echo "=== Metrics Content ==="
                    cat metrics/metrics.json || echo "metrics.json not found"
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'models/*.pkl, metrics/*.json', allowEmptyArchive: true
        }
        success {
            echo '✅ Pipeline completed successfully!'
            echo 'Artifacts have been archived.'
        }
        failure {
            echo '❌ Pipeline failed. Check the logs above for details.'
        }
    }
}
