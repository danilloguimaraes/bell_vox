pipeline {
    agent any  // Runs on the Jenkins container

    environment {
        GIT_CREDENTIALS_ID = 'gh-danillo'
        GIT_REPO_URL = 'https://github.com/danilloguimaraes/bell_vox'
        GIT_BRANCH = 'main'
    }

    stages {
        stage('Checkout Código') {
            steps {
                script {
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "*/${GIT_BRANCH}"]],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [],
                        userRemoteConfigs: [[
                            url: GIT_REPO_URL,
                            credentialsId: GIT_CREDENTIALS_ID
                        ]]
                    ])
                }
            }
        }

        stage('Executar Testes em Docker') {
            steps {
                script {
                    sh '''
                        docker run --rm -v $PWD:/app -w /app python:3.10 sh -c "
                        python --version &&
                        pip install --upgrade pip &&
                        pip install -r requirements.txt &&
                        pip install pytest &&
                        pytest tests/"
                    '''
                }
            }
        }

        stage('Finalização') {
            steps {
                echo "✅ Pipeline finalizado com sucesso!"
            }
        }
    }
}
