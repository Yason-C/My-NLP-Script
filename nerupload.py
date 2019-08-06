####Jason Croddy
###DEOI MongoDB to JSON-LD
##8/6/19
#The Polis Center
import pymongo
import spacy
import en_core_web_sm
from pyley import CayleyClient, GraphObject
import json

#Load Natural Language Processing (NLP)
nlp = en_core_web_sm.load()

#Connect to MongoDB instance
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#Query through the database to access DEOI entries
mydb = myclient["deoi"]
mycol = mydb["entries"]
#Query to pull the body of the entry for lanuage processing loop
mydoc = mycol.distinct('body', {}, {})
#Loop that queries through the database to find individual id and body of encyclopedia entries, and uses NLP to analyze the body text and discover/catagorize entities
for x in mydoc:
    #NLP of the body text
    doc = nlp(x)
    #nlp resturns a list of entities from the body, here I put them into a python list to loop through later
    ents = list(doc.ents)
    #Parses an ID from the entry
    myID = mycol.distinct('_id', {'body': x}, {})
    myID = str(myID)
    #Formats ID
    myID = myID[11:-3]
    #Loop will create specific JSON-LD entries for each text entity found in each encyclopedia entry
    for ent in doc.ents:
        #The data format for JSON-LD
        data: {
            "@type": "ListItem",
            "identifier": myID,
            "name": ent.text,
            "description": ent.label_
            }
        #Print data to console for validation
        print(myID, ent.text, ent.label_)
        #Save JSON data to a file
        with open('C:\\cayley_0.7.5_windows_amd64\\data\\testdata_.json', 'a') as json_file:  
           json.dump(data, json_file, indent=4)