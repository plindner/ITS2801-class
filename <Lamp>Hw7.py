#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 23:42:17 2021

@author: chrislamp
"""
#Importing bs4 beatufiul soup so I can do the webscrpting 
from bs4 import BeautifulSoup as bs
import requests
#the tyype of computer/device im going to use for this project so it uses my ip address
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
#So its in english 
LANGUAGE = "en-US,en;q=0.5"
#to define what webpage im using 
def get_weather_data(url):
    
    #getting acess to the session
    session = requests.Session()
   #so it accepts my device
    session.headers['User-Agent'] = USER_AGENT
    #so it uses english
    session.headers['Accept-Language'] = LANGUAGE
    #so its in english
    session.headers['Content-Language'] = LANGUAGE
    #url html link
    html = session.get(url)
    # create a new soup
    soup = bs(html.text, "html.parser")

 # store all results on this dictionary
    result = {}
    # extract Athens Ohio webpage for data
    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    # extract temperature now
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    # get the day and hour now
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    # get the actual weather
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    
 # get the precipitation
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    # get the % of humidity
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    # extract the wind
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
   
   

  # get next few days' weather
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        # extract the name of the day
        day_name = day.find("div", attrs={"class": "vk_lgy"}).attrs['aria-label']
        # get weather status for that day
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        # maximum temparature in fahrenheit
        max_temp = temp[0].text
        # minimum temparature fahrenheit
        min_temp = temp[2].text
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
    # append to result
    result['next_days'] = next_days
    return result
#to use the webiste provided in class to find the weather for Portland, Orgenon
if __name__ == "__main__":
    #url for the website
    URL = "https://forecast.weather.gov/MapClick.php?lat=44.9055&lon=-122.8107&lg=english&FcstType=text#.YFgSseYpBQI"
    #to write more freindly user comman line 
    import argparse
    #an easier way to webscript the page
    parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
   #to get the weather from porland oregon
    parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                        Default is your current location determined by your IP Address""", default="")
    # parse arguments
    args = parser.parse_args()
    #to collect the data
    region = args.region
    URL += region
    # get data
    data = get_weather_data(URL)
    
# print data for thr weather 
    print("Weather for:", data["region"])
    #for what time it is and date
    print("Now:", data["dayhour"])
    #for the tempetaure
    print(f"Temperature now: {data['temp_now']}°C")
    #for the description of the weather 
    print("Description:", data['weather_now'])
    #for the description
    print("Precipitation:", data["precipitation"])
   #for the precipation of the weather
    print("Humidity:", data["humidity"])
    #for the humidity of the weather 
    print("Wind:", data["wind"])
    #for the wind results
    print("Next days:")
    #for the days to come
    for dayweather in data["next_days"]:
        #For the weather day of the next days to be put in a list on the output file
        print("="*40, dayweather["name"], "="*40)
       #for the temperatrue data
        print("Description:", dayweather["weather"])
        #for the high tempeature
        print(f"Max temperature: {dayweather['max_temp']}°C")
       #for the low temperature
        print(f"Min temperature: {dayweather['min_temp']}°C")
    