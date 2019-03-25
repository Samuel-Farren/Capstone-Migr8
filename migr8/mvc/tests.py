from django.test import TestCase
from mvc import helpers
import os
import urllib.request
import urllib.parse

# Create your tests here.
class WatsonTestCase(TestCase):
  def test_status(self):
    if os.system("ping -c 1 8.8.8.8") == 0:
      self.assertEqual(str(helpers.WatsonStatus()), "('READY', 'The classifier instance is now available and is ready to take classifier requests.')")
    else:
      self.assertEqual(helpers.WatsonStatus(), "Watson Unable to be Reached.")

  def test_where_query_seafood(self):
    query = "Where should I go to eat seafood"
    required_cities = ["Boston", "San Francisco", "Las Vegas"]

    response = str(urllib.request.urlopen("http://localhost:8000/search?search=" + urllib.parse.quote(query)).read())
    for city in required_cities:
      self.assertTrue(city in response)

  def test_where_query_barbecue(self):
    query = "Where can I get some barbecue"
    required_cities = ["Memphis", "Austin"]

    response = str(urllib.request.urlopen("http://localhost:8000/search?search=" + urllib.parse.quote(query)).read())
    for city in required_cities:
      self.assertTrue(city in response)

  def test_where_query_gambling(self):
    query = "I would like to go gambling"
    required_cities = ["Las Vegas"]

    response = str(urllib.request.urlopen("http://localhost:8000/search?search=" + urllib.parse.quote(query)).read())
    for city in required_cities:
      self.assertTrue(city in response)

  def test_what_query_las_vegas(self):
    query = "What can I do in Las Vegas"
    required_cities = ["Las Vegas", "See:", "Eat:", "Do:"]

    response = str(urllib.request.urlopen("http://localhost:8000/search?search=" + urllib.parse.quote(query)).read())
    for city in required_cities:
      self.assertTrue(city in response)

  def test_what_query_baltimore(self):
    query = "What can I see in Baltimore"
    required_cities = ["Baltimore", "See:", "Eat:", "Do:"]

    response = str(urllib.request.urlopen("http://localhost:8000/search?search=" + urllib.parse.quote(query)).read())
    for city in required_cities:
      self.assertTrue(city in response)

  def test_what_query_washington(self):
    query = "What can I eat in Washington DC"
    required_cities = ["Washington, D.C.", "See:", "Eat:", "Do:"]

    response = str(urllib.request.urlopen("http://localhost:8000/search?search=" + urllib.parse.quote(query)).read())
    for city in required_cities:
      self.assertTrue(city in response)

  def test_empty_query(self):
    query = ""
    required_cities = ["Please enter a query."]

    response = str(urllib.request.urlopen("http://localhost:8000/search?search=" + urllib.parse.quote(query)).read())
    for city in required_cities:
      self.assertTrue(city in response)