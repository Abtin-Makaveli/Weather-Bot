import os
import discord
import requests
import json
from keep_alive import keep_alive

client = discord.Client()
default_city = "toronto"

# When given a city name in string format it returns the formatted weather forecast for the current day in string format, if the city does not exist, it returns None
def get_weather(city):
  link = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=779b4df598629a6dcf4990ff50042919&units=metric"
  response = requests.get(link)
  json_data = json.loads(response.text)
  print("\n \n" + link + "\n")
  print(json.dumps(json_data, sort_keys=True,
    indent=4, separators=(',', ': ')))
  the_weather = "**Weather: **" + json_data["weather"][0]["main"] + "\n**Description: **" + json_data["weather"][0]["description"].title() + "\n**Temperature: **" + str(json_data["main"]["temp"])
  return(the_weather);

def get_input(input):
  word_list = input.split()
  word_list.pop(0)
  result = word_list[0]
  word_list.pop(0)
  for element in word_list:
        result += "+" + element
  return result

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  global default_city
  if message.author == client.user:
    return
  
  if message.content.startswith("!weather") and len(message.content) == 8:
    global default_city
    # This bit of code does not work due to how the bot is hosted, so for now the default city will be toronto
    #if default_city != None:
    #  await message.channel.send(get_weather(default_city))
    #else:
    #  await message.channel.send("Specify what city's weather you want to see, the right way to use the bot is: **!weather [NAME OF CITY]** or you can set a default city with: **!weather default [NAME OF CITY]**")
    await message.channel.send(get_weather(default_city))
    return

  if message.content.startswith("!weather default"):
    default_city = message.content.split()[2]
    print(default_city)
    await message.channel.send("Your default city has been changed, if the **!weather** command does not return what you want, try spelling the city's name correctly")
    return

  if message.content.startswith("!weather") and len(message.content) > 8:
    temp = get_input(message.content)
    await message.channel.send(get_weather(temp))
    return

keep_alive()
client.run(os.environ['TOKEN'])