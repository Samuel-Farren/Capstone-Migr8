from bs4 import BeautifulSoup
from urllib2 import urlopen
import json
import time
import os.path


def getCityName(ref):
    return ref[ref.rfind("/",47)+1:]

def getBroadDescription(soup, ):
    broadDescription = soup.find('div', class_='pseudoparagraph')

def filterChars(string):
    string = string.replace("\\n","")
    string = string.replace("\\t","")

    string = string.encode("ascii","ignore")
    return string


dataset = {}
amenities = {}
add = {}
doc = {}
watsonSet = []
mostPopulousCities = ["washingtondc","newyorkstate/newyork","california/losangeles","illinois/chicago","texas/houston","pennsylvania/philadelphia","arizona/phoenix","texas/sanantonio","california/sandiego","texas/dallas","california/san_jose",
"michigan/detroit","indiana/indianapolis","florida/jacksonville","california/sanfranciscobayarea/sanfrancisco","ohio/columbus","texas/austin","tennessee/memphis","maryland/baltimore","texas/fort_worth","northcarolina/charlotte","texas/elpaso","wisconsin/milwaukee",
"massachusetts/boston","colorado/denver","kentucky/louisville","tennessee/nashville","nevada/lasvegas","oregon/portland","oklahoma/oklahomacity","arizona/tucson"]

BASE_URL = "http://www.world66.com/northamerica/unitedstates/lib/alldestinations"

html = urlopen(BASE_URL)
soup = BeautifulSoup(html,"lxml")
all_links = soup.find_all("a")
hrefs = []
for l in all_links:
    hrefs.append(l.get("href"))
first = "http://www.world66.com/northamerica/unitedstates/california/patterson"
last = "http://www.world66.com/northamerica/unitedstates/newmexico/zuni"

#1787 cities
print("\nThe number of cities in the US are: " + str(len(hrefs)) + "\n")
unitedStates = hrefs[hrefs.index(first)+1:hrefs.index(last)+1]


cityID = 1
for city in range(0,1):
    BASE_URL = "http://www.world66.com/northamerica/unitedstates/nevada/lasvegas"
    #testCity = unitedStates[city]
    #newyork city, miami, boston, philadelphia, washington dc, los angelas, hollywood
    #chicago, lasvegas, san francisco Bay area,
    #testCity = unitedStates[city]
    testCity = BASE_URL
    print testCity
    cityName = testCity[testCity.rfind("/",47)+1:]


    try:
        html = urlopen(testCity)
        soup = BeautifulSoup(html,"lxml")
        broadDescription = soup.find('div', class_='pseudoparagraph')
    except:
        pass

    print(cityName)
    try:
        broad = broadDescription.find_all(text=True)
    except:
        broad = "Error"
        pass

    bdescription = ""
    for thing in broad:
        bdescription = bdescription + thing
    #print description

    listLinks = soup.find('div', class_='box-bottom')
    l = listLinks.find_all("a")
    listHrefs = []
    for link in l:
        listHrefs.append(link.get("href"))

    BASE_URL = "http://www.world66.com"

    ###Filtering
    listHrefs = listHrefs[1:len(listHrefs)-1]
    #print(listHrefs)
    for link in listHrefs:
        if "child?" in link or "|" in link:
            listHrefs.remove(link)
    #print listHrefs
    ###########
    print listHrefs
    amenityMap = {}
    placesMap = {}
    for am in range(len(listHrefs)):

        testAmenity = BASE_URL + listHrefs[am]
        #div class=grey-box <p>
        amenityName = testAmenity[testAmenity.rfind("/",47)+1:]
        try:
            html = urlopen(testAmenity)
            soup = BeautifulSoup(html,"lxml")
            amenityDescription = soup.find('div', class_='pseudoparagraph')
        except:
            amenityDescription = "\n"
            pass
        amenityMap[amenityName] = amenityDescription

        # try:
        #     amenity = amenityDescription.find_all(text=True)
        # except:
        #     amenity = "No amenities in " + cityName
        #     pass

        # description = ""
        # for thing in amenity:
        #     description = description + thing
        #print description
        #print amenityName




        try:
            places = soup.find_all(class_='pointofinterest')
        except:
            places = "No places in " + cityName
        placesMap[amenityName] = places
        # for place in places:
        #     h3 = place.find("h3")
        #     names.append(h3.find(text = True))

        # specifics = {}
        # specifics["places"] = names
        # specifics["description"] = filterChars(description)
        # amenities["name"] = amenityName
        # amenities["details"] = specifics
    # cityInfo = {}
    # cityInfo["name"] = cityName
    # cityInfo["description"] = filterChars(bdescription)
    # cityInfo["amenities"] = amenities
    # dataset["id"] = cityID
    # dataset["name"] = cityName
    # dataset["details"] = cityInfo


    # doc["doc"] = dataset
    # add["add"] = doc
    # watsonSet.append(add)

    # print(add)
    # json_data = json.dumps(add)
    # parsed = json.loads(json_data)
    fileName = cityName + ".txt"




    with open(os.path.join('USMostPopulatedCities/',fileName), 'a') as outfile:
        outfile.write("%s" % broadDescription)
        print broadDescription
        for key in amenityMap:
            outfile.write("%s" % amenityMap[key])
            print amenityMap[key]

        for place in placesMap:
            outfile.write("%s" % placesMap[place])
            print placesMap[place]





        # json.dump(parsed, outfile)
    # specifics.clear()
    # amenities.clear();
    # cityInfo.clear()
    # dataset.clear()
    # doc.clear()
    # add.clear()

    #print json.dumps(parsed, indent=4, sort_keys=True)


    #watsonSet.append(add)
    #doc.clear()
    #add.clear()
    #cityInfo.clear()
    #dataset.clear()
    # cityID = cityID + 1
    time.sleep(1)

# json_data = json.dumps(watsonSet)
# parsed = json.loads(json_data)
# with open('watsonJsonFormat.txt', 'w') as outfile:
#     json.dump(parsed, outfile)
#print(watsonSet)
# parsed = json.loads(watsonSet)
# print json.dumps(parsed, indent=4, sort_keys=True)


#FILTER \n









#Get all <li> in a div with class "box-bottom"

#For City general informaiton: <div> class= pseudoparagraph <p>









# with open("lobbying.json", "w") as writeJSON:
#     json.dump(lobbying, writeJSON)


# {
#   "add" : {
#     "doc" : {
#       "id" : 1,
# .
# .
# .
# "commit" : { }
