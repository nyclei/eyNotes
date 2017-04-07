import requests
import urllib2
import json
import sys
import re
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from BeautifulSoup import BeautifulSoup
from urlparse import urljoin


section = str(sys.argv[1])

# prepare base url : royalBaseUrl
if(section=='stage') :
    royalBaseUrl = "https://www.stage2.royalcaribbean.com"
elif(section=='prod') :
    royalBaseUrl = "https://www.royalcaribbean.com"
else :
    print "Error:  incorrect environment, must be one of [stage|prod]."
    print "Example:"
    print "    python ./flushRoyalHomePageImages.py stage"
    sys.exit(0);

# prepare secure http session : s
edgerc = EdgeRc('.edgerc')
akamaiBaseUrl = 'https://%s' % edgerc.get(section, 'host')
s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
akamaiInvalidateUrl = urljoin(akamaiBaseUrl, '/ccu/v3/invalidate/url')

# prepare the payload: payload
html_page = urllib2.urlopen(royalBaseUrl)
soup = BeautifulSoup(html_page)
images = []
for img in soup.findAll('img'):
    imageUrl = urljoin(royalBaseUrl, img.get('src'))
    images.append(imageUrl)

payloadJson = {'objects': []}
payloadJson['objects'] = images
payload=json.dumps(payloadJson)
print payload

# post the payload to Akamai
result = s.post( url=akamaiInvalidateUrl, data=payload, headers={'Content-Type': 'application/json'})
print result.status_code
print result.json()
