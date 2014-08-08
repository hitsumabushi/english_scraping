import requests
from jinja2 import  Environment, FileSystemLoader
import lxml.html

# URL List
_BBC  = 'http://www.bbc.com/'
_CNET = 'http://www.cnet.com/'
WEB_LIST= [_BBC, _CNET]

# Output Template
env = Environment(loader = FileSystemLoader('.', encoding='utf-8'))
template = env.get_template('count.jinja2')

# Get Resources
ignore_content_BBC=["picture-galleries", "world-service-language-links", "av-carousel---top-stories"]
response = requests.get(_BBC + "/news")
root = lxml.html.fromstring(response.text)
[ div.drop_tree() for div in root.xpath('//div[' + ' or '.join([ '@id="' + content + '"' for content in ignore_content_BBC ]) + ']')]

links = root.xpath('//div[@id="now"]//a[@class="story"]')
[[ img.drop_tree() for img in link.xpath('//img') ] for link in links ]
[[ span.drop_tree() for span in link.xpath('//span') ] for link in links ]
[ link.make_links_absolute(_BBC) for link in links ]

with open("articles.html", "w") as file:
    file.write(template.render(links = [ lxml.html.tostring(link, encoding="utf-8").decode("utf-8").strip()
                                         for link in links ]))
