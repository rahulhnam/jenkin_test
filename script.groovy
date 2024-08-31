pipeline {
    agent { label 'master' }  // Specify the built-in node as the agent

    stages {
        stage('Run Python Script') {
            steps {
                echo 'Running extraction.py...'

                // Run the Python script
                bat 'python "extraction.py"'
            }
        }
    }
}