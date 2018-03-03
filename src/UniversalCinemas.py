import bs4 as bs
import urllib.request
import re
import json

src = urllib.request.urlopen('https://universalcinemas.com/').read()
soup = bs.BeautifulSoup(src, "lxml")

foo = soup.find_all('script')
foo = foo[8]
foo = str(foo)

jd = json.dumps(foo[foo.index("{"):])
jl = json.loads(jd)
print (jl)


#print(re.split(r"movieData = ",foo.text))

# movies = soup.find("div", {"id": "moviePreviews"})

# movie_names = movies.find_all('h2')
# movie_ids = []

# id_list = movies.find_all('a')

# for i in range(0, len(id_list) - 2, 2):		# to get rid of extra links
# 	movie_ids.append(id_list[i].get('href'))




