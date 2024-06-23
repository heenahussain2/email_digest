""" 
The functions here are all independent from one another and therefore it isn't necessary to wrap them in a class,
instead we make it a python module which contains a bunch of independent functions to get various types of content
If we decide to add more sources to the content, we can easily build this library with other functions and add new sources
"""
import csv 
import random
import requests
import datetime

def get_random_quote(quotes_file = "quotes.csv"):
    """
    Retrieve a random quote from a CSV file. NOTE - will add API later
    """
    file_path = f"daily_digest/data_files/{quotes_file}" 
    try:
        with open(file_path) as csvfile:
            quotes = [{ "author": line[0],
                        "quote": line[1]} for line in csv.reader(csvfile, delimiter="|")]

    except Exception as e:
        print(f"Some Error occured, using default quote...{e}")
        quotes = [{
            "author" : "Confucius",
            "quote" : "He who wishes to secure the good of others, has already secured his own."
        }]
    return random.choice(quotes)

def get_weather_forecast(coords={"lat" : 21.31521972039856, "lon":76.23306375235012}):
    """
    Using the coordinates for Burhanpur. In this function using OpenWeatherAPI to get the weather forecast
    Can change ti later to dynamically put coordinates of all the recipients for the weather
    """
    forecasts = {}
    api_key = "e90baf25c09643d11bd0ebb5c40709d3"
    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={coords['lat']}&lon={coords['lon']}&APPID={api_key}&units=metric"
    weather_resp = requests.get(weather_url).json()
    if weather_resp and weather_resp["cod"] == "200":
        forecasts["city"] = weather_resp["city"]["name"] # city name
        forecasts["country"] = weather_resp["city"]["country"] # country name
        forecasts["periods"] = list()
        for each_period in weather_resp["list"][:9]: #populate list with next 9 forecasts
            forecasts["periods"].append({
                "timestamp" : datetime.datetime.fromtimestamp(each_period["dt"]),
                "temp" : each_period["main"]["temp"],
                "description" : each_period["weather"][0]["description"].title(),
                "icon" : f"http://openweathermap.org/img/wn/{each_period['weather'][0]['icon']}"
            })
    return forecasts

def get_wikipedia_article():
    """
    This function is for retrieving a random wikipedia article
    """
    try: # retrieve random wikipedia article
        wiki_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
        wiki_response = requests.get(wiki_url)
        if wiki_response.status_code == 200:
            wiki_json = wiki_response.json()
            return {
                "title" : wiki_json["title"],
                "extract" : wiki_json["extract"], 
                "url" : wiki_json["content_urls"]["desktop"]["page"]
            } 
    except Exception as e:
        print(e)


if __name__ == "__main__":
    ## Tests for random quotes generator function
    quote = get_random_quote()
    print(f"Random quote is - {quote['quote']} - {quote['author']}")
    ## Default quote
    quote = get_random_quote(quotes_file=None)
    print(f"Default quote is - {quote['quote']} - {quote['author']}")
    ### Test cases for get_weather_forecast()
    print("Testing weather forecast retrieval......")
    #Case 1 - default
    forecast = get_weather_forecast()
    if forecast:
        print(f"Forecast for default case\n city - {forecast['city']}, {forecast['country']}")
        for each_forecast in forecast["periods"]:
            print(f"{each_forecast['timestamp']} | {each_forecast['temp']} | {each_forecast['description']}")
    #Case2 - A different city
    bangalore = {"lat":12.957453529155968,"lon": 77.71602488168344} ## Coordinates for Bengaluru IN
    forecast = get_weather_forecast(coords=bangalore)
    if forecast:
        print(f"Forecast for city - {forecast['city']}, {forecast['country']}")
        for each_forecast in forecast["periods"]:
            print(f"{each_forecast['timestamp']} | {each_forecast['temp']} | {each_forecast['description']}")

    #Case 3 - Invalid coordinates
    invalid = {"lat": 12345.566, "lon": 12234.45}
    forecast = get_weather_forecast(coords=invalid)
    if not forecast:
        print("This is an invalid Case")
    ### Test cases for get_random_articles()
    print("Testing retrieval of random wikipedia articles .......")
    wiki_article = get_wikipedia_article()
    if wiki_article:
        print(f"Title - {wiki_article['title']}\nurl - {wiki_article['url']}\nSummary - {wiki_article['extract']}")