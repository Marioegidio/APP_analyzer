import json
import sys
import glob
from collections import OrderedDict
from User import User
from utility import *

items = None
requests = []
domainsData = None
thirdPartSites = dict()
thirdPartSites_ios = dict()
thirdPartSites_android = dict()
attributes = None

with open("data/domains/domains.json") as domanisFile:
    domainsData = json.load(domanisFile)


if len(sys.argv) > 1:
    print(sys.argv[1])
    oS = sys.argv[1]
    if oS.lower() == "ios":
        osName = ["ios"]
        dataFile = dataFile + "iOS.json"
    elif oS.lower() == "android":
        osName = ["andorid"]
        dataFile = dataFile+"Android.json"
    else:
        Exception("Sistema Operativo non valido! (ios | android)")
else:
    osName = ["android", "ios"]
    dataFileNames = ["data/PII/data_Android.json", "data/PII/data_iOS.json"]


with open("data/domains/third_part_domains.json", 'w') as outJsonDomains:
    for oS in osName:
        user = None
        if oS == osName[0]:
            user = User(dataFileNames[0])
        else:
            user = User(dataFileNames[1])
        attributes = list(user.__dict__.keys())

        for testFile in glob.glob("data/testFiles_" + oS + "/*.har"):
            nomeFile = testFile.split('/')[2].split('.')[0]
            nomeApp = nomeFile.split('_')[0].lower()
            domainsList = domainsData[nomeApp]
            with open(testFile) as file:
                httpData = json.load(file)
                traffic = httpData["log"]["entries"]
                count = 0
                for index, entry in enumerate(traffic):
                    for item in entry:
                        raw = str(entry[item])
                        if (item == "request"):
                            if "url" in entry[item]:
                                requestUrl = entry[item]["url"]
                                splittedUrl = requestUrl.split(
                                    '://')[1].split('/')[0].split('.')
                                domain = splittedUrl[len(
                                    splittedUrl)-2] + "." + splittedUrl[len(splittedUrl)-1]

                                if domain not in domainsList:

                                    if oS == osName[0]:
                                        addDomain(thirdPartSites_android,
                                                  entry, nomeApp, domain, user, attributes)
                                    elif oS == osName[1]:
                                        addDomain(thirdPartSites_ios,
                                                  entry, nomeApp, domain, user, attributes)

                                    addDomain(thirdPartSites, entry,
                                              nomeApp, domain, user, attributes)

                                # else:
                                #     #generare file per siti non di terze parti
                                #     print("non faccio nulla")

# costruisco chart 1
buildChart1(thirdPartSites)

# costruisco chart2
buildChart2(thirdPartSites_ios, thirdPartSites_android)

# costruisco chart3
buildChart3(thirdPartSites, attributes)

# costruisco chart4
buildChart4(thirdPartSites_android, thirdPartSites_ios, attributes)

# costruisco chart5
buildChart5(thirdPartSites, "data/category.json", attributes)
with open("output.json", 'w') as outFile:
    json.dump(thirdPartSites, outFile)
