#!/bin/bash

# Wrapper script to run the smoke tests locally
#
# Expected Env variables:
# CICD_PROJECT_ID - project id of the survey assist CICD project.
#
# Optional Env variables (script will attempt to resolve if not provided):
# SOC_VECTOR_STORE_URL - The URL of the SOC classification API to run the tests against
# SA_ID_TOKEN - A valid Google Identity Token generated from your credentials (assuming you're running locally) 
#
# Expected parameter: [sandbox|dev]
#
# Example ./run_smoke_tests.sh dev

if [[ ! -v CICD_PROJECT_ID ]]; then 
   echo "Please set the environment variable CICD_PROJECT_ID i.e. export CICD_PROJECT_ID="
   exit 1
fi

if [[ $1 = "sandbox" ]] || [[ $1 = "dev" ]]; then
   echo Test environment "$1"
else
  echo "Please pass test environment of 'sandbox' or 'dev' e.g. ./run_smoke_tests.sh sandbox"
  exit 1
fi

if [[ -z "${SOC_VECTOR_STORE_URL}" ]]; then
    echo Environment variable SOC_VECTOR_STORE_URL was not set, getting $1 url from parameter store:
    SOC_VECTOR_STORE_URL=$(gcloud parametermanager parameters versions describe $1 --parameter=infra-test-config --location=global --project $CICD_PROJECT_ID --format=json | python3 -c "import sys, json; print(json.load(sys.stdin)['payload']['data'])" | base64 --decode | python3 -c "import sys, json; print(json.load(sys.stdin)['cr-soc-url'])")/v1/soc-vector-store
    export SOC_VECTOR_STORE_URL
    echo "$SOC_VECTOR_STORE_URL"
else
    echo Using SOC_VECTOR_STORE_URL="$SOC_VECTOR_STORE_URL"
fi
#
# Example way to set token after gcloud auth login
# export SA_ID_TOKEN=`gcloud auth print-identity-token`
if [[ -z "${SA_ID_TOKEN}" ]]; then
    echo Environment variable SA_ID_TOKEN was not set, getting a new identity token from local credentials, if authenticated.
    SA_ID_TOKEN=$(gcloud auth print-identity-token)   
    export SA_ID_TOKEN 
else
    echo Using currently set SA_ID_TOKEN. If this becomes stale, run export SA_ID_TOKEN=\`gcloud auth print-identity-token\`
fi
pytest -s