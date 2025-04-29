#!/usr/bin/env groovy

/*
This script runs both the stage migration from production
*/

pipeline {

    agent {
        dockerfile {
            filename 'Dockerfile'
            args '-e DISCORD_WEBHOOK_URL=$DISCORD_WEBHOOK_URL -e PDAP_EMAIL=$PDAP_EMAIL -e PDAP_PASSWORD=$PDAP_PASSWORD -e LOCATION_IQ_API_KEY=$LOCATION_IQ_API_KEY'
        }
    }

    stages {
        stage('Run Geocoder') {
            steps {
                echo 'Running Geocoder...'
                sh 'whoami && id && ls -ld /tmp/.uv-cache'
                sh 'chmod +x *'
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