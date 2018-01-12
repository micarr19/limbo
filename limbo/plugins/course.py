"""!course <query> will return a list of classes in an MIT course"""
import re
try:
    from urllib import quote, unquote
except ImportError:
    from urllib.request import quote, unquote
import requests

courses = set()

for i in range(25):
    if i != 13 and i != 19 and i != 23:
        courses.add(str(i))

courses = courses.union(set(('EC','ES','HST','IDS','MAS','STS','CMS','WGS','21A','21W','21M','21G','21H','21L')))
for course in courses:
    course = str(course)

def class_search(q):
    query = quote(q)

    if query == '21':
        return class_search('21A')+'\n'+class_search('21W')+'\n'+class_search('CMS')+'\n'+class_search('21G')+'\n'+class_search('21H')+'\n'+class_search('21L')+'\n'+class_search('21M')+'\n'+class_search('WGS')
    elif query not in courses:
        return "Not a valid MIT Course Number"

    url = "http://student.mit.edu/catalog/search.cgi?search={0}".format(query)
    info = requests.get(url).text
    info = info[info.index('<A HREF="m'):]
    info = info[:info.index('</DL>')]
    info = info.splitlines()

    for i in range(len(info)):
        info[i] = info[i][info[i].index('<A HREF="m'.format(query))+1:info[i].index('</A>')]
        info[i] = info[i][info[i].index('>')+1:]

    info = '\n'.join(info)
    return info

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!(?:course|search) (.*)", text)
    if not match:
        return
    return class_search(match[0])

on_bot_message = on_message
