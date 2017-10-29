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
    print(title)
    
    # query wikidata for topics
    

run("I want to learn about Finance")


'''

ask.run("I want to learn about Finance")


'''