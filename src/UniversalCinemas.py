import bs4 as bs
import urllib.request
import re
import json

src = urllib.request.urlopen('https://universalcinemas.com/').read()
soup = bs.BeautifulSoup(src, "lxml")

foo = soup.find_all('script')
foo = foo[8]
foo = str(foo)

foo = foo[foo.index("{"):]
foo = foo[:foo.index("movieDataByReleaseDate")]

commaIndex = foo[:foo.rfind("'2018-")].rfind(",")
bar = foo[:commaIndex]
while(commaIndex != -1):
	foo = foo[:commaIndex] + foo[commaIndex+1:]
	commaIndex = bar.rfind(",")
	foo = foo[:commaIndex] + foo[commaIndex+1:]
	commaIndex = bar[:bar.rfind("'2018-")].rfind(",")
	bar = foo[:commaIndex]


for i in range(0,3):
	foo = foo[:foo.rindex(",")] + foo[foo.rindex(",")+1:]

while(foo.find("/*will have to change nowPlaying to have separate dates everywhere */") != -1):
	foo = foo.replace("/*will have to change nowPlaying to have separate dates everywhere */", "")


jd = json.dumps(foo)
jl = json.loads(jd)
print (jl)


#print(re.split(r"movieData = ",foo.text))

# movies = soup.find("div", {"id": "moviePreviews"})

# movie_names = movies.find_all('h2')
# movie_ids = []

# id_list = movies.find_all('a')

# for i in range(0, len(id_list) - 2, 2):		# to get rid of extra links
# 	movie_ids.append(id_list[i].get('href'))




