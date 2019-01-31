#DEPENDENCIES
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

#DEPENDENCIES - MONGODB
from pymongo import MongoClient


#INITIALIZE ARRAYS
MarsNewsTitles = []
MarsNewsContent = []
results = {}

def scrape(): 
    #GET THE RESPONSE, PARSE THE RESPONSE 
    nasaNews_url = "https://mars.nasa.gov/news/?page=0&per_page=20&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    news_response = requests.get(nasaNews_url)
    news_parsed = bs(news_response.text, "html.parser")
    
    #PRINT TO CHECK AND INSPECT THE NEWS_PARSED FILE
    #pprint (news_parsed)
    
    #FIND AND APPEND TITLE
    for div_title in news_parsed.find_all("div", class_="content_title"):
        #print(div_title.find("a").text.strip())
        MarsNewsTitles.append(div_title.find("a").text.strip())

    #FIND AND APPEND DESCRIPTION
    for div_content in news_parsed.find_all("div", class_="rollover_description_inner"):
        #print(div_content.text.strip())
        MarsNewsContent.append(div_content.text.strip())

    
    
    #PRINT TO CHECK LISTS
    for item in MarsNewsTitles:
        print(item)
    print("\n")    
    for item in MarsNewsContent:
        print(item)
    print("\n")
    
    #APPEND NEWS TITLE AND CONTENT TO RESULTS DICTIONARY
    try:
        results.update({"marsNewsTitles" : MarsNewsTitles})
        print("news titles appended to dictionary")    
    except:
        print("failed to append titles to dictionary")    
    try:
        results.update({"marsNewsContent" : MarsNewsContent})
        print("news content appended to dictionary")  
    except:
        print("failed to append content to dictionary") 
    print("\n")
    
    
        
    #GET THE RESPONSE, PARSE THE RESPONSE 
    jplImage_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)"
    image_response = requests.get(jplImage_url)
    image_parsed = bs(image_response.text, "html.parser")
    
    #PRINT TO CHECK AND INSPECT THE IMAGE_PARSED FILE
    #pprint (image_parsed)
    
    #FIND LIST OF IMAGES AS UNORDERED LIST CLASS ARTICLES
    images = image_parsed.find("ul", class_="articles")
    #print(images)
    
    #FIND FIRST IMAGE <A> TAG
    firstImage = images.find("a")
    #print(firstImage)
    
    #FIND URL END IN <A> TAG
    firstImageLink = firstImage.attrs['data-fancybox-href']
    #print(imageLinkEnd)
    
    #COMBINE URL START TO END FOUND IN <A> TAG
    firstImageLink = "https://www.jpl.nasa.gov" + firstImageLink
    print(firstImageLink)
    try:
        results.update({"firstImageLink" : firstImageLink})
        print("large image link appended to dictionary")  
    except:
        print("failed to append large image link to dictionary") 
    print("\n")
    
    
    
    #GET THE RESPONSE, PARSE THE RESPONSE 
    twitterWeather_url = "https://twitter.com/marswxreport?lang=en"
    weather_response = requests.get(twitterWeather_url)
    weather_parsed = bs(weather_response.text, "html.parser")
    
    #PRINT TO CHECK AND INSPECT THE WEATHER_PARSED FILE
    #pprint (weather_parsed)
    
    #FIND WEATHER TWEET STREAM
    weatherStream = weather_parsed.find("div", class_="stream")
    #print (weatherStream)
    
    #FIND LATEST TWEET IN STREAM USING FIND
    currentTweet = weatherStream.find("li")
    #print (currentTweet)
    
    #FIND WEATHER BY ISOLATING FIRST CONTENT OF LATEST TWEET. USING FIND WOULD GIVE ME CONTENTS OF THE <A> TAG WITHIN TOO
    mars_weather = currentTweet.p.contents[0].strip()
    print(mars_weather)
    try:
        results.update({"mars_weather" : mars_weather})
        print("mars_weather appended to dictionary")  
    except:
        print("failed to append mars_weather to dictionary") 
    print("\n")    
    
    
    
    #GET THE RESPONSE, PARSE THE RESPONSE 
    facts_url = "https://space-facts.com/mars/"
    
    #GET TABLES FROM URL INTO VARIABLE TABLES
    tables = pd.read_html(facts_url)
    #print(tables)
    
    #MAKE TABLE INTO DATAFRAME
    factsDf = tables[0]
    #factsDf
    print("Facts DataFrame Created\n")
    try:
        results.update({"factsDf" : factsDf})
        print("facts table df appended to dictionary")  
    except:
        print("failed to append facts table df to dictionary") 
    print("\n")      
    
    
    
    #WRITE TO HTML
    factsDf.to_html('MarsFactsTable.html')
    print("HTML Created\n")
    return
    #END OF FUNCTION



#CALL FUNCTION
scrape()



#PRINT RESULTS DICTIONARY
pprint(results)



#MONGODB
#establish connection and check if database exists
conn = "mongodb://localhost:27017"
client = MongoClient(conn)
db = client.scrapedInfo
print(client.list_database_names())
if 'scrapedInfo' in client.list_database_names(): 
    client.drop_database('scrapedInfo')   
collection = db.scrapedMarsInfo
print("mongoDB connetion, database, schema, and table established")
#upload dictionary to database
try:
    collection.insert_many(results)
    print("results dumped to mongoDB")
except:
    print("dump to mongoDB FAILED")


                
        
print("SCRIPT COMPLETE")