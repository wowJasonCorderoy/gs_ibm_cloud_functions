import helpers as hlp

try:
    PROJECT = hlp.get_project_id()
except:
    PROJECT = 'gcp-wow-pvc-grnstck-dev'