import wikipedia
import wikipediaapi
import wikipedia
import requests
import bs4
import re


def get_wiki_data(class_name):
    print(class_name)
    try:
        page = wikipedia.page(class_name, auto_suggest=False)
        page_url = page.url
        summary = page.summary

        # Get response
        response = requests.get(page_url)
        # Parse the response
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        # Get infobox element
        infobox_bs4 = soup.find('table', {'class': 'infobox'})
        image = infobox_bs4.find('img')
        image_srcset = image['srcset'].split(',')
        image_url = image_srcset[len(image_srcset) - 1]
        image_url = image_url[1:len(image_url) - 3]
        image_url = 'https:' + image_url
        print(image_url)

        # Get order, family, genus, species names
        order_ele = infobox_bs4.find('td', text=re.compile('Order')).find_next_sibling()
        family_ele = infobox_bs4.find('td', text=re.compile('Family')).find_next_sibling()
        genus_ele = infobox_bs4.find('td', text=re.compile('Genus')).find_next_sibling()
        species_ele = infobox_bs4.find('td', text=re.compile('Species')).find_next_sibling()

        order_name = order_ele.find('a').text
        family_name = family_ele.find('a').text
        genus_name = genus_ele.find('i').text
        species_name = species_ele.find('b').text

        return summary, order_name, family_name, genus_name, species_name, page_url, image_url
    except:
        print(class_name + ': page not found')

