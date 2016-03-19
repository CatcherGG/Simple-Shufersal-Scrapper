#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2, StringIO, gzip
from bs4 import BeautifulSoup

def writePricesToFile(price_file_link, filename):
    global response
    outFilePath = "./Shufersal/" + filename + ".xml"
    response = urllib2.urlopen(price_file_link)
    compressedFile = StringIO.StringIO()
    compressedFile.write(response.read())
    compressedFile.seek(0)
    decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
    with open(outFilePath, 'w+') as outfile:
        outfile.write(decompressedFile.read())


def getMaxPage(page_soup):
    for a in page_soup.findAll('a', {"data-swhglnk": "true"}):
        if 'page' in a['href']:
            max_page = a['href'][a['href'].index('=') + 1:]
    return int(max_page)

def extract_prices_from_page(page_soup):
    for price_link in page_soup.findAll('tr', {"class": "webgrid-row-style"}):
        price_file_link = price_link.find('a', href=True, target='_blank')['href']
        store_index = price_link.findChildren('td')[0].text
        date = price_link.findChildren('td')[1].text
        filename = price_link.findChildren('td')[6].text
        store_full_name = price_link.findChildren('td')[5].text
        writePricesToFile(price_file_link, filename)

    for price_link in page_soup.findAll('tr', {"class": "webgrid-alternating-row"}):
        price_file_link = price_link.find('a', href=True, target='_blank')['href']
        store_index = price_link.findChildren('td')[0].text
        date = price_link.findChildren('td')[1].text
        filename = price_link.findChildren('td')[6].text
        store_full_name = price_link.findChildren('td')[5].text
        #try:
         #   store_address = u'שופרסל ' + store_full_name.split('-')[1].strip() + ' ' + store_full_name.split('-')[2].strip()
        #except IndexError:
            #store_address = u'שופרסל ' + store_full_name.split('-')[1].strip()
        writePricesToFile(price_file_link, filename)


def startFetchingShufersal():
    print('Starting to fetch Shufersal prices:')
    baseURL = "http://prices.shufersal.co.il/?page="
    response = urllib2.urlopen(baseURL + str(1))
    html = response.read()
    page_soup = BeautifulSoup(html, 'html.parser')
    for i in range(1, getMaxPage(page_soup) + 1):
        print('Fetching page number: ' + str(i))
        response = urllib2.urlopen(baseURL + str(i))
        html = response.read()
        page_soup = BeautifulSoup(html, 'html.parser')
        extract_prices_from_page(page_soup)


startFetchingShufersal()






