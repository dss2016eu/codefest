# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 15:47:12 2016

Transcribe Gaelic corpus using abair.ie

@author: Adam Varga
"""

from lxml import html
import requests

def read_file(filename):
    
    with open(filename, 'r') as source:
        text = source.read()
        
    return text.split('.')
        
def transcribe(sentence):
    
    request_url='http://www.abair.tcd.ie/?view=words&lang=eng&page=synthesis&synth=gd&xpos=0&ypos=0&speed=Gn%C3%A1thluas&pitch=1.0&input=' + sentence + '&xmlfile=20160704_135150.xml&colors=default'
    options = {'ipa': 'X-SAMPA'}
    
    r = requests.post(request_url, data=options)
    tree = html.fromstring(r.content)
    transcriptions = tree.xpath('//td[@class="transcription"]/text()')
    
    t = []    
    for transcription in transcriptions:
        t.append(' '.join(transcription.split()))
        
    return ' '.join(t)

def write_file(transcriptions, outfile):
    
    with open(outfile, 'w'):
        pass
    
    for transcription in transcriptions:
        with open(outfile, 'a+') as target:
            target.write(transcription + ' \n')

if __name__ == '__main__':
    
    source_text = read_file('in.txt')
    transcriptions = []
    for sentence in source_text:
        transcriptions.append(transcribe(sentence))
    write_file(transcriptions, 'out.txt')
    