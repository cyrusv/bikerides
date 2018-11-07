import requests
from bs4 import BeautifulSoup as bs

class Ride(object):
	def __init__(self, name, description, distance, climb, fire, single, paved, road, technical, scenic):
		self.name = name
		self.description = description
		self.distance = float(distance)
		self.climb = int(climb)
		self.fire = getSurface(fire)
		self.single = getSurface(single)
		self.paved = getSurface(paved)
		self.road = getSurface(road)
		self.technical = int(technical)
		self.scenic = int(scenic)

	def __repr__(self):
		return """
		{}: {} miles {} ft, {} technical, {} single
		""".format(self.name, self.distance, self.climb, self.technical, self.single)


def getSurface(text):
	return int(text.split('%')[0] or 0)

def getText(el):
	return '' if el is None else el.text

r = requests.get("https://bayarearides.com/")
soup = bs(r.text, 'html.parser')

maintable = soup.find_all("table", id="snippetlist")
assert len(maintable) == 1
maintable = maintable[0]

rides = []
for row in maintable.find_all('table', class_='rowtable'):
	name = getText(row.find('span', class_='sortname'))
	description = 'todo'
	distance = getText(row.find('span', class_='length'))
	climb = getText(row.find('span', class_='climb'))
	fire = getText(row.find('span', class_='type_fireroad'))
	single = getText(row.find('span', class_='type_singletrack'))
	paved = getText(row.find('span', class_='type_paved'))
	road = getText(row.find('span', class_='type_road'))
	technical = getText(row.find('div', class_='rating-container-technical').find('div'))
	scenic = getText(row.find('div', class_='rating-container-scenic').find('div'))
	rides.append(Ride(name, description, distance, climb, fire, single, paved, road, technical, scenic))

print([r for r in rides if 
	r.technical < 6 and r.single < 10
])
