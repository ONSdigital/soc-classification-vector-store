#!/bin/bash
GIT_SHA=$(git rev-parse --short HEAD)
gcloud beta builds submit .. --config=cicd/cloudbuild_dev_and_sandbox.yaml \
	--project survey-assist-sandbox \
	--service-account projects/ons-cicd-surveyassist/serviceAccounts/ons-cicd-surveyassist@ons-cicd-surveyassist.iam.gserviceaccount.com \
	--gcs-source-staging-dir gs://survey-assist-sandbox_cloudbuild/soc-api \
	--substitutions=_GAR_SOC_VECTOR_STORE_IMAGE=europe-west2-docker.pkg.dev/survey-assist-sandbox/soc-vector-store/soc-vector-store,SHORT_SHA=$GIT_SHA \
	--region europe-west2
