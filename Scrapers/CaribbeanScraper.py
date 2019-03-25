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
                #print "title and description didnt work"
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
        #print h2
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
        #print h2
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
                #print "title and description didnt work"
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
                #print "title and description didnt work"
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
        #print h2
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


#49  Countries
caribbean = [
        'Anguilla',
        'Antigua and Barbuda',
        'Aruba',
        'Bahamas',
        'Barbados',
        'Belize',
        'Bermuda',
	    'Bonaire',
        'British Virgin Islands',
        'Cayman Islands',
        'Cuba',
        'Curacao',
        'Dominica',
        'Dominican Republic',
        'Grenada',
        'Guadeloupe',
        'Guyana',
        'Haiti',
        'Jamaica',
        'Martinique',
        'Montserrat',
        'Puerto Rico',
        'Saba',
        'St Barthelemy',
        'Sint_Eustatius',
        'Saint_Kitts_and_Nevis',
        'Saint_Lucia',
        'St Maarten',
        'St Martin',
        'St Vincent and the Grenadines',
        'Suriname',
        'Trinidad and Tobago',
        'Turks and Caicos Islands',
        'United States Virgin Islands',
        'Venezuela'
]

BASE_URL = "https://en.wikivoyage.org"
ohio_url = "https://en.wikivoyage.org/wiki/Ohio"

driver = webdriver.Firefox() # if you want to use chrome, replace Firefox() with Chrome()
driver.implicitly_wait(2)

#print soup
#print cityHtml
write = True
missedCities = []


for q in range(len(caribbean)):
    print(states[q] + "\n\n")
    src = getSourceHtml(driver,BASE_URL + "/wiki/" + states[q])
    # html = urlopen(ohio_url)
    soup = BeautifulSoup(src,"lxml")
    cityHtml = soup.find_all('div', class_='mw-h2section')[1]
    stateCities = []
    li = cityHtml.find_all('li')
    for link in li:
        a = link.find('a')
        stateCities.append(a.get('href'))

    for i in range(0,len(stateCities)):
        cityName = stateCities[i][stateCities[i].rfind("/")+1:]
        testCity = BASE_URL + stateCities[i]
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
                    testCity = BASE_URL + str(district)
                    print testCity + "\n\n\n"
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
                #print "City isn't big enough to have districts"
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
        counter = 1;
        if write:
            with open(os.path.join('CaribbeanDataset/',fileName), 'a') as outfile:
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
