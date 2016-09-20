import json
import getpass

from watson_developer_cloud import AuthorizationV1
from watson_developer_cloud import NaturalLanguageClassifierV1


#TODO put this somewhere that it can be used by other modules if needed
class Nlp(object):
    
    classifierId = None
    nlc = None
    
    
    def __init__(self, username, password, classifierName):
        self.nlc = NaturalLanguageClassifierV1(
            username=username,
            password=password
        )
        classifiers = self.__getClassifiers()
        self.classifierId = classifiers[classifierName]
    
    
    def __getClassifiers(self):
        classifiers = self.nlc.list()
        classifierNames = {}
        for i in classifiers['classifiers']:
            classifierNames = {i['name']: i['classifier_id']}
            print(i['name'])
        return classifierNames
    
    def checkStatus(self):
        return self.nlc.status(self.classifierId)
    
    
    def classify(self, text):
        result = self.nlc.classify(self.classifierId, text)
        module = ""
        highestPercent = 0
        for i in result['classes']:
           if(i['confidence'] > highestPercent):
                module = i['class_name'] 
        return module
