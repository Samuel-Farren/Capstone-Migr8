from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from mvc import models
import json
from watson_developer_cloud import RetrieveAndRankV1, NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    features
from mvc import helpers
from mvc import credential as cred
import re
import unicodedata

# Create your views here.
def hello(request):
    retrieve_and_rank = RetrieveAndRankV1(
    username=cred.RRUSER,
    password=cred.RRPASS)

    context = {
        'greeting':'Hello World!',
        'status': helpers.WatsonStatus()
    }
    return render(request, 'Migr8/index.html', context)

def search(request):
    query = request.GET.get("search")
    if query:
        if request.user.is_authenticated():
            newquery = models.Querys.objects.create(user=request.user, query=query)
            newquery.save()
        nlcresult = helpers.nlcQuery(query.replace("?",""))
        if nlcresult == "where":
            results = helpers.rrQuery(query.replace("?",""), cred.CLUSTERID, cred.COLLECTION)
            cities = []
            bodies = []
            if results:
                cities, bodies = helpers.extractData(results)
            blurbs = []
            newbodies = []
            nlu = NaturalLanguageUnderstandingV1(
                version='2017-02-27',
                username=cred.NLUUSER,
                password=cred.NLUPASS)
            response = nlu.analyze(
                text=query,
                features=[features.Entities(), features.Keywords()])
            for x in bodies:
                temp_body = helpers.replace_custom_tags(x)
                blurbs.append(re.sub(r'<.*?>', '', temp_body)[:255] + '...')
                newbodies.append(temp_body)
                for y in response["keywords"]:
                    blurbs[len(blurbs) - 1] = blurbs[len(blurbs) - 1].replace(y["text"],'<mark>'+y["text"]+'</mark>')
                    newbodies[len(blurbs) - 1] = newbodies[len(blurbs) - 1].replace(y["text"],'<mark>'+y["text"]+'</mark>') 
            context = {
                'display_mode': 1,
                'status': helpers.WatsonStatus(),
                'query': query,
                'data': zip(cities, zip(blurbs, newbodies))
            }
            return render(request, 'Migr8/search.html', context)
        else:
            results = helpers.rrQuery(query.replace("?",""), cred.CLUSTERID2, cred.COLLECTION2)
            cities = []
            bodies = []
            city = ""
            city_content = ""
            display_mode = -1
            if results:
                cities, bodies = helpers.extractData(results)
                city = cities[0]
                display_mode = 2
            newbodies = []
            for x in bodies:
                newbodies.append(x)
            if results:
                city_content = newbodies[0]
            context = {
                'display_mode': display_mode,
                'status': helpers.WatsonStatus(),
                'query': query,
                'city': city,
                'city_content': city_content
            }
            return render(request, 'Migr8/search.html', context)
    else:
        context = {
            'display_mode': 0,
            'status': helpers.WatsonStatus()
        }
        return render(request, 'Migr8/search.html', context)

def profile(request):
    context = {}
    if request.user.is_authenticated():
        querys = models.Querys.objects.filter(user=request.user)
        context = { 'querys' : querys}
        return render(request, 'registration/profile.html', context)
    else:
        return render(request, 'Migr8/errorpage.html', context)
