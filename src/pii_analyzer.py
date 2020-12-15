import json
import sys
import glob
import src.User as User


print(sys.argv[1])

oS = sys.argv[1]
dataFile = "data/PII/data_"
if oS.lower() == "ios":
    dataFile = dataFile + "iOS.json"
elif oS.lower() == "android":
    dataFile = dataFile+"Android.json"
else:
    Exception("Sistema Operativo non valido! (ios | android)")

# appname = sys.argv[1]
user = User(dataFile)
attributes = list(user.__dict__.keys())
items = None
requests = []

for testFile in glob.glob("testFiles_" + oS + "/*.har"):
    nomeFile = testFile.split('/')[1].split('.')[0]
    print(nomeFile)
    with open("Output/Out_"+ nomeFile + ".txt", 'a') as outTxtFile:
        with open(testFile) as file:
            httpData = json.load(file)

            traffic = httpData["log"]["entries"]
            count = 0
            for index, entry in enumerate(traffic):
                for item in entry:
                    raw = str(entry[item])
                    for attribute in attributes:
                        if type(getattr(user, attribute)) == list:
                            for value in getattr(user, attribute):
                                # if (item == "request"):
                                if(value.lower() in raw.lower()):
                                    if "url" in entry[item]:
                                        outTxtFile.write("\n>> ["+str(index)+"] " + attribute + " = " + value +
                                                         "\n   " + str(entry[item]["url"]))
                                        requests.append(entry)
                                    else:
                                        outTxtFile.write("\n>> ["+str(index)+"] " + attribute + " = " + value +
                                                         "\n   ")

                        else:
                            # if (item == "request"):
                            if(getattr(user, attribute).lower() in raw.lower()):

                                if "url" in entry[item]:
                                    outTxtFile.write("\n>> ["+str(index)+"] " + attribute + " = " + getattr(user, attribute) +
                                                     "\n   " + str(entry[item]["url"]))
                                else:
                                    outTxtFile.write("\n>> ["+str(index)+"] " + attribute + " = " + getattr(user, attribute) +
                                                     "\n   ")

                                requests.append(entry)

    with open("Output/Out_" + nomeFile + ".json", 'w') as outFile:
        json.dump(requests, outFile)
