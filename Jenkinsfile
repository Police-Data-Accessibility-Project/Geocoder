#!/usr/bin/env groovy

pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = '1'
        IMAGE_NAME = 'pdap-geocoder'
        IMAGE_TAG = 'latest'
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
        JENKINS_UID = sh(script: 'id -u', returnStdout: true).trim()
    }

    stages {

        stage('Build Docker Image') {
            steps {
                echo "Building image with UID=${JENKINS_UID}"
                sh """
                    docker build \
                        --build-arg JENKINS_UID=${JENKINS_UID} \
                        -t ${FULL_IMAGE} \
                        .
                """
            }
        }

        stage('Run Geocoder in Docker') {
            agent {
                docker {
                    image "${FULL_IMAGE}"
                    reuseNode true
                    args "-e DISCORD_WEBHOOK_URL=${env.DISCORD_WEBHOOK_URL} \
                          -e PDAP_EMAIL=${env.PDAP_EMAIL} \
                          -e PDAP_PASSWORD=${env.PDAP_PASSWORD} \
                          -e LOCATION_IQ_API_KEY=${env.LOCATION_IQ_API_KEY}"
                }
            }
            steps {
                echo 'Running Geocoder...'
                sh 'whoami && id && ls -ld $UV_CACHE_DIR || echo "No cache dir found"'
                sh 'uv run main.py'
            }
        }
    }

    post {
        failure {
            script {
                def payload = """{
                    "content": "🚨 Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
                }"""

                sh """
                curl -X POST -H "Content-Type: application/json" -d '${payload}' ${env.DISCORD_WEBHOOK_URL}
                """
            }
        }
    }
}