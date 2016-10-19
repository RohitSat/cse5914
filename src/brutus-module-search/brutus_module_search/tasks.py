from flask import json

from .app import app
import json
from watson_developer_cloud import RetrieveAndRankV1


def find_document(question):
    """
    user rank and retrieve to find the appropriate 
    document and return the answer to the users question
    """

    retrieve_and_rank = RetrieveAndRankV1(
                username=app.config['RAR_WATSON_USERNAME'],
                password=app.config['RAR_WATSON_PASSWORD'])
    
    # Solr clusters
    solr_clusters = retrieve_and_rank.list_solr_clusters()
    pysolr_client = retrieve_and_rank.get_pysolr_client(
        app.config['RAR_WATSON_CLUSTER_ID'], 
        app.config['RAR_WATSON_COLLECTION_NAME'])
    
    results = pysolr_client.search(question)
    if(len(results.docs) > 0): 
        return results.docs[0]['body']
    
    # no results found
    # TODO better error handling but this is due tomorrow.. 
    return "I am sorry I was unable to find an answer to your question" 
