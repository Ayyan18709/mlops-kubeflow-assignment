pipeline {
    agent any

    stages {
        stage('Environment Setup') {
            steps {
                echo 'Setting up environment...'
                // Windows-compatible commands
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Pipeline Execution') {
            steps {
                echo 'Running MLflow pipeline...'
                // Use venv python directly
                bat 'venv\\Scripts\\python main.py'
            }
        }
        
        stage('Verify Artifacts') {
            steps {
                echo 'Verifying artifacts...'
                // Windows dir command instead of ls
                bat 'dir models'
                bat 'dir metrics'
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
            echo 'Pipeline failed. Check the logs above.'
        }
    }
}
