import constants as cnst

PROJECT = cnst.PROJECT
funcs2deploy = ['ibm_lamb_abattoir_constraints', 'ibm_lamb_livestock', 'ibm_lamb_member_properties', 'ibm_lamb_processing_fees', 'ibm_lamb_supplementary']

readme_str = f"""
# ibm cloud functions
Make sure you're in the correct gcp project:
gcloud config set project {PROJECT}

Make sure you are in this repo's root directory before running below gcloud commands!!!

##Deploy:
"""

for func in funcs2deploy:
    readme_str = readme_str+f"""
gcloud functions deploy {func} --entry-point={func} --runtime=python39 --trigger-http  --allow-unauthenticated --memory=4096MB --min-instances=1 --max-instances=100 --timeout=240 --set-secrets=ibm-creds=ibm-planning-creds:latest
"""

readme_str = readme_str+"""
##to test functions try running this in python:
"""

readme_str = readme_str+"""
import helpers as hlp
"""

for func in funcs2deploy:
    readme_str = readme_str+f"""
hlp.ping_cloud_function("https://us-central1-{PROJECT}.cloudfunctions.net/{func}", {{'scenario_name':'TEST'}})
"""

print(readme_str)

