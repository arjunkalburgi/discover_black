import re, requests, json

def run(question):

    # parse 
    search_topic = re.match(r'I want to learn about (.*)', question)
    search_topic = search_topic.group(1)
    # print(search_topic)

    # query wikidata for desc
    api_url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=" + search_topic
    response = requests.get(api_url)
    if (response.status_code is not 200): 
        print("fail")
        quit()
        
    data = json.loads(response.content)
    extract = data[u'query'][u'pages'][data[u'query'][u'pages'].keys()[0]][u'extract'] # sorry
    # print(extract)

    # get actual title 
    title = data[u'query'][u'pages'][data[u'query'][u'pages'].keys()[0]][u'title'] # sorry
    # print(title)

    # query wikidata for topics
    level = 1
    sections = narrow(title, level)
    print("What about " + title + " would you like to learn?")
    for sec in sections: 
        print(sec["name"])

    


def narrow(title, level):
    
    # query wikidata for inner sections
    api_url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&prop=sections&page=" + title
    response = requests.get(api_url)
    if (response.status_code is not 200): 
        print("fail")
        quit()
        
    data = json.loads(response.content)

    moretopics = []
    for section in data[u'parse'][u'sections']: 
        if (int(section[u'level']) is (level+1)): 
            moretopics.append({"name": section[u'line'], "title": section[u'anchor']})
    return moretopics
    

# run("I want to learn about Finance")


def getres(title): 
    print("https://learn-anything.xyz/api/maps/?q=" + title.replace(" ", "+"))
    response = requests.get("https://learn-anything.xyz/api/maps/?q=" + title.replace(" ", "+"))
    if (response.status_code is not 200): 
        print("fail")
        quit()
        
    data = json.loads(response.content)

    dataa = [item for item in data if item.get('key') == unicode(title, "utf-8")]
    if len(dataa) is not 0: 
        response = requests.get("https://learn-anything.xyz/api/maps/" + dataa[0]['id'])
        if (response.status_code is not 200): 
            print("fail")
            quit()
            
        data = json.loads(response.content)
        dataaa = [{"title": item.get('nodes')[0]['text'], "url": item.get('nodes')[0]['url']} for item in data if len(item.get('nodes')) > 0]
        print(dataaa)
    else: 
        print("ugh")

getres("finance")

'''

[
    {u'category': u'wiki', u'url': u'http://www.wikiwand.com/en/Finance', u'fy': -198.72339255700297, u'fx': 166.524520158506, u'text': u'finance', u'nodes': []}, 
    {u'url': u'', u'text': u'interesting', u'nodes': [
        {u'category': u'blog', u'url': u'https://www.bloomberg.com/view/topics/money-stuff', u'fy': -90.82971845862471, u'fx': 670.7188228438229, u'text': u'articles by Matt Levine  \ufe0f', u'nodes': [], u'color': u'rgba(104, 255, 109, 1.0)'}], u'fx': 471.71882284382286, u'fy': -103.32971845862471}, 
        {u'category': u'mindmap', u'url': u'/economics/finance/financial-markets', u'fy': 110.53068161010742, u'fx': -279.38691329956055, u'text': u'financial markets  \ufe0f', u'nodes': []}, 
        {u'category': u'mindmap', u'url': u'/economics/finance/technical-analysis', u'fy': 112.34018325805664, u'fx': -37.26051712036133, u'text': u'technical analysis  \ufe0f', u'nodes': []}, 
        {u'category': u'mindmap', u'url': u'/economics/finance/forward-contracts', u'fy': 113.71540069580078, u'fx': 213.8391571044922, u'text': u'forward contracts  \ufe0f', u'nodes': []}, 
        {u'category': u'mindmap', u'url': u'/economics/finance/financial-services', u'fy': 118.30343018022546, u'fx': 465.89791358692537, u'text': u'financial services  \ufe0f', u'nodes': []}
]


[
    [
        {u'category': u'blog', 
         u'url': u'https://www.bloomberg.com/view/topics/money-stuff', 
         u'fy': -90.82971845862471, u'fx': 670.7188228438229,
         u'text': u'articles by Matt Levine  \ufe0f', 
         u'nodes': [],
         u'color': u'rgba(104, 255, 109, 1.0)'}
    ]
]
'''