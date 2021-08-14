import re

import wikipedia
import requests
import bs4
from utils import wiki_fetch

className = "Ivory Gull"
summary, order_name, family_name, genus_name, species_name, page_url, image_url = wiki_fetch.get_wiki_data(className)
print(summary, order_name, family_name, genus_name, species_name, page_url, image_url)
page = wikipedia.page(className)
page_url = page.url
# summary = page.summary
# images = page.images
# image_url = images[0]
# print("Image URL: "+image_url)
#
# infobox = read_html(page_url, attrs={'class': 'infobox'})[0]
# print(infobox)
# orderName = infobox.iat[7, 1]
# print("Order: " + orderName)
#
# import hashlib
# def get_wc_thumb(image, width=300): # image = e.g. from Wikidata, width in pixels
#     image = image.replace(' ', '_') # need to replace spaces with underline
#     m = hashlib.md5()
#     m.update(image.encode('utf-8'))
#     d = m.hexdigest()
#     return "https://upload.wikimedia.org/wikipedia/commons/thumb/"+d[0]+'/'+d[0:2]+'/'+image+'/'+str(width)+'px-'+image

# Get response
response = requests.get(page_url)
# Parse the response
soup = bs4.BeautifulSoup(response.text, 'html.parser')
# Get infobox element
infobox_bs4 = soup.find('table', {'class': 'infobox'})

order_ele = infobox_bs4.find('td', text=re.compile('Order')).find_next_sibling()
family_ele = infobox_bs4.find('td', text=re.compile('Family')).find_next_sibling()
genus_ele = infobox_bs4.find('td', text=re.compile('Genus')).find_next_sibling()
species_ele = infobox_bs4.find('td', text=re.compile('Species')).find_next_sibling()

order_name = order_ele.find('a').text
family_name = family_ele.find('a').text
genus_name = genus_ele.find('i').text
species_name = species_ele.find('b').text

print(order_name, '\n', family_name, '\n', genus_name, '\n', species_name)




# Class name fetching test
#
# class_file = open('classes.txt', 'r')
# for line in class_file.readlines():
#     print(line)
#     number_n_name = line.split(' ')
#     print()
#     number = number_n_name[0]
#     if number == str(2):
#         original_class_name = number_n_name[1].split('.')[1]
#         class_name = ''
#         name_words = original_class_name.split('_')
#         for word in name_words:
#             if not word.istitle():
#                 word = '-' + word
#             else:
#                 word = ' ' + word
#             class_name = class_name + word
#         print(class_name)
#         break
