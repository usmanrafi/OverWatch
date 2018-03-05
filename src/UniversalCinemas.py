import bs4 as bs
import urllib.request
import re
import json

def printAllMovies():
	global data, days, movies_showing, movie_ids, movie_titles, movie_actors
	global movie_director, movie_duration, movie_times

	offset = 0
	for i in range(0,len(movies_showing)):
		print(days[i] + "> \n")
		for j in range(0, movies_showing[i]):
			print("\tTitle> \t\t" + movie_titles[offset])
			print("\tDirector> \t" + movie_director[offset])
			print("\tDuration> \t" + movie_duration[offset])
			print("\tActors> \t" + movie_actors[offset])
			print("\tTimes> \n") 
			print(movie_times[offset])

			print("\n\n")
			offset += 1


def cleanData(data):
	data = data[8]
	data = str(data)

	data = data[data.index("{"):]
	data = data[:data.index("movieDataByReleaseDate")]

	commaIndex = data[:data.rfind("'2018-")].rfind(",")
	bar = data[:commaIndex]
	while(commaIndex != -1):
		data = data[:commaIndex] + data[commaIndex+1:]
		commaIndex = bar.rfind(",")
		data = data[:commaIndex] + data[commaIndex+1:]
		commaIndex = bar[:bar.rfind("'2018-")].rfind(",")
		bar = data[:commaIndex]


	for i in range(0,3):
		data = data[:data.rindex(",")] + data[data.rindex(",")+1:]

	while(data.find("/*will have to change nowPlaying to have separate dates everywhere */") != -1):
		data = data.replace("/*will have to change nowPlaying to have separate dates everywhere */", "")

	while(data.find("'") != -1):
		data = data.replace("'", "\"")

	jd = json.dumps(data)
	jl = json.loads(jd)	

	return data

def parseMovies():

	global data, days, movies_showing, movie_ids, movie_titles, movie_actors
	global movie_director, movie_duration, movie_times

	index = data.find("2018")

	while(data.find("2018") != -1):

		days.append(data[index:index+10].strip())

		data = data[index+10:]

		movie_count = 0					# movies showing in a particular day

		offset = data.find("url")
		while(offset != -1 and offset < data.find("2018")):

			movie_ids.append(data[offset+7:data.find("\"", offset+7)].strip())

			offset = data.find("title")
			data = data[offset:]
			movie_titles.append(data[9: data.find("\"", 9)].strip())

			offset = data.find("duration")
			data = data[offset:]
			movie_duration.append(data[12: data.find("\"", 12)].strip())

			offset = data.find("director")
			data = data[offset:]
			movie_director.append(data[12: data.find("\"", 12)].strip())

			offset = data.find("actors")
			data = data[offset:]
			movie_actors.append(data[10: data.find("\"", 10)].strip())

			times = []
			offset = data.find("times")
			data = data[offset:]

			offset = data.find("time\":")
			while(offset != -1 and offset < data.find("url")):

				data = data[offset+8:]
				times.append(data[: data.find("\"")].strip())
				data = data[data.find("\""):]

				category = data.find("shortName")
				if(category != -1 and category < data.find("time") and category < data.find("url")):
					times.append(data[category+12:data.find("\"", category+12)].strip())
				offset = data.find("time")


			movie_times.append(times)
			movie_count += 1

			offset = data.find("url")


		movies_showing.append(movie_count)
		index = data.find("2018")


def getMoviesByCategory(cat):

	if(cat < 0 or cat > 3):
		print("Incorrect category entered!")

	if(cat == 3):
		printAllMovies()
	else:

		global data, days, movies_showing, movie_ids, movie_titles, movie_actors
		global movie_director, movie_duration, movie_times

		offset = 0
		for i in range(0,len(movies_showing)):
			print(days[i] + ">")
			for j in range(0, movies_showing[i]):

				catTimes = []		# to store different category times
				
				time = movie_times[offset]
				if(cat == 2):
					k = 0;
					while(k < (len(time)-1)):
						if(time[k+1] == "Ultra"):
							catTimes.append(time[k])
						k += 1

				elif(cat == 1):
					k = 0;
					while(k < (len(time)-1)):

						if(time[k+1] == "Gold"):
							catTimes.append(time[k])
						
						k += 1
				elif(cat == 0):
					k = 0;
					while(k < (len(time)-1)):

						if(time[k+1] != "Gold" and time[k+1] != "Ultra" and time[k] != "Gold" and time[k] != "Ultra"):
							catTimes.append(time[k])
						
						k += 1

					if(k == len(time)-1 and time[k] != "Gold" and time[k] != "Ultra"):
						print(time[k])

				if(len(catTimes) != 0):
					print("\tTitle> \t\t" + movie_titles[offset])
					print("\tDirector> \t" + movie_director[offset])
					print("\tDuration> \t" + movie_duration[offset])
					print("\tActors> \t" + movie_actors[offset])
					
					if(cat == 2):
						print("\tTimes (Ultra) > \n") 
					elif(cat == 1):
						print("\tTimes (Gold) > \n") 		
					elif(cat == 0):
						print("\tTimes (Normal) > \n") 

					print ("\t", end = "")
					print(catTimes)

					print("\n\n")
				
				offset += 1
		



#######   main   #######

src = urllib.request.urlopen('https://universalcinemas.com/').read()
soup = bs.BeautifulSoup(src, "lxml")
data = soup.find_all('script')

data = cleanData(data)

days = []				
movies_showing = [] 	# to store how many movies are being shown in day

movie_ids, movie_titles, movie_actors = ([] for i in range(3))	
movie_director, movie_duration, movie_times = ([] for i in range(3))

parseMovies()
#category = input("Enter category of movies [0-Normal] [1-Gold] [2-Ultra] [3-All]")
#getMoviesByCategory(category)
# print(days)
# print(movies_showing)
# print(movie_ids)
# print(movie_titles)
# print(movie_duration)
# print(movie_director)
# print(movie_actors)
# print(movie_times)