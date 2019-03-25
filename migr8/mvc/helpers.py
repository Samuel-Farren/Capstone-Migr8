from watson_developer_cloud import RetrieveAndRankV1
from watson_developer_cloud import NaturalLanguageClassifierV1
from mvc import credential as cred
import eventlet
import json
import os
import re
from bs4 import BeautifulSoup

#returns status of watson server or a status message if watson is unable to be reached.
def WatsonStatus():
    retrieve_and_rank = RetrieveAndRankV1(
    username=cred.RRUSER,
    password=cred.RRPASS)
    nlc = NaturalLanguageClassifierV1(
        username=cred.NLCUSER,
        password=cred.NLCPASS
    )
    status = {}
    status2 = {}
    timeout = eventlet.Timeout(3, True)
    try:
        status2 = nlc.status(cred.NLCCLUSTER)
        status = retrieve_and_rank.get_solr_cluster_status(
        solr_cluster_id=cred.CLUSTERID)
    except:
        status = { "solr_cluster_status":"Retrieve and Rank Unable to be Reached."}
        status2 = { "status_description":"Natural Language Classifier Unable to be reached"}
    finally:
        timeout.cancel()
    return status["solr_cluster_status"], status2["status_description"]

def rrQuery(query, cluster, col):
    retrieve_and_rank = RetrieveAndRankV1(
    username=cred.RRUSER,
    password=cred.RRPASS)
    results = {}
    try:
        pysolr_client = retrieve_and_rank.get_pysolr_client(cluster, col)
        results = pysolr_client.search(query).docs
    except:
        results = {}
    return results

def extractData(docs):
    cities = [os.path.splitext(str(doc["fileName"]))[0].replace("_", " ").title() for doc in docs]
    bodies = [doc["body"] for doc in docs]
    return cities, bodies

def nlcQuery(query):
    natural_language_classifier = NaturalLanguageClassifierV1(
    username=cred.NLCUSER,
    password=cred.NLCPASS)
    #status = natural_language_classifier.status(cred.NLCCLUSTER)

    try:
        classes = natural_language_classifier.classify(cred.NLCCLUSTER,query)
        results = classes['top_class']
    except:
        results = {}
    return results

def replace_custom_tags(body):
    temp = re.sub(r'\[(\S*?)( .*?)*?\]', '[\g<1>]', body)
    temp = re.sub(r'\[a\](.*?)\[/a\]', '\g<1>', temp)

    temp = re.sub(r'\[h.\]$', '', temp)
    temp = re.sub(r'^\[/h.\]', '', temp)
    temp = re.sub(r'\[div\]\s*$', '', temp)
    temp = re.sub(r'\[/div\]\s*$', '', temp)

    temp = re.sub(r'\[/(.*?)\]', '</\g<1>>', re.sub(r'\[([^/]*?)\]', '<\g<1>>', temp))
    #return BeautifulSoup(temp, "html.parser").prettify()
    return temp