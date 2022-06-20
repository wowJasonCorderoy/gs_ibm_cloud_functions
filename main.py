import numpy as np
import pandas as pd
from TM1py.Services import TM1Service
from TM1py.Utils.Utils import build_pandas_dataframe_from_cellset
from google.cloud import bigquery
import os
import json
import re
import constants as cnst

PROJECT = cnst.PROJECT

def ibm_lamb_abattoir_constraints(request):
    # Extracting MDX data and convert to a dataframe
    #Version = 'TEST'
    Version = request.form.get('scenario_name')

    env_var_ibm_creds = 'ibm-creds'
    ibm_creds = json.loads(os.environ[env_var_ibm_creds])

    url = ibm_creds['url']
    ibm_user = ibm_creds['user']
    ibm_password = ibm_creds['password']

    with TM1Service(base_url=url, user=ibm_user, password=ibm_password, namespace='LDAP', ssl=True) as tm1:

        Country =  "AU"
        Livestock =  "LAMB"

        mdx = """
        SELECT {
        TM1SubsetToSet([Time].[Time],"FY Week Leaves","public")
        } ON 0, 
        {
        TM1SubsetToSet([Abattoir].[Abattoir],"Lamb Abattoirs","public")}*
        {TM1SubsetToSet([LivestockMeasure].[LivestockMeasure],"Optimiser Constraints","public")} ON 1 
        FROM [LivestockModel] WHERE (
        [Version].[Version].["""+Version+"""], [Contract].[Contract].[None], [Livestock].[Livestock].[Lamb]
        )
        """

        df = tm1.cubes.cells.execute_mdx_dataframe(mdx,skip_consolidated_cells=True,include_attributes=False,skip_zeros=False).fillna(0)

    df['scenario_name'] = Version

    print("printing df")
    print(df)

    client = bigquery.Client(project=PROJECT)
    table_id = 'ibm.ibm_lamb_abattoir_constraints'

    v_scenario_name = Version.lower()

    sql = (
    f"""
    DELETE FROM `{PROJECT}.{table_id}`
    WHERE lower(scenario_name) = '""" + v_scenario_name + """'
    """
    )

    try: # if doesn't exist then don't error.
        client.query(sql)
    except:
        f"no delete for v_scenario_name: {v_scenario_name}"

    # Write out to GCP  
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

    return {'df':df.to_json(orient='index')}

def ibm_lamb_livestock(request):
    # Extracting MDX data and convert to a dataframe
    #Version = 'TEST'
    Version = request.form.get('scenario_name')

    env_var_ibm_creds = 'ibm-creds'
    ibm_creds = json.loads(os.environ[env_var_ibm_creds])

    url = ibm_creds['url']
    ibm_user = ibm_creds['user']
    ibm_password = ibm_creds['password']

    with TM1Service(base_url=url, user=ibm_user, password=ibm_password, namespace='LDAP', ssl=True) as tm1:

        Country =  "AU"
        Livestock =  "LAMB"

        mdx = """
        SELECT 
        {
        TM1SubsetToSet([Time].[Time],"FY Week Leaves","public")
        } ON 0, 
        {TM1SubsetToSet([Abattoir].[Abattoir],"Lamb Abattoirs","public")}*
        {TM1SubsetToSet([Contract].[Contract],"Lamb Contracts","public")}*
        {TM1SubsetToSet([LivestockMeasure].[LivestockMeasure],"Lamb Livestock Cost Drivers","public")} ON 1 
        FROM [LivestockModel] 
        WHERE ([Version].[Version].["""+Version+"""], [Livestock].[Livestock].[Lamb])
        """
        df = tm1.cubes.cells.execute_mdx_dataframe(mdx,skip_consolidated_cells=True,include_attributes=False,skip_zeros=False).fillna(0)

    df['scenario_name'] = Version

    print("printing df")
    print(df)

    client = bigquery.Client(project=PROJECT)
    table_id = 'ibm.ibm_lamb_livestock'

    v_scenario_name = Version.lower()

    sql = (
    f"""
    DELETE FROM `{PROJECT}.{table_id}`
    WHERE lower(scenario_name) = '""" + v_scenario_name + """'
    """
    )

    try: # if doesn't exist then don't error.
        client.query(sql)
    except:
        f"no delete for v_scenario_name: {v_scenario_name}"

    # Write out to GCP  
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

    return {'df':df.to_json(orient='index')}

def clean_cols(df):
  c_names = df.columns
  c0 = [re.sub('[^a-zA-Z0-9]+', '_', x) for x in c_names]
  c1 = [re.sub('^[^a-zA-Z]+', '', x) for x in c0]
  return c1

def ibm_lamb_member_properties(request):
    # Extracting MDX data and convert to a dataframe
    Version = request.form.get('scenario_name')

    env_var_ibm_creds = 'ibm-creds'
    ibm_creds = json.loads(os.environ[env_var_ibm_creds])

    url = ibm_creds['url']
    ibm_user = ibm_creds['user']
    ibm_password = ibm_creds['password']

    with TM1Service(base_url=url, user=ibm_user, password=ibm_password, namespace='LDAP', ssl=True) as tm1:
        Dimension = 'CRMSite'
        CRM_Attributes = tm1.power_bi.get_member_properties(
        dimension_name=Dimension,
        hierarchy_name=Dimension,
        member_selection="{Tm1SubsetAll([" + Dimension + "])}",
        skip_consolidations=True,
        skip_parents=False)
        Dimension = 'Time'
        Time_Attributes = tm1.power_bi.get_member_properties(
        dimension_name=Dimension,
        hierarchy_name=Dimension,
        member_selection="{Tm1SubsetAll([" + Dimension + "])}",
        skip_consolidations=True,
        #attributes=["" + Dimension + " Optimiser Description"],
        skip_parents=False).drop(columns='}SYS_TEMP_ATTRIBUTE')
        Dimension = 'Product'
        Product_Attributes = tm1.power_bi.get_member_properties(
        dimension_name=Dimension,
        hierarchy_name=Dimension,
        member_selection="{Tm1SubsetAll([" + Dimension + "])}",
        skip_consolidations=True,
        #attributes=["" + Dimension + " Optimiser Description"],
        skip_parents=False)

    CRM_Attributes['scenario_name'] = Version
    Time_Attributes['scenario_name'] = Version
    Product_Attributes['scenario_name'] = Version

    # clean column names
    CRM_Attributes.columns = clean_cols(CRM_Attributes)
    Time_Attributes.columns = clean_cols(Time_Attributes)
    Product_Attributes.columns = clean_cols(Product_Attributes)

    client = bigquery.Client(project=PROJECT)
    dataset_name = 'ibm'

    # delete scenario from table(s) if already there
    v_scenario_name = Version.lower()
    for d_t in ['lamb_ibm_crm_attributes','lamb_ibm_time_attributes', 'lamb_ibm_product_attributes']:
        try: # if doesn't exist then don't error.
            client.query(f"""
            DELETE FROM `{PROJECT}.{dataset_name}.{d_t}`
            WHERE lower(scenario_name) = '""" + v_scenario_name + """'
            """)
        except:
            f"no delete for v_scenario_name: {v_scenario_name}"


    # Write out to GCP  
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    job = client.load_table_from_dataframe(CRM_Attributes, f"{dataset_name}.lamb_ibm_crm_attributes", job_config=job_config)
    job = client.load_table_from_dataframe(Time_Attributes, f"{dataset_name}.lamb_ibm_time_attributes", job_config=job_config)
    job = client.load_table_from_dataframe(Product_Attributes, f"{dataset_name}.lamb_ibm_product_attributes", job_config=job_config)

    return {'CRM_Attributes':CRM_Attributes.to_json(orient='index'),
    'Time_Attributes':Time_Attributes.to_json(orient='index'),
    'Product_Attributes':Product_Attributes.to_json(orient='index'),
    }

def ibm_lamb_processing_fees(request):
    # Extracting MDX data and convert to a dataframe
    #Version = 'TEST'
    Version = request.form.get('scenario_name')

    env_var_ibm_creds = 'ibm-creds'
    ibm_creds = json.loads(os.environ[env_var_ibm_creds])

    url = ibm_creds['url']
    ibm_user = ibm_creds['user']
    ibm_password = ibm_creds['password']

    with TM1Service(base_url=url, user=ibm_user, password=ibm_password, namespace='LDAP', ssl=True) as tm1:

        Country =  "AU"
        Livestock =  "LAMB"

        mdx = """
        SELECT 
        {TM1SubsetToSet([Time].[Time],"FY Week Leaves","public")} ON 0, 
        {TM1SubsetToSet([Abattoir].[Abattoir],"Lamb Abattoirs","public")}*
        {TM1SubsetToSet([LivestockMeasure].[LivestockMeasure],"Processing Costs","public")} ON 1 
        FROM [LivestockModel] 
        WHERE (
        [Version].[Version].["""+Version+"""], [Livestock].[Livestock].[Lamb], [Contract].[Contract].[None]
        )
        """

        df = tm1.cubes.cells.execute_mdx_dataframe(mdx,skip_consolidated_cells=True,include_attributes=False,skip_zeros=False).fillna(0)

    df['scenario_name'] = Version

    print("printing df")
    print(df)

    client = bigquery.Client(project=PROJECT)
    table_id = 'ibm.ibm_lamb_processing_fees'

    v_scenario_name = Version.lower()

    sql = (
    f"""
    DELETE FROM `{PROJECT}.{table_id}`
    WHERE lower(scenario_name) = '""" + v_scenario_name + """'
    """
    )

    try: # if doesn't exist then don't error.
        client.query(sql)
    except:
        f"no delete for v_scenario_name: {v_scenario_name}"

    # Write out to GCP  
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

    return {'df':df.to_json(orient='index')}

def ibm_lamb_supplementary(request):
    # Extracting MDX data and convert to a dataframe
    #Version = 'TEST'
    Version = request.form.get('scenario_name')

    env_var_ibm_creds = 'ibm-creds'
    ibm_creds = json.loads(os.environ[env_var_ibm_creds])

    url = ibm_creds['url']
    ibm_user = ibm_creds['user']
    ibm_password = ibm_creds['password']

    with TM1Service(base_url=url, user=ibm_user, password=ibm_password, namespace='LDAP', ssl=True) as tm1:

        Country =  "AU"
        Livestock =  "LAMB"

        mdx = """
        SELECT {
        TM1SubsetToSet([Time].[Time],"FY Week Leaves","public")
        } ON 0, 
        {
        TM1SubsetToSet([CRMSite].[CRMSite],"Hilton Sites","public")}*
        {TM1SubsetToSet([Product].[Product],"Lamb Supp Products","public")}*
        {[SupplementaryMeasure].[SupplementaryMeasure].[Max Purchase Limit KG],
        [SupplementaryMeasure].[SupplementaryMeasure].[Min Purchase Limit KG],
        [SupplementaryMeasure].[SupplementaryMeasure].[Avg. Price/KG Limit]
        } ON 1 
        FROM [Supplementary] WHERE ([Version].[Version].["""+Version+"""])
        """

        df = tm1.cubes.cells.execute_mdx_dataframe(mdx,skip_consolidated_cells=True,include_attributes=False,skip_zeros=False).fillna(0)

    df['scenario_name'] = Version

    print("printing df")
    print(df)

    client = bigquery.Client(project=PROJECT)
    table_id = 'ibm.ibm_lamb_supplementary'

    v_scenario_name = Version.lower()

    sql = (
    f"""
    DELETE FROM `{PROJECT}.{table_id}`
    WHERE lower(scenario_name) = '""" + v_scenario_name + """'
    """
    )

    try: # if doesn't exist then don't error.
        client.query(sql)
    except:
        f"no delete for v_scenario_name: {v_scenario_name}"

    # Write out to GCP  
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

    return {'df':df.to_json(orient='index')}
