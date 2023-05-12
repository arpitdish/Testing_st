import streamlit as st
import pandas as pd
import csv
import json
import requests
import re

st.set_page_config(page_title="BPI Payload", layout="wide")


st.subheader("Welcome to BOT World! Tamanna")


option = st.selectbox("Select the attribute for which you need data", ('Compute Node', 'gnbdu'))

st.write('selected : ', option)



spectra = st.file_uploader("upload csv site", type={"csv", "txt"})
if spectra is not None:
    df = pd.read_csv(spectra, header= None)



nx1_data=pd.read_csv("New BPI Tracker - NX1(manual).csv",  low_memory=False)
planet_data=pd.read_csv("New BPI Tracker - Planet(manual).csv", low_memory=False)
sddc_data=pd.read_csv("New BPI Tracker - SDDC2(no_update) (1).csv")
cz_data=pd.read_csv("query_data_cz_final - Sheet1.csv", low_memory=False)


def cloudzone_name(site_id):
    row_num_5=cz_data[cz_data['site']==str(site_id)].index[0]
    cz_pandas=cz_data[cz_data['site']==str(site_id)]
    czname=str(cz_pandas['cz_data'][row_num_5])
    finaL_cz_name=  str(czname[-1])
    return finaL_cz_name 


def bmc_host_name(site_id):
    
    row_num_1=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    nx1_pandas=nx1_data[nx1_data['Site ID']==str(site_id)]
    server=str(nx1_pandas['DU Server Model'][row_num_1])
    
    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    server_vendor=str( planet_pandas['RAN_SW_VENDOR'][row_num_2])
    
    if server_vendor =='Mavenir':
        if server =='Supermicro':
            du_server='sm'
        else:
            du_server='xr'
    else:
        du_server='xr'
    bmc_h_name=str(site_id.lower())+"-"+str(du_server)+"-bmc"+"0001"+".paas.prod.corp.dish-wireless.net"
    return  bmc_h_name


def compute_resources(site_id):
    
    row_num_1=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    nx1_pandas=nx1_data[nx1_data['Site ID']==str(site_id)]
    server=str(nx1_pandas['DU Server Model'][row_num_1])
    
    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    server_vendor=str( planet_pandas['RAN_SW_VENDOR'][row_num_2])
    
    if server_vendor =='Mavenir':
        if server =='Supermicro':
            du_server='sm'
        else:
            du_server='xr'
    else:
        du_server='xr'
    cr=str(site_id.lower())+"-"+str(du_server)+"-srv"+"0001"+".paas.prod.corp.dish-wireless.net"
    return  cr


def du_nodeselector(site_id):
    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    server_vendor=str( planet_pandas['RAN_SW_VENDOR'][row_num_2])
    if server_vendor =='Mavenir':
        ven='mv'
    else:
        ven='ss'
        
    du=str(site_id.lower())+"-"+str(ven)
    
    return du


def resourse_pool_name(site_id):
    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    server_vendor=str( planet_pandas['RAN_SW_VENDOR'][row_num_2])
    if server_vendor =='Mavenir':
        ven='mv'
    else:
        ven='ss'
        
    rpn=str(site_id.lower())+"-"+str(ven)
    
    return rpn

def node_pool_name(site_id):
    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    server_vendor=str( planet_pandas['RAN_SW_VENDOR'][row_num_2])
    if server_vendor =='Mavenir':
        ven='mv'
    else:
        ven='ss'
        
    npn=str(site_id.lower())+"-"+str(ven)
    
    return npn


def site_vswitch(site_id):
    site_loc=str(site_id[0:2].lower())
    row_num_1=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    mgm_pandas=nx1_data[nx1_data['Site ID']==str(site_id)]
    cluster=str(mgm_pandas['Fiber Type'][row_num_1])
    if cluster == 'Lit':
        fibre='c'
    else:
        fibre='l'
    server=str(mgm_pandas['DU Server Model'][row_num_1])
    
    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    servor_ven_data=planet_pandas['RAN_SW_VENDOR'][row_num_2]
    
        
    if servor_ven_data=='Mavenir':
        if server =='Supermicro':
            du_server='sm'
        elif server =='Dell XR11':
            du_server='xr'
        else:
            du_server='dl'
        svs=site_loc+'0001'+str(fibre)+'-'+str(du_server)+"-"+str(cloudzone_name(site_id))+'-dvs01'
        return svs
    else:
        du_server='xr'
        svs=site_loc+'0001'+str(fibre)+'-'+str(du_server)+"-"+str(cloudzone_name(site_id))+'-dvs01'
        return svs

def engg_site_id(site_id):
    return site_id.lower()

def profile(site_id):
    
    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    servor_ven_data=planet_pandas['RAN_SW_VENDOR'][row_num_2]
    
    if servor_ven_data =='Mavenir':
        prf="mavenir-compute-v1"
    else:
        prf="samsung-compute-v"
    return prf

def gitlab_values(site_id):
    site_loc=str(site_id[0:2].lower())

    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    servor_ven_data=planet_pandas['RAN_SW_VENDOR'][row_num_2]
    
    if  servor_ven_data=='Mavenir':
        ran_vendors='mavenir'
    else:
        ran_vendors='samsung'
    
    gitv="https://cys001n-gitlab-p001.tools.corp.dish-wireless.net/"+str(ran_vendors)+"/du/"+str(site_loc)+"/"+str(site_id.lower())+".yaml"
    return  gitv

def gitlab_tag(site_id):
    aoi=str(site_id[2:5])
    
    
    row_num=sddc_data[sddc_data['AOI']==str(aoi)].index[0]
    sddc_pandas=sddc_data[sddc_data['AOI']==str(aoi)]
    region=sddc_pandas['AWS Region'][row_num]

    gitt='sddc-'+'us'+str(region.lower())+'-mno'
    return gitt

def parent_cluster(site_id):
    aoi=str(site_id[2:5])
    
    
    row_num=sddc_data[sddc_data['AOI']==str(aoi)].index[0]
    sddc_pandas=sddc_data[sddc_data['AOI']==str(aoi)]
    region=sddc_pandas['AWS Region'][row_num]

    sddc_n=sddc_pandas['Unnamed: 8'][row_num]
    sddc_no=int(re.findall(r'[\d]+',sddc_n)[0])
    final_sddc_no="{:03d}".format(sddc_no)

    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    k8_data=int(planet_pandas['CUSTOM_K8_ID_DUS'][row_num_2])
    final_k8_data="{:02d}".format(k8_data)

    servor_ven_data=planet_pandas['RAN_SW_VENDOR'][row_num_2]
    if servor_ven_data=='Mavenir':
        server_vendor='mv'
    else:
        server_vendor='ss'


    pc='us'+str(region.lower())+'mk'+str(final_sddc_no)+'-'+str(site_id[:2].lower())+str(final_k8_data)+"-"+str(server_vendor)+'01p'
    
    return pc 
    

def site_hostfolder(site_id):
    

    site_loc=str(site_id[0:2].lower())
    row_num_1=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    mgm_pandas=nx1_data[nx1_data['Site ID']==str(site_id)]
        
    server=str(mgm_pandas['DU Server Model'][row_num_1])
        
    cluster=str(mgm_pandas['Fiber Type'][row_num_1])
    if cluster == 'Lit':
        fibre='c'
    else:
        fibre='l'
            
    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    servor_ven_data=planet_pandas['RAN_SW_VENDOR'][row_num_2]
        
    if servor_ven_data=='Mavenir':
        if server =='Supermicro':
            du_server='sm'
        elif server =='Dell XR11':
            du_server='xr'
        else:
            du_server='dl'
        shf=site_loc+'0001'+str(fibre)+'-'+str(du_server)+'-'+str(cloudzone_name(site_id))

        return shf
    else:
        du_server='xr'
        shf=site_loc+'0001'+str(fibre)+'-'+str(du_server)+'-smsg-'+str(cloudzone_name(site_id))

        return  shf

data_final={}


def compute_node(site_id):
    data_final['site']=site_id
    data_final['bmc_host_names']=bmc_host_name(site_id)
    data_final['compute_resources']=compute_resources(site_id)
    data_final['du_nodeSelector']=du_nodeselector(site_id)
    data_final['resourcepool_names']=resourse_pool_name(site_id)
    data_final['nodepool_names']=node_pool_name(site_id)
    data_final['site_vswitch']=site_vswitch(site_id)
    data_final['engg_site_id']=engg_site_id(site_id)
    data_final['profile']=profile(site_id)
    data_final['gitlab_values']=gitlab_values(site_id)
    data_final['gitlab_tag']=gitlab_tag(site_id)
    data_final['parent_cluster']=parent_cluster(site_id)
    data_final['site_hostfolder']=site_hostfolder(site_id)
    data_final['site_vmfolder']=site_hostfolder(site_id)



def ptp_namespace(site_id):
    site_name = str(site_id).lower()
    
    row_num_1=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    kub_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    cluster=int(kub_pandas['CUSTOM_GNODEB_NAME'][row_num_1][-6:])
    
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    sddc_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    region=int(sddc_pandas['CUSTOM_GNODEB_SITE_NUMBER'][row_num])
    final_cluster_no="{:03d}".format(region)

    
    ptp_name=site_name+'-ns-ss-ptp-'+str(cluster)+'-'+str(final_cluster_no)
    
    return ptp_name

def du_namespace(site_id):
    site_name = str(site_id).lower()
    
    row_num_1=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    kub_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    cluster=int(kub_pandas['CUSTOM_GNODEB_NAME'][row_num_1][-6:])
    
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    sddc_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    region=int(sddc_pandas['CUSTOM_GNODEB_SITE_NUMBER'][row_num])
    final_cluster_no="{:03d}".format(region)

    
    du_name=site_name+'-ns-ss-du-'+str(cluster)+'-'+str(final_cluster_no)
    
    return du_name

def cnf_namespace(site_id):
    site_name = str(site_id).lower()
    
    row_num_1=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    kub_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    cluster=int(kub_pandas['CUSTOM_GNODEB_NAME'][row_num_1][-6:])
    
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    sddc_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    region=int(sddc_pandas['CUSTOM_GNODEB_SITE_NUMBER'][row_num])
    final_cluster_no="{:03d}".format(region)

    
    cnf_name=site_name+'-cnf-ss-du-'+str(cluster)+'-'+str(final_cluster_no)
    
    return cnf_name

def f1u_network(site_id):

    data_no=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    fib_type=nx1_data[nx1_data['Site ID']==str(site_id)]
    fib=fib_type['Fiber Type'][data_no]
    
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    ran_vendor=planet_data[planet_data['SITE_ID']==str(site_id)]
    ran_ven=ran_vendor['RAN_SW_VENDOR'][row_num]
            
    if ran_ven=='Mavenir':
        ran_vendors='mvnr'
        if fib=='Lit':
            fu_data='numa0-'+str(ran_vendors)+'-du-f1u-323'
            return fu_data
        else:
            fu_data="please contact for dark site"
            return fu_data
    else:
        ran_vendors='smsg'
        if fib=='Lit':
            fu_data='numa0-'+str(ran_vendors)+'-du-f1u-623'
            return fu_data
        else:
            fu_data="please contact for dark site"
            return fu_data

def radcup_network(site_id):

    data_no=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    fib_type=nx1_data[nx1_data['Site ID']==str(site_id)]
    fib=fib_type['Fiber Type'][data_no]
    
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    ran_vendor=planet_data[planet_data['SITE_ID']==str(site_id)]
    ran_ven=ran_vendor['RAN_SW_VENDOR'][row_num]
            
    if ran_ven=='Mavenir':
        ran_vendors='mvnr'
        if fib=='Lit':
            rcp='numa0-'+str(ran_vendors)+'-du-uplane-202'
            return rcp
        else:
            rcp="please contact for dark site"
            return rcp
    else:
        ran_vendors='smsg'
        rcp='do not need in samsung'
        return rcp

def global_nf_mtcilId(site_id):
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    ran_vendor=planet_data[planet_data['SITE_ID']==str(site_id)]
    ran_ven=ran_vendor['RAN_SW_VENDOR'][row_num]
    if ran_ven=='Mavenir':
        gnm="mtcil1"
        return gnm
    else:
        gnm='do not need in samsung'
        return gnm


def global_mtcil_kafka_svc_fqdn(site_id):
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    ran_vendor=planet_data[planet_data['SITE_ID']==str(site_id)]
    ran_ven=ran_vendor['RAN_SW_VENDOR'][row_num]
    if ran_ven=='Mavenir':
        gmf="kafka-svc.mvnr-mtcil1-inframgmt-mtcil-mtcil1.svc.cluster.local:9092"
        return gmf
    else:
        gmf='do not need in samsung'
        return gmf

def global_mtcil_etcd_svc_fqdn(site_id):
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    ran_vendor=planet_data[planet_data['SITE_ID']==str(site_id)]
    ran_ven=ran_vendor['RAN_SW_VENDOR'][row_num]
    if ran_ven=='Mavenir':
        gme="etcd.mvnr-mtcil1-inframgmt-mtcil-mtcil1.svc.cluster.local:2379"
        return gme
    else:
        gme='do not need in samsung'
        return gme

def f1c_port_group(site_id):

    data_no=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    fib_type=nx1_data[nx1_data['Site ID']==str(site_id)]
    fib=fib_type['Fiber Type'][data_no]
    
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    ran_vendor=planet_data[planet_data['SITE_ID']==str(site_id)]
    ran_ven=ran_vendor['RAN_SW_VENDOR'][row_num]
            
    if ran_ven=='Mavenir':
        ran_vendors='mvnr'
        if fib=='Lit':
            rcp='numa0-'+str(ran_vendors)+'-du-f1c-318'
            return rcp
        else:
            rcp="please contact for dark site"
            return rcp
    else:
        ran_vendors='smsg'
        rcp='do not need in samsung'
        return rcp

def mplane_port_group(site_id):

    data_no=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    fib_type=nx1_data[nx1_data['Site ID']==str(site_id)]
    fib=fib_type['Fiber Type'][data_no]
    
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    ran_vendor=planet_data[planet_data['SITE_ID']==str(site_id)]
    ran_ven=ran_vendor['RAN_SW_VENDOR'][row_num]
            
    if ran_ven=='Mavenir':
        ran_vendors='mvnr'
        if fib=='Lit':
            rcp='numa0-'+str(ran_vendors)+'-du-mplane-201'
            return rcp
        else:
            rcp="please contact for dark site"
            return rcp
    else:
        ran_vendors='smsg'
        rcp='do not need in samsung'
        return rcp

def uplane_port_group(site_id):

    data_no=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    fib_type=nx1_data[nx1_data['Site ID']==str(site_id)]
    fib=fib_type['Fiber Type'][data_no]
    
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    ran_vendor=planet_data[planet_data['SITE_ID']==str(site_id)]
    ran_ven=ran_vendor['RAN_SW_VENDOR'][row_num]
            
    if ran_ven=='Mavenir':
        ran_vendors='mvnr'
        if fib=='Lit':
            rcp='numa0-'+str(ran_vendors)+'-du-uplane-202'
            return rcp
        else:
            rcp="please contact for dark site"
            return rcp
    else:
        ran_vendors='smsg'
        rcp='do not need in samsung'
        return rcp


def k_mgmt_port_group(site_id):

    data_no=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    fib_type=nx1_data[nx1_data['Site ID']==str(site_id)]
    fib=fib_type['Fiber Type'][data_no]
    
    row_num=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    ran_vendor=planet_data[planet_data['SITE_ID']==str(site_id)]
    ran_ven=ran_vendor['RAN_SW_VENDOR'][row_num]
            
    if ran_ven=='Mavenir':
        ran_vendors='mvnr'
        if fib=='Lit':
            rcp='numa0-'+str(ran_vendors)+'-k8s-mgmt-311'
            return rcp
        else:
            rcp="please contact for dark site"
            return rcp
    else:
        ran_vendors='smsg'
        rcp='do not need in samsung'
        return rcp

def vmc_Segment_mtcil(site_id):
    site_loc=str(site_id[0:2])
    aoi=str(site_id[2:5])
    
    row_num_1=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    kub_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    cluster=int(kub_pandas['CUSTOM_K8_ID_DUS'][row_num_1])
    final_cluster_no="{:02d}".format(cluster)
    
    row_num=sddc_data[sddc_data['AOI']==str(aoi)].index[0]
    sddc_pandas=sddc_data[sddc_data['AOI']==str(aoi)]
    region=sddc_pandas['AWS Region'][row_num]
    sddc_n=sddc_pandas['Unnamed: 8'][row_num]
    sddc_no=int(re.findall(r'[\d]+',sddc_n)[0])
    
    final_sddc_no="{:03d}".format(sddc_no)
    vmc_Segment_mtcil='NET-VM-TKG'+str(final_cluster_no)+site_id[0:2]+'-MTCIL-CMN-'+'US'+str(region)+'AZ12RANMK'+str(final_sddc_no)
    return vmc_Segment_mtcil

def mgmt_pot_group(site_id):
    site_loc=str(site_id[0:2].lower())
    row_num_1=nx1_data[nx1_data['Site ID']==str(site_id)].index[0]
    mgm_pandas=nx1_data[nx1_data['Site ID']==str(site_id)]
    cluster=str(mgm_pandas['Fiber Type'][row_num_1])
    if cluster == 'Lit':
        fibre='c'
    else:
        fibre='l'
    server=str(mgm_pandas['DU Server Model'][row_num_1])
    
    row_num_2=planet_data[planet_data['SITE_ID']==str(site_id)].index[0]
    planet_pandas=planet_data[planet_data['SITE_ID']==str(site_id)]
    servor_ven_data=planet_pandas['RAN_SW_VENDOR'][row_num_2]
    
        
    if servor_ven_data=='Mavenir':
        if server =='Supermicro':
            du_server='sm'
        elif server =='Dell XR11':
            du_server='xr'
        else:
            du_server='dl'
        svs=site_loc+'0001'+str(fibre)+'-'+str(du_server)+"-"+str(cloudzone_name(site_id))+'-mgmt-96'
        return svs
    else:
        du_server='xr'
        svs=site_loc+'0001'+str(fibre)+'-'+str(du_server)+"-"+str(cloudzone_name(site_id))+'-mgmt-96'
        return svs

def gnbdu(site_id):
    data_final['site']=site_id
    data_final['du_namespace']=du_namespace(site_id)
    data_final['ptp_namespace']=ptp_namespace(site_id)
    data_final['f1u_network']=f1u_network(site_id)
    data_final['radcup_network']=radcup_network(site_id)
    data_final['global_nf_mtcilId']=global_nf_mtcilId(site_id)
    data_final['global_mtcil_kafka_svc_fqdn']=global_mtcil_kafka_svc_fqdn(site_id)
    data_final['global_mtcil_etcd_svc_fqdn']=global_mtcil_etcd_svc_fqdn(site_id)
    data_final['mgmt_port_group']=mgmt_pot_group(site_id)
    data_final['f1c_portGroup']=f1c_port_group(site_id)
    data_final['mplane_portGroup']=mplane_port_group(site_id)
    data_final['uplane_portGroup']=uplane_port_group(site_id)
    data_final['k8s_mgmt_portGroup']=k_mgmt_port_group(site_id)
    data_final['vmc_segment_mtcil']=vmc_Segment_mtcil(site_id)
    data_final['cnf_name']=cnf_namespace(site_id)



if option=='Compute Node':
	df2=pd.DataFrame()
	for site in df[0]:
	    compute_node(site)
	    df1 = pd.json_normalize(data_final)
	    df2 = pd.concat([df2, df1], ignore_index=True)

else:
	df2=pd.DataFrame()
	for site in df[0]:
	    gnbdu(site)
	    df1 = pd.json_normalize(data_final)
	    df2 = pd.concat([df2, df1], ignore_index=True)






def convert_df(df):
   return df.to_csv(index=False)


csv = convert_df(df2)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)