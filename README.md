# gemini-app

1) Set the PROJECT_ID in your local dev
2) Ensure you are using ADC locally --> gcloud auth application-default login
3) Use a service account which has Vertex AI User, Artifact registry Admin roles
4) Assign Default Compute Engine Service Account Cloud Run Builder role so that Cloud Build can work and it uses by default Compute Enginer SA
5) Your User need to have Cloud Run Source Developer roles
6) no need to create a JSON Key for your service Account, Once ADC is configured properly, it will work in Cloud Run
7)  gcloud run deploy gemini-app \
    --source . \
    --region us-central1 \
    --port 8501 \
    --service-account=[your_sa]
    --allow-unauthenticated
