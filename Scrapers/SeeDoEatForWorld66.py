from bs4 import BeautifulSoup
from urllib2 import urlopen
import json
import time
import os.path
import sys
from time import sleep

# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def getSee(soup):
    seeStuff = getSeeSection(soup)
    lis = []
    seeMap = {}
    if seeStuff == "No See Section Found":
        return " "
    else:
        lis = seeStuff.find_all('li')
        for thing in lis:
            title = ""
            description = ""
            try:
                title = thing.find('span',class_='fn org listing-name').contents[0].encode('utf-8').strip()
                description = thing.find('span',class_ = 'note listing-content').contents[0].encode('utf-8').strip()
            except:
                print "title and description didnt work"
                pass
            seeMap[title] = description
        return seeMap

def getSeeSection(soup):
    cityHtml = soup.find_all('div', class_='mw-h2section')
    section = ""
    for section in cityHtml:
        h2 = section.select('h2')
        h2 = h2[0].get_text()
        #print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print h2
        #print h2
        if h2 == 'See[edit]' or h2=='See[edit][add listing]' or h2 == 'See[edit]' or h2=='See':
            return section
    return "No See Section Found"

def getDoSection(soup):
    cityHtml = soup.find_all('div', class_='mw-h2section')
    section = ""
    for section in cityHtml:
        h2 = section.select('h2')
        h2 = h2[0].get_text()
        #print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print h2
        if h2 == 'Do[edit]' or h2=='Do[edit][add listing]' or h2 == 'Do[edit]' or h2=='Do':
            return section
    return "No Do Section Found"


def getDo(soup):
    doStuff = getDoSection(soup)
    #print seeStuff
    lis = []
    doMap = {}
    if doStuff == "No See Section Found":
        return " "
    else:
        lis = doStuff.find_all('li')
        title = ""
        description = ""
        for thing in lis:
            try:
                title = thing.find('span',class_='fn org listing-name').contents[0].encode('utf-8').strip()
                description = thing.find('span',class_ = 'note listing-content').contents[0].encode('utf-8').strip()
            except:
                print "title and description didnt work"
                pass
            doMap[title] = description
        return doMap


def getEat(soup):
    eatStuff = getEatSection(soup)
    #print seeStuff
    lis = []
    eatMap = {}
    if eatStuff == "No See Section Found":
        return " "
    else:
        lis = eatStuff.find_all('li')
        title = ""
        description = ""
        for thing in lis:
            try:
                title = thing.find('span',class_='fn org listing-name').contents[0].encode('utf-8').strip()
                description = thing.find('span',class_ = 'note listing-content').contents[0].encode('utf-8').strip()
            except:
                print "title and description didnt work"
                pass
            eatMap[title] = description
        return eatMap

def getEatSection(soup):
    cityHtml = soup.find_all('div', class_='mw-h2section')
    section = ""
    for section in cityHtml:
        h2 = section.select('h2')
        h2 = h2[0].get_text()
        #print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print h2
        #print h2
        if h2 == 'Eat[edit]' or h2=='Eat[edit][add listing]' or h2 == 'Eat[edit]' or h2=='Eat':
            return section
    return "No Eat Section Found"

def getSourceHtml(driver, url):
    driver.get(url)
    sleep(3)
    src = driver.page_source # gets the html source of the page
    return src

def getNYC():
    cities = ["Manhattan","Brooklyn","Queens","Bronx","Staten"]



states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho",
"Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi",
"Missouri","Montana","Nebraska","Nevada","New_Hampshire","New_Jersey","New_Mexico","New_York_(state)","North_Carolina","North_Dakota",
"Ohio","Oklahoma","Oregon","Pennsylvania","Rhode_Island","South_Carolina","South_Dakota","Tennessee","Texas","Utah","Vermont",
"Virginia","Washington","West_Virginia","Wisconsin","Wyoming"]

#Add Austin back in

#BASE_URL = "https://en.wikivoyage.org/wiki/"
world66Cities = ["Baltimore", "Boston", "Charlotte", "Chicago", "Columbus", "Dallas", "Denver", "Detroit", "El_Paso", "Fort_Worth", "Houston", "Indianapolis",
"Jacksonville", "Las_Vegas", "Los_Angeles", "Louisville", "Memphis", "Milwaukee", "New_York_City", "Nashville", "Oklahoma_City", "Philadelphia", "Phoenix", "Portland_(Oregon)", "San_Jose_(California)",
"San_Antonio", "San_Diego", "San_Francisco", "Tucson", "Washington,_D.C.", 'Manhattan', 'Brooklyn', 'Queens', 'Bronx',
'Staten', 'Austin/Downtown', 'Austin/East', 'Austin/Northwest']

world66Cities = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx',
'Staten', 'Austin/Downtown', 'Austin/East', 'Austin/Northwest']


# world66Cities = ['Charlotte', 'Dallas', 'Oklahoma_City', 'San_Francisco', 'Tucson', 'Washington,_D.C.', 'Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten', 'Austin/Downtown', 'Austin/East', 'Austin/Northwest']

# world66Cities = ['Dallas/Downtown', 'Dallas/North_Dallas', 'Dallas/South_Dallas']

#Get Ney York,
# world66Cities = ["Portland_(Oregon)", "San_Jose_(California)",
# "San_Antonio", "San_Diego", "San_Francisco", "Tucson", "Washington,_D.C."]

#Deleted NYC
#nyc = ["Manhattan","Brooklyn","Queens","Bronx","Staten"]

BASE_URL = "https://en.wikivoyage.org/wiki/"
district_url = "https://en.wikivoyage.org"
# ohio_url = "https://en.wikivoyage.org/wiki/Ohio"

driver = webdriver.Firefox() # if you want to use chrome, replace Firefox() with Chrome()

write = True
missedCities = []
for i in range(0,len(world66Cities)):
    cityName = world66Cities[i]
    testCity = BASE_URL + world66Cities[i]
    src = getSourceHtml(driver,testCity)
    soup = BeautifulSoup(src,"lxml")
    districtHtml = soup.find('div', class_='mw-h2section')
    #print districtHtml
    h2=[]
    districtsWithInfo = []



    try:
        h2 = districtHtml.select('h2')
        districts = []

        if h2[0].get_text() == 'Districts[edit]':
            cityDistrictHtml = []
            regionTable = districtHtml.select('#region_list')
            tables = regionTable[0].find_all('table')
            for table in tables:
                a = table.find('a')
                districts.append(a.get('href'))
            #print districts
            for district in districts:
                districtMap = {}
                testCity = district_url + str(district)
                print testCity
                src = getSourceHtml(driver,testCity)
                soup = BeautifulSoup(src,"lxml")
                try:
                    districtMap['district'] = district
                    districtMap['see'] = getSee(soup)
                    districtMap['do'] = getDo(soup)
                    districtMap['eat'] = getEat(soup)
                    districtsWithInfo.append(districtMap)
                except:
                    pass
        else:
            #print h2[0].get_text()
            print "City isn't big enough to have districts"
            see = getSee(soup)
            do = getDo(soup)
            eat = getEat(soup)

    except Exception as e:
        h2.append("Failed")
        print "Finding h2 Failed"
        # print h2[0].get_text().strip()
        print e
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        write=False
        pass
    fileName = cityName + ".html"
    if cityName == "Manhattan" or cityName == "Brooklyn" or cityName=="Queens" or cityName == "Bronx" or cityName == "Staten":
        fileName = "New_York_City.html"
    if cityName == "Austin/Downtown" or cityName == "Austin/East" or cityName=="Austin/Northwest":
        fileName = "Austin.html"
    if cityName == "Dallas/Downtown" or cityName == "Dallas/North_Dallas" or cityName=="Dallas/South_Dallas":
        fileName = "Dallas.html"
    counter = 1
    if write:
        with open(os.path.join('World66SeeDoEat/',fileName), 'a') as outfile:

            if len(districtsWithInfo) > 0:
                #for each item in districitswithInfo print see
                outfile.write("%s" % "<h1>See:</h1>\n\n")
                outfile.write("%s" % "<ul>")
                for district in districtsWithInfo:
                    s = district['see']
                    for key in s:
                        outfile.write("%s" % "\n<li>")
                        outfile.write("%s" % "<h3>")
                        outfile.write("%s" % key)#.encode('utf-8').strip())
                        outfile.write("%s" % "</h3>")
                        outfile.write("%s" % "<p>")
                        outfile.write("%s" % s[key])#.encode('utf-8').strip())
                        outfile.write("%s" % "</p>")
                        outfile.write("%s" % "</li>")
                outfile.write("%s" % "</ul>")

                outfile.write("%s" % "<h1>Do:</h1>\n\n")
                outfile.write("%s" % "<ul>")
                for district in districtsWithInfo:
                    d = district['do']
                    for key in d:
                        outfile.write("%s" % "\n<li>")
                        outfile.write("%s" % "<h3>")
                        outfile.write("%s" % key)#.encode('utf-8').strip())
                        outfile.write("%s" % "</h3>")
                        outfile.write("%s" % "<p>")
                        outfile.write("%s" % d[key])#.encode('utf-8').strip())
                        outfile.write("%s" % "</p>")
                        outfile.write("%s" % "</li>")
                outfile.write("%s" % "</ul>")

                outfile.write("%s" % "<h1>Eat:</h1>\n\n")
                outfile.write("%s" % "<ul>")
                for district in districtsWithInfo:
                    e = district['eat']
                    for key in e:
                        outfile.write("%s" % "\n<li>")
                        outfile.write("%s" % "<h3>")
                        outfile.write("%s" % key)#.encode('utf-8').strip())
                        outfile.write("%s" % "</h3>")
                        outfile.write("%s" % "<p>")
                        outfile.write("%s" % e[key])#.encode('utf-8').strip())
                        outfile.write("%s" % "</p>")
                        outfile.write("%s" % "</li>")
                outfile.write("%s" % "</ul>")

            else:
                #for each item in districitswithInfo print see
                outfile.write("%s" % "<h1>See:</h1>\n")
                outfile.write("%s" % "<ul>")
                for key in see:
                    outfile.write("%s" % "\n<li>")
                    outfile.write("%s" % "<h3>")
                    outfile.write("%s" % key)#.encode('utf-8').strip())
                    outfile.write("%s" % "</h3>")
                    outfile.write("%s" % "<p>")
                    outfile.write("%s" % see[key])#.encode('utf-8').strip())
                    outfile.write("%s" % "</p>")
                    outfile.write("%s" % "</li>")
                    counter += 1
                counter = 1
                #for each item in districitswithInfo print do
                outfile.write("%s" % "</ul>")
                outfile.write("%s" % "<h1>Do:</h1>\n")
                outfile.write("%s" % "<ul>")
                for key in do:
                    outfile.write("%s" % "\n<li>")
                    outfile.write("%s" % "<h3>")
                    outfile.write("%s" % key)#.encode('utf-8').strip())
                    outfile.write("%s" % "</h3>")
                    outfile.write("%s" % "<p>")
                    outfile.write("%s" % do[key])#.encode('utf-8').strip())
                    outfile.write("%s" % "</p>")
                    outfile.write("%s" % "</li>")
                #for each item in districitswithInfo print eat
                outfile.write("%s" % "</ul>")
                outfile.write("%s" % "<h1>Eat:</h1>\n")
                outfile.write("%s" % "<ul>")
                for key in eat:
                    outfile.write("%s" % "\n<li>")
                    outfile.write("%s" % "<h3>")
                    outfile.write("%s" % key)#.encode('utf-8').strip())
                    outfile.write("%s" % "</h3>")
                    outfile.write("%s" % "<p>")
                    outfile.write("%s" % eat[key])#.encode('utf-8').strip())
                    outfile.write("%s" % "</p>")
                    outfile.write("%s" % "</li>")
                outfile.write("%s" % "</ul>")
    else:
        missedCities.append(cityName)
        write = True
print missedCities
