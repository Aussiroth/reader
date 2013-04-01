import webapp2
import urllib2
from xml.dom import minidom
import re
import json
	
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('''
	  
	<!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <title>DHS Reader</title>
        <meta name="viewport" content="width=device-width">

		<link rel="icon" href = "/static/favicon.ico">
        <link rel="stylesheet" href="static/stylesheets/main.css">
    </head>
    <body>
        
		<header class = "center blue">
			<h1> DHS READER</h1>
		</header>
		
		<!-- Content goes here -->
		
		<div id = "content" class = "center blue">
		''')
		xml = urllib2.urlopen('http://www.dhs.sg/rss/what%2527s-new%3F-19.xml').read()
		
		xml_data = minidom.parseString(xml).getElementsByTagName('channel')

		# get all items
		allnews = xml_data[0].getElementsByTagName('item')
		
		jsons = {}
		
		# loop all items
		for detail in allnews:
			# get title
			title = detail.getElementsByTagName('title')[0].firstChild.nodeValue.strip()
			# get link
			link = detail.getElementsByTagName('link')[0].firstChild.nodeValue.strip()
			# get description
			description = detail.getElementsByTagName('description')[0].firstChild.wholeText.strip()
			description = re.sub("<[^>]*>", "", description)
			description = description[:-12]
			jsons[title] = [link, description]
		jsondata = [jsons]
		encoded = json.dumps(jsondata, sort_keys=True)
		news = json.loads(encoded)
		for item in news[0]:
			#write in div
			self.response.out.write('''
				<div class = "app red">
				<a href = "
			''')
			#link
			self.response.out.write(news[0][item][0])
			self.response.out.write(''' ">''')
			#title
			self.response.out.write(item)
			self.response.out.write('''</a><p>''')
			#description
			self.response.out.write(news[0][item][1])
			self.response.out.write('''</p>''')
			self.response.out.write('''</div>''')
		
		self.response.out.write('''
		</div>
		</body>
		</html>
	  
	  
	  '''
	)
	
	
app = webapp2.WSGIApplication([('/', MainPage)
							   ]
							   ,
                               debug=True)