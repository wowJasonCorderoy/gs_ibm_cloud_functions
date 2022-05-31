# ibm cloud functions
Make sure you're in the correct gcp project:
gcloud config set project gcp-wow-pvc-grnstck-prod

Make sure you are in this repo's root directory before running below gcloud commands!!!

##Deploy:

gcloud functions deploy ibm_lamb_abattoir_constraints --entry-point=ibm_lamb_abattoir_constraints --runtime=python39 --trigger-http  --allow-unauthenticated --memory=4096MB --min-instances=1 --max-instances=100 --timeout=240 --set-secrets=ibm-creds=ibm-planning-creds:latest

gcloud functions deploy ibm_lamb_livestock --entry-point=ibm_lamb_livestock --runtime=python39 --trigger-http  --allow-unauthenticated --memory=4096MB --min-instances=1 --max-instances=100 --timeout=240 --set-secrets=ibm-creds=ibm-planning-creds:latest

gcloud functions deploy ibm_lamb_member_properties --entry-point=ibm_lamb_member_properties --runtime=python39 --trigger-http  --allow-unauthenticated --memory=4096MB --min-instances=1 --max-instances=100 --timeout=240 --set-secrets=ibm-creds=ibm-planning-creds:latest

gcloud functions deploy ibm_lamb_processing_fees --entry-point=ibm_lamb_processing_fees --runtime=python39 --trigger-http  --allow-unauthenticated --memory=4096MB --min-instances=1 --max-instances=100 --timeout=240 --set-secrets=ibm-creds=ibm-planning-creds:latest

gcloud functions deploy ibm_lamb_supplementary --entry-point=ibm_lamb_supplementary --runtime=python39 --trigger-http  --allow-unauthenticated --memory=4096MB --min-instances=1 --max-instances=100 --timeout=240 --set-secrets=ibm-creds=ibm-planning-creds:latest

##to test functions try running this in python:

import helpers as hlp

hlp.ping_cloud_function("https://us-central1-gcp-wow-pvc-grnstck-prod.cloudfunctions.net/ibm_lamb_abattoir_constraints", {'scenario_name':'TEST'})

hlp.ping_cloud_function("https://us-central1-gcp-wow-pvc-grnstck-prod.cloudfunctions.net/ibm_lamb_livestock", {'scenario_name':'TEST'})

hlp.ping_cloud_function("https://us-central1-gcp-wow-pvc-grnstck-prod.cloudfunctions.net/ibm_lamb_member_properties", {'scenario_name':'TEST'})

hlp.ping_cloud_function("https://us-central1-gcp-wow-pvc-grnstck-prod.cloudfunctions.net/ibm_lamb_processing_fees", {'scenario_name':'TEST'})

hlp.ping_cloud_function("https://us-central1-gcp-wow-pvc-grnstck-prod.cloudfunctions.net/ibm_lamb_supplementary", {'scenario_name':'TEST'})