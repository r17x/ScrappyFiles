from bs4 import BeautifulSoup as BS

import requests
import os
import re

print " @Author : ri7nz <ri7nz.labs@gmail.com> "
"""

sample to scrap : http://dl.1tehmovies.com/94/


1. GET URI Target
2. Get Dir & Files List Save on dictionary python data type
3. Search filename by data type
4. get Result
5. tada download

"""

def getContent(uri):

    # get uri by head method
    uri_status = requests.head(uri)

    # check uri status
    if uri_status.status_code == 200:

        print "Get content from {uri}\n".format(uri=uri)
        content = requests.get(uri)

        # return if html content-type
        return content

def is_html(content):

    if content.headers['Content-Type'] == 'text/html':
        return content.content

    print "No Html Content"

    return None


def getTable(content):

    print("Parsing & Check HTML Content...")

    content = BS(content, 'html.parser')

    # because sample target is a tag
    table   = content.find_all('a')

    return table

def tableText(table, key):

    text_unicode = map(getText, table)
    text_str     = map(to_utf8, table)
    text_uri     = map(getUri, table)
    return {
            'unicode' : text_unicode,
            'text'    : text_str,
            'uri'     : text_uri
    }[key]

def to_utf8(text):

    #return string
    return ''.join(text).encode('utf-8').strip()

def to_uri(text):

    global uri

    return uri + text

def files_or_folder(uri):

    name, extension = os.path.splitext(uri)

    return { 'name' : name,
             'extension': extension if extension != '' else 'is directory',
             'uri'  : to_uri(uri) }

def getText(bs_tag):

    return bs_tag.get_text()

def getUri(bs_tag):

    return bs_tag.get('href')

uri = raw_input('URI Target: ')

content = is_html( getContent(uri) )

if content is None:

    exit("Exiting...")

table     = getTable(content)
list_uri = tableText(table, 'uri')
list_text = tableText(table, 'text')
list_uri_text = map(to_utf8, list_uri)
q = raw_input('Keyword :')

pattern = r"\b{txt}\b".format(txt = q)

regex = re.compile(pattern)

list_uri_text = filter(regex.search, list_uri_text)

result = map(files_or_folder, list_uri_text)

for r in result:

    print "Result of <{q}>...\n===> NAME : {fname}\n===> URI : {uri}\n===> Extension : {ext}\n===========THANKS==============".format(
            q=q,
            fname=r['name'],
            uri=r['uri'],
            ext=r['extension']
    )
