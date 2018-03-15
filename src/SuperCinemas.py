import bs4 as bs
import urllib.request as url
import re
import json

######	main #######

src = url.urlopen('http://supercinema.com.pk/')
soup = bs.BeautifulSoup(src, 'lxml')

print(soup.beautify())