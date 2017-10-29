"""The main command for asking questions"""

from .base import Base
import re, requests, json, inquirer, unicodedata, Algorithmia

full_api = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=" 
description_api = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=" 
        

class Want(Base):
    """Print the user's question"""

    def run(self):
        # parse 
        search_topic = "_".join(self.options['<topic>'])
        self.getdesc(search_topic, description_api + search_topic)


    def getdesc(self, search_topic, description_api_url): 
        
        # query wikidata for desc
        response = requests.get(description_api_url)
        if (response.status_code is not 200): 
            print("fail")
            quit()
            
        data = json.loads(response.content)
        extract = data[u'query'][u'pages'][data[u'query'][u'pages'].keys()[0]]

        if (u'revisions' in extract): 
            # is the redirect
            revisions = extract[u'revisions'][0][u'*']
            revisions = revisions.replace("[", "")
            revisions = revisions.replace("]", "")
            redirectstringintermediate = re.match(r'#REDIRECT (.*)', revisions) 
            redirectstring = redirectstringintermediate.group(1)
            print(search_topic + " is redirecting to " + redirectstring)
            redirectstring = redirectstring.replace(" ", "_")

            self.getdesc(redirectstring, description_api + redirectstring)

        elif (u'extract' in extract and extract[u'extract'] is not u'') : 
            # is the proper description
            client = Algorithmia.client('simDyTFFYXL1fSEX+m50s4r4NbK1')
            algo = client.algo('nlp/Summarizer/0.1.6')
            result = algo.pipe([extract[u'extract'], 2]).result
            print(result)

            self.findsections(data)

        else: 
            # called intro api on a full api
            # get the intro one
            self.getdesc(search_topic, full_api + search_topic)


    def findsections(self, data): 
        # get actual title 
        title = data[u'query'][u'pages'][data[u'query'][u'pages'].keys()[0]][u'title'] # sorry
        # print(title)

        # query wikidata for sections
        level = 1
        sections = self.narrow(title, level)

        # TODO no sections

        # make user select from sections
        print("\nWhat about " + title + " would you like to learn?")
        self.selectnext(sections, title)


    def selectnext(self, sections, title): 
        questions = [
                inquirer.List('size',
                                message="Check these",
                                choices=[sec["name"] for sec in sections],
                ),
            ]
        answers = inquirer.prompt(questions)

        nextt = sections[[sec["name"] for sec in sections].index(answers["size"])]
        # give me resources 
        if [sec['name'] for sec in sections].index(answers["size"]) is 0: 
            res = self.getres(title)
            if (len(res) > 0): 
                print("Saving resources...")
                print([item['title'] for item in res])
                print("Above has been saved to your library")
            else: 
                print("resource lookup error")
            quit()
        # go back
        elif (answers["size"] is "Back"): 
            self.selectnext(nextt["sections"], nextt["title"])
        # subcategories 
        elif ("more" in nextt): 
            print("There are subcategories!")
            nextt["more"].append({"name": "Back", "title": title, "sections": sections})
            self.selectnext(nextt["more"], nextt["name"])
        # search new
        else: 
            self.getdesc(nextt["name"], description_api + nextt["title"])


    def narrow(self, title, level):
        
        # query wikidata for inner sections
        api_url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&prop=sections&page=" + title
        response = requests.get(api_url)
        if (response.status_code is not 200): 
            print("fail")
            quit()
            
        data = json.loads(response.content)

        moretopics = []
        moretopics.append({"name": "Give me resources about " + title, "title": title})
        for i, section in enumerate(data[u'parse'][u'sections']): 
            if (int(section[u'level']) is (level+1)): 
                moretopics.append({"name": unicodedata.normalize('NFKD', section[u'line']).encode('ascii','ignore'), "title": unicodedata.normalize('NFKD', section[u'anchor']).encode('ascii','ignore')})
            elif (int(section[u'level']) is (level+2)):
                if "more" in moretopics[-1]: 
                    moretopics[-1]["more"].append({"name": unicodedata.normalize('NFKD', section[u'line']).encode('ascii','ignore'), "title": unicodedata.normalize('NFKD', section[u'anchor']).encode('ascii','ignore')})
                else:
                    moretopics[-1]["more"] = [{"name": unicodedata.normalize('NFKD', section[u'line']).encode('ascii','ignore'), "title": unicodedata.normalize('NFKD', section[u'anchor']).encode('ascii','ignore')}]

        return moretopics[0:4]


    def getres(self, title): 
        response = requests.get("https://learn-anything.xyz/api/maps/?q=" + title.replace(" ", "+"))
        if (response.status_code is not 200): 
            print("fail")
            quit()
            
        data = json.loads(response.content)
        dataa = [item for item in data if item.get('key') == title.lower()]
        if len(dataa) is not 0: 
            response = requests.get("https://learn-anything.xyz/api/maps/" + dataa[0]['id'])
            if (response.status_code is not 200): 
                print("fail")
                quit()
                
            data = json.loads(response.content)['nodes']
            dataaa = [{"title": item.get('nodes')[0]['text'], "url": item.get('nodes')[0]['url']} for item in data if len(item.get('nodes')) > 0]
            return dataaa
        else: 
            print("error in learn-anything")
            return "errr"
