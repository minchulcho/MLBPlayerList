import os 
import json 
import requests

class MLBStorage: 
    def __init__(self, path):
        self.path = path 
        self.getPlayerList()
        self._list = []

    '''
        updateNewPlayer(id)
            - Using ID, make URL. reuqest the url to server. 
              Then create text file and write res to the file. 
            - return Boolean
    '''
    def updateNewSinglePlayer(self, id):
        if self.isInList(id): 
            return False
        res = self.connted(str(id))
        #id = str(id)
        # url = 'https://statsapi.mlb.com/api/v1/people/'+id+'?hydrate=currentTeam,team,stats(type=[yearByYear,yearByYearAdvanced,careerRegularSeason,careerAdvanced,availableStats](team(league)),leagueListId=mlb_hist)&site=en'
        # res = requests.get(url)   
        # res = res.text
        
        if( self.isNotValued(res)  ) : 
            return False
        else: 
            jsonData = json.loads(res)
            jsonData["playerName"] = jsonData["copyright"]
            del jsonData["copyright"]
            
            save = open(self.path+str(id)+".json",'w') 
            save.write(json.dumps(jsonData))
            save.close()             
            return True
    '''
        updateMultiplePlayers(id, counter)
            - Bring player information from id to counter. 

    '''
    def updateMultiplePlayers(self, id, counter): 
        result = []
        for i in range(id, id+counter):
            success  = self.updateNewSinglePlayer(i)
            result.append({"id":i, "result":success})
        print(result)

    '''
        getPlayer(id)
            - return dictionary (a player information)
        
    '''
    def getPlayer(self, id): 
        if not self.isInList(id):
            return None

        reader = open( self.path+str(id)+".txt", 'r' )
        res = reader.read()
        reader.close()
        
        jsonData = json.loads(res)
        if "people" in jsonData:
            people = jsonData["people"][0]
        else:
            people = None
        
        return people

#################### HELP FUNCTIONs #################### 
    '''
        search id in file list in the path folder. 
            - return Boolean( id in the folder or not)
    '''
    def isInList(self, id):
        return str(id)+'.txt' in os.listdir( self.path )

    '''
        getPlayerList()
            - return type : list(about player data list in folder) 
    '''
    def getPlayerList(self):
        files = os.listdir(self.path)        
        def xx(ElemOfFiles):
            num = -1
            try:
                num = int(ElemOfFiles.split('.')[0])
            except BaseException as e:
                pass
            return num
        def yy(ElemOfFiles):
            return ElemOfFiles >= 0
        files = list(map(xx, files))

        files = list(filter(yy, files))
        return files
    
    def dataCleaning(self):
         return None

    def isNotValued (self, source):
        search = '"messageNumber":10'
        end = len(search)
        iter = 0 
        
        while True:
            if source[iter:end] != search:
                iter+=1
                end+=1
            else:
                break  
            if end >= len(search): 
                break 
        if( source[iter:end] == search):
            return True
        else:
            return False  


    def deleteData(self, id):
        if not self.isInList(id):
            print( "not in the list ")
            return None

        path = os.path.join(self.path, str(id)+'.txt')
        os.remove(path)
    
#################### Applied Functions #################### 
    def personalInfo(self, id):
        if not self.isInList(id):
            print( "not in the list ")
            return None 
        info = self.getPlayerList()
        print ( type (info ) )

    def getTeamInfo(self, id): 
        if not self.isInList(id):
            return None

        reader = open( self.path+str(id)+".txt", 'r' )
        res = reader.read()
        reader.close()

        jsonData = json.loads(res)
        print (jsonData["people"][0]["currentTeam"]["name"])

    def getOldestPlayer(self):
        currentMax = 0
        oldest = None
        for id in self.getPlayerList():
            player = self.getPlayer(id)
            try:
                if currentMax < player['currentAge']:
                    currentMax = player['currentAge']
                    oldest = player
            except:
                pass
        return oldest
####################new add code ##########################

    def connted(self, id):
        #https://statsapi.mlb.com/api/v1/people/++++?hydrate=currentTeam,team,stats(type=[yearByYear,yearByYearAdvanced,careerRegularSeason,careerAdvanced,availableStats](team(league)),leagueListId=mlb_hist)&site=en
        url = 'https://statsapi.mlb.com/api/v1/people/'+id+'?hydrate=currentTeam,team,stats(type=[yearByYear,yearByYearAdvanced,careerRegularSeason,careerAdvanced,availableStats](team(league)),leagueListId=mlb_hist)&site=en'
        res = requests.get(url)   
        res = res.text
        
        #print (( json.loads(res))["people"][0]["fullName"])
        
        
        
        
        #print (( json.loads(res)).keys())
        #print (type(json.loads(res)))





        return res

    def getEditList(self, id): 
            res =self.connted(str(id))
            context ={ 
                "name" : "", 
                "id" : ""
            }
            if( self.isNotValued(res)  ) : 
                print( "invalid id " + str (id))
                return None
            else: 
                jsonData = json.loads(res)
                print ( jsonData.keys())
                context["name"] = (jsonData["people"][0]["fullName"])
                context["id"] = (jsonData["people"][0]["id"])
                self._list.append(context)

            return True

    def makePlayerList(self):
        # 110078 ~ 111078
        _id = 110000
        result = []
        for i in range(_id, _id+1000):
            self.getEditList(i)
        jsonType = json.dumps(self._list)
        #print( jsonType)
        save = open(self.path+"list"+".txt",'w') 
        save.write(jsonType)
        save.close()
        return None



'''
    Using local folder
'''
mlbstorage = MLBStorage('./MLB/data/')
mlbstorage.makePlayerList()
'''
    enter Player ID from MLB as a parameter 
        David Americo Ortiz     : 120074  
        Christopher Allen Sale  : 519242
'''
#mlbstorage.updateNewSinglePlayer(425783)
'''
    First parameter is start ID 
    Second parameter is how much do you want 
'''
#mlbstorage.updateMultiplePlayers(477999, 20) 

'''
    enter the player MLB ID who you want to find 
'''
# print(mlbstorage.getPlayer(477132))

'''
    enter the player MLB ID who you want to delete  
'''
#mlbstorage.deleteData(547963)
#print(mlbstorage.getOldestPlayer())
# print(json.dumps(mlbstorage.getPlayer(547944)))


# print (  mlbstorage.getPlayer(547944)['fullName'] )


#mlbstorage.getPlayerList()



