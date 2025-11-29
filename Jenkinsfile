pipeline {
    agent any

    stages {
        stage('Environment Setup') {
            steps {
                echo 'Setting up environment...'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Pipeline Execution') {
            steps {
                echo 'Running MLflow pipeline...'
                // Ensure environment is active
                sh '. venv/bin/activate && python main.py'
            }
        }
        
        stage('Verify Artifacts') {
            steps {
                echo 'Verifying artifacts...'
                sh 'ls -l models/'
                sh 'ls -l metrics/'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'models/*.pkl, metrics/*.json', allowEmptyArchive: true
        }
    }
}
