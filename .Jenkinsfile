pipeline {
    agent any  // Executa em qualquer agente Jenkins disponível

    environment {
        GIT_CREDENTIALS_ID = 'gh-danillo'
        GIT_REPO_URL = 'https://github.com/danilloguimaraes/bell_vox'
        GIT_BRANCH = 'main'
        IMAGE_NAME = 'bell_vox'
        CONTAINER_NAME = 'bell_vox_app'
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

        stage('Build da Imagem Docker') {
            steps {
                script {
                    sh """
                        docker build -t ${IMAGE_NAME}:latest .
                    """
                }
            }
        }

        stage('Implantação do Container') {
            steps {
                script {
                    sh """
                        # Parar e remover container antigo, se existir
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true

                        # Iniciar novo container com Flask na porta padrão (5000)
                        docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Configuração do Proxy no nginx para o aplicativo bell_vox com arquivo de configuracao bell_vox.bell_vox.com.conf') {
            steps {
                script {
                    sh """
                        # Para o container do nginx
                        docker stop nginx || true

                        # Copiar arquivo de configuração do nginx
                        cp resources/bell_vox.conf /etc/nginx/conf.d/bell_vox.conf

                        # Reiniciar o container do nginx
                        docker start nginx
                    """
                }
            }
        }

        stage('Finalização') {
            steps {
                echo "✅ Implantação concluída com sucesso!"
            }
        }
    }
}
