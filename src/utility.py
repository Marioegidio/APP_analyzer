import plotly.express as px
import plotly.graph_objects as go
import json
import re

colors = ["#FF7069", "#F5FF38", "#2FD3F6", "#0006F5",
          "#07AD23", "#C000F5", "#141414", "#CC1514", "#01F6C1"]


def buildDataForChart(sites, typeOfChart, fileName=None):
    dataForChart = list()
    chartDict = dict()
    tempDict = dict()
    categoryData = None
    if typeOfChart == 5:
        with open(fileName) as categoryFile:
            categoryData = json.load(categoryFile)

    for site in sites:
        requestNumber = 0
        leaksNumber = 0
        leakDict = dict()

        if typeOfChart == 1:
            for appName in sites[site]:
                requestNumber = requestNumber + \
                    len(sites[site][appName]["requestList"])
            dataForChart.append((site, requestNumber))

        elif typeOfChart == 2:
            for appName in sites[site]:
                if appName in tempDict:
                    tempDict[appName] = tempDict[appName] + \
                        len(sites[site][appName]["requestList"])
                else:
                    tempDict.update(
                        {appName: len(sites[site][appName]["requestList"])})
            dataForChart.append((site, requestNumber))

        elif typeOfChart == 3:
            for appName in sites[site]:
                for leaksName in sites[site][appName]["leakList"]:
                    # print(leaksName)
                    if leaksName in leakDict:
                        leakDict[leaksName] = leakDict[leaksName] + \
                            sites[site][appName]["leakList"][leaksName]
                    else:
                        leakDict.update(
                            {leaksName: sites[site][appName]["leakList"][leaksName]})
                    leaksNumber = leaksNumber + \
                        sites[site][appName]["leakList"][leaksName]
            chartDict.update(
                {site: {"leaks": leakDict, "leaksNumber": leaksNumber}})

        elif typeOfChart == 4:
            for appName in sites[site]:
                leakDict = dict()
                leaksNumber = 0
                for leaksName in sites[site][appName]["leakList"]:
                    leakDict.update(
                        {leaksName: sites[site][appName]["leakList"][leaksName]})
                    leaksNumber = leaksNumber + \
                        sites[site][appName]["leakList"][leaksName]
                if appName in chartDict:
                    for leak in leakDict:
                        if leak in chartDict[appName]["leaks"]:
                            chartDict[appName]["leaks"][leak] = chartDict[appName]["leaks"][leak] + leakDict[leak]
                        else:
                            chartDict[appName]["leaks"].update(
                                {leak: leakDict[leak]})
                    chartDict[appName]["leaksNumber"] = chartDict[appName]["leaksNumber"] + leaksNumber
                else:
                    chartDict.update(
                        {appName: {"leaks": leakDict, "leaksNumber": leaksNumber}})

        elif typeOfChart == 5:

            for appName in sites[site]:
                leakDict = dict()
                leaksNumber = 0
                for leaksName in sites[site][appName]["leakList"]:
                    leakDict.update(
                        {leaksName: sites[site][appName]["leakList"][leaksName]})
                    leaksNumber = leaksNumber + \
                        sites[site][appName]["leakList"][leaksName]
                if appName in tempDict:
                    for leak in leakDict:
                        if leak in tempDict[appName]["leaks"]:
                            tempDict[appName]["leaks"][leak] = tempDict[appName]["leaks"][leak] + leakDict[leak]
                        else:
                            tempDict[appName]["leaks"].update(
                                {leak: leakDict[leak]})
                    tempDict[appName]["leaksNumber"] = tempDict[appName]["leaksNumber"] + leaksNumber
                else:
                    tempDict.update(
                        {appName: {"leaks": leakDict, "leaksNumber": leaksNumber}})
    if typeOfChart == 5:
        for popolarity in categoryData:
            popDict = {popolarity: dict()}
            for category in categoryData[popolarity]:
                for appName in categoryData[popolarity][category]:
                    if appName in tempDict:
                        if category in popDict[popolarity]:
                            # TODO aggiungere codice per poter testare più app della stessa categoria
                            print("non capiterà")
                        else:
                            popDict[popolarity].update({category: {
                                                        "leaks": tempDict[appName]["leaks"], "leaksNumber": tempDict[appName]["leaksNumber"]}})

            chartDict.update(popDict)

    if typeOfChart == 3 or typeOfChart == 4 or typeOfChart == 5:
        return chartDict

    if typeOfChart == 2:
        dataForChart = [(k, v) for k, v in tempDict.items()]

    return sorted(dataForChart, key=lambda tup: tup[1], reverse=True)


def addDomain(sites, entry, nomeApp, domain, user, attributes):
    if domain not in sites:
        sites[domain] = dict()
        dictRequest = {nomeApp: {"requestList": list(), "leakList": dict()}}
        dictRequest[nomeApp]["requestList"].append(entry)
        sites[domain].update(
            dictRequest)
    else:
        if nomeApp not in sites[domain]:
            dictRequest = {
                nomeApp: {"requestList": list(), "leakList": dict()}}
            dictRequest[nomeApp]["requestList"].append(
                entry)
            sites[domain].update(
                dictRequest)
        else:
            sites[domain][nomeApp]["requestList"].append(
                entry)
    findLeak(entry, user, sites[domain][nomeApp]["leakList"], attributes)


def old_findLeak(entry, user, leakDict, attributes):
    raw = str(entry)
    for attribute in attributes:
        if type(getattr(user, attribute)) == list:
            for value in getattr(user, attribute):
                value = value.replace("+", "\+")
                value = value.replace(".", "\.")
                if(re.search(value, raw.lower())):
                    if attribute in leakDict:
                        leakDict[attribute] = leakDict[attribute] + 1
                    else:
                        leakDict.update({attribute: 1})
        else:
            value = getattr(user, attribute).lower()
            value = value.replace("+", "\+")
            value = value.replace(".", "\.")
            # if(re.search("\\b"+value+"\\b", raw.lower())):
            if(re.search(value, raw.lower())):
                if attribute in leakDict:
                    leakDict[attribute] = leakDict[attribute] + 1
                else:
                    leakDict.update({attribute: 1})


def findLeak(entry, user, leakDict, attributes):
    raw = str(entry)
    for attribute in attributes:
        if type(getattr(user, attribute)) == list:
            for value in getattr(user, attribute):
                if(value.lower() in raw.lower()):
                    if attribute in leakDict:
                        leakDict[attribute] = leakDict[attribute] + 1
                    else:
                        leakDict.update({attribute: 1})
        else:
            if(getattr(user, attribute).lower() in raw.lower()):
                if attribute in leakDict:
                    leakDict[attribute] = leakDict[attribute] + 1
                else:
                    leakDict.update({attribute: 1})


def buildChart1(thirdPartSites, desc=""):
    # indica il primo grafico definito nell'analisi
    chart1 = {"sites": list(), "requests": list(), }

    # costruisco chart1
    dataForChart1 = buildDataForChart(thirdPartSites, 1)
    for item in dataForChart1[:15]:
        chart1["sites"].append(item[0])
        chart1["requests"].append(item[1])

    # fig = px.bar(chart1, x='sites', y='requests')
    fig = go.Figure(data=[
        go.Bar(name="AllApp",  x=chart1["sites"], y=chart1["requests"], text=chart1["requests"], textfont={'size': 15},
               textposition='outside', marker_line_width=0.5, marker_line_color='rgb(8,48,107)', opacity=0.85,),
    ])
    # Change the bar mode
    fig.update_layout(xaxis={"title": "Domini"}, yaxis={"title": "#Richieste"}, barmode='group',  font={
                      "size": 20}, title=("Numero richieste a siti di terze parti"+desc.strip()+""))
    fig.show()
    # fine chart1


def buildChart2(thirdPartSites_ios, thirdPartSites_android, desc=""):

    # indica il secodno grafico definito nell'analisi
    chart2_android = {"apps": list(), "requests": list(), }
    chart2_ios = {"apps": list(), "requests": list(), }

    # costruisco chart2
    dataForChart2_android = buildDataForChart(thirdPartSites_android, 2)
    dataForChart2_ios = buildDataForChart(thirdPartSites_ios, 2)

    for item in dataForChart2_android:
        chart2_android["apps"].append(item[0])
        chart2_android["requests"].append(item[1])
    for item in dataForChart2_ios:
        chart2_ios["apps"].append(item[0])
        chart2_ios["requests"].append(item[1])

    fig = go.Figure(data=[
        go.Bar(name="iOS",  x=chart2_ios["apps"], y=chart2_ios["requests"], text=chart2_ios["requests"], textfont={'size': 15},
               textposition='outside', marker_line_width=0.5, marker_line_color='rgb(8,48,107)', opacity=0.85),
        go.Bar(name="Android",
               x=chart2_android["apps"], y=chart2_android["requests"], text=chart2_android["requests"], textfont={'size': 15}, textposition='outside', marker_line_width=0.5, marker_line_color='rgb(8,48,107)', opacity=0.85)
    ])
    # Change the bar mode
    fig.update_layout(xaxis={"title": "Apps"}, yaxis={"title": "#Richieste"}, barmode='group',  font={
                      "size": 20}, title=("Numero rischieste a siti di terze parti"+desc.strip()+" (iOS/Android)"))
    fig.show()
    # fine chart2


def buildChart3(thirdPartSites, attributes, desc=""):

    # indica il terzo grafico definito nell'analisi
    chart3 = {"sites": list(), "leaks": list(dict()), }

    # costruisco chart3
    dataForChart3 = buildDataForChart(thirdPartSites, 3)
    dataForChart3 = {k: v for k, v in sorted(
        dataForChart3.items(), key=lambda item: item[1]["leaksNumber"], reverse=True)[:15]}
    # print(dataForChart3)
    dataCreated = list()
    for index, attribute in enumerate(attributes):
        leakValue = list()

        siteList = list()
        for site in dataForChart3:
            siteList.append(site)
            if attribute in dataForChart3[site]["leaks"]:
                leakValue.append(dataForChart3[site]["leaks"][attribute])

            else:
                leakValue.append(0)

        dataCreated.append(go.Bar(name=attribute, x=siteList,
                                  y=leakValue, marker_color=colors[index]))

    fig = go.Figure(data=dataCreated,)
    fig.update_layout(xaxis={"title": "Domini"}, yaxis={"title": "#PII leaks"}, barmode='stack',  font={
                      "size": 20}, title=("Leaks siti di terze parti"+desc.strip()+""))
    fig.show()
    # fine chart3


def buildChart4(thirdPartSites_android, thirdPartSites_ios, attributes, desc=""):

    # indica il secodno grafico definito nell'analisi
    chart4_android = {"apps": list(), "requests": list(), }
    chart4_ios = {"apps": list(), "requests": list(), }

    # costruisco chart4
    dataForChart4_android = buildDataForChart(thirdPartSites_android, 4)
    dataForChart4_ios = buildDataForChart(thirdPartSites_ios, 4)
    dataForChart4_android = {k: v for k, v in sorted(
        dataForChart4_android.items(), key=lambda item: item[1]["leaksNumber"], reverse=True)[:22]}
    dataForChart4_ios = {k: v for k, v in sorted(
        dataForChart4_ios.items(), key=lambda item: item[1]["leaksNumber"], reverse=True)[:22]}

    dataCreated_android = list()
    dataCreated_ios = list()

    for index, attribute in enumerate(attributes):
        leakValue = list()
        appList = list()
        for app in dataForChart4_android:
            appList.append(app)
            if attribute in dataForChart4_android[app]["leaks"]:
                leakValue.append(
                    dataForChart4_android[app]["leaks"][attribute])
            else:
                leakValue.append(0)
        dataCreated_android.append(
            go.Bar(name=attribute, x=appList, y=leakValue, marker_color=colors[index]))
        appList = list()
        leakValue = list()
        for app in dataForChart4_ios:
            appList.append(app)
            if attribute in dataForChart4_ios[app]["leaks"]:
                leakValue.append(dataForChart4_ios[app]["leaks"][attribute])
            else:
                leakValue.append(0)
        dataCreated_ios.append(
            go.Bar(name=attribute, x=appList, y=leakValue, marker_color=colors[index]))

    fig_android = go.Figure(data=dataCreated_android)
    fig_android.update_layout(barmode='stack', xaxis={"title": "Apps"}, yaxis={"title": "#PII leaks"}, font={
                              "size": 20}, title=("App Android (siti di terze parti"+desc.strip()+")"))
    fig_android.show()

    fig_ios = go.Figure(data=dataCreated_ios)
    fig_ios.update_layout(xaxis={"title": "Apps"}, yaxis={"title": "#PII leaks"}, barmode='stack',  font={
                          "size": 20}, title=("App iOS (siti di terze parti"+desc.strip()+")"),)
    fig_ios.show()
    # fine chart4


def buildChart5(thirdPartSites, fileName, attributes, desc=""):

    # indica il quinto grafico definito nell'analisi
    # costruisco chart5
    dataForChart5 = buildDataForChart(thirdPartSites, 5, fileName)

    dataForChart5["popolari"] = {k: v for k, v in sorted(
        dataForChart5["popolari"].items(), key=lambda item: item[1]["leaksNumber"], reverse=True)[:22]}
    dataForChart5["non_popolari"] = {k: v for k, v in sorted(
        dataForChart5["non_popolari"].items(), key=lambda item: item[1]["leaksNumber"], reverse=True)[:22]}

    dataCreated_pop = list()
    dataCreated_nonPop = list()

    for index, attribute in enumerate(attributes):
        leakValue = list()
        CatList = list()
        for category in dataForChart5["popolari"]:
            CatList.append(category)
            if attribute in dataForChart5["popolari"][category]["leaks"]:
                leakValue.append(
                    dataForChart5["popolari"][category]["leaks"][attribute])
            else:
                leakValue.append(0)
        dataCreated_pop.append(
            go.Bar(name=attribute, x=CatList, y=leakValue,  marker_color=colors[index]))
        CatList = list()
        leakValue = list()
        for category in dataForChart5["non_popolari"]:
            CatList.append(category)
            if attribute in dataForChart5["non_popolari"][category]["leaks"]:
                leakValue.append(
                    dataForChart5["non_popolari"][category]["leaks"][attribute])
            else:
                leakValue.append(0)

        dataCreated_nonPop.append(
            go.Bar(name=attribute, x=CatList, y=leakValue, marker_color=colors[index]))

    fig_pop = go.Figure(data=dataCreated_pop)
    fig_pop.update_layout(barmode='stack', xaxis={"title": "Categorie"}, yaxis={"title": "#PII leaks"}, font={"size": 20},  title=("Leaks App Popolari (siti di terze parti"+desc.strip()+")"),)
    fig_pop.show()

    fig_non_pop = go.Figure(data=dataCreated_nonPop)
    fig_non_pop.update_layout(xaxis={"title": "Categorie"}, yaxis={"title": "#PII leaks"}, barmode='stack',   font={"size": 20}, title=("Leaks App Non Popolari (siti di terze parti"+desc.strip()+")"),)
    fig_non_pop.show()
    # fine chart5


# // relazione
# // tab permessi
# // geo
