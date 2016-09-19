#!/usr/bin/env python3

import json
import getpass
import argparse
import optparse

from watson_developer_cloud import AuthorizationV1
from watson_developer_cloud import NaturalLanguageClassifierV1



authFile = "auth.json"

def main():
	parser = argparse.ArgumentParser(description="Util method for Natural Language Processor")
	parser.add_argument('--trainingData', help='path to data file of training data')

	args = parser.parse_args()
	with open(authFile, 'r') as service_file:
	    service_data = json.loads(service_file.read())
	# authorize and get a token
	credentials = service_data['credentials']
	
	global nlc
	nlc = NaturalLanguageClassifierV1(
		username=credentials['username'],
		password=credentials['password']
	)
	
	sendTrainingData(args.trainingData)
	

def checkStatus(classifierId):
	classifiers = getClassifiers()
	print('Availible classifiers : ')
	for c in classifiers:
		print(c)
	classifierName = input('Choose a classifier' ) 
	status = nlc.status(classifiers[classifierName])
	print(json.dumps(status, indent=2))


def classify(classifierId, phrase):
	print(classifierId)
	result = nlc.classify(classifierId, phrase)
	print(json.dumps(result, indent=2))


def getClassifiers():
	classifiers = nlc.list()
	classifierNames = {}
	for i in classifiers['classifiers']:
		classifierNames ={ i['name'] : i['classifier_id'] }
	return classifierNames


def sendTrainingData(trainingFile): 
	classifiers = getClassifiers()
	print('Availible classifiers : ')
	for c in classifiers:
		print(c)
	print('use \'brutus-api\' for the backend classifier to decide which module to use')
	classifierName = input('What classifier are you training? (chose from above or enter new classifier' ) 
	with open(args.trainingFile, 'rb') as training_data:
		results = nlc.create(training_data=training_data, name=classifierName)
		print(json.dumps(results, indent=2))

	

if __name__ == "__main__":
	main()
