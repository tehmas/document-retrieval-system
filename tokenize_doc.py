# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, Comment
import re
import numpy as np
from nltk.stem import PorterStemmer
import sys
import os

def parse_html(url):
    data = remove_headers(url)
    soup = BeautifulSoup(data)
    #body = soup.find("body")
    
    # removing scripts, style and meta content
    [s.extract() for s in soup(['script','style'])]
    
    # removing comments
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    
    text = soup.get_text(' ')
    return text

def split_in_lower_case(text):
    exp = r'\w+(\.?\w+)*'
    matches = re.finditer(exp,text)
    tokens = []    
    for match in matches:
        if match:
            tokens.append(match.group().lower())
    return tokens
    
def stop_wording(tokens, file_name):
    #f = open(file_name)
    #stop_words = f.readlines()
    #f.close()
    stop_words = np.loadtxt(file_name,dtype=str)    
    remaining_words = [token for token in tokens if token not in stop_words]
    return remaining_words

def porter_stemming(tokens):
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(token) for token in tokens]
    return stemmed
    
def remove_headers(file_name):
    f = open(file_name)
    data = f.read().splitlines()
    
    found_header = True
    i = 0
    for line in data:
        if ('<html' in line.lower() or\
        '<!doctype html' in line.lower()) \
        and 'content-type:' not in line.lower():
            found_header = False
            file_data = ' '.join(data)
            return file_data
        if found_header == True:
            data[i] = ''
        i += 1
        
    file_data = ' '.join(data)
    return file_data

def main(directory_name):
    file_names = os.listdir(directory_name)
    doc_id = 1
    term_id = 1
    terms = []
    docs = []
    doc_term_positions = []
    term_map = {}    
    
    for file_name in file_names:
        print file_name + ' ' +  str(doc_id)
        text = parse_html(directory_name + '\\' + file_name)
        match = split_in_lower_case(text)
        words = stop_wording(match, 'stoplist.txt')
        stemmed = porter_stemming(words)

        position = 1
        for token in stemmed:
            if term_map.has_key(token) == False:
                term_map[token] = term_id
                terms.append((str(term_id) +'\t'+ token))
                term_id += 1
            doc_term_positions.append((doc_id,term_map[token], position))
            position += 1
        
        docs.append((str(doc_id) + '\t' + file_name))
        doc_id += 1

    postings = {} 
    for posting in doc_term_positions:
        if postings.has_key((posting[0], posting[1]))==False:
            postings[(posting[0], posting[1])]=[posting[2]]
        else:
            postings[(posting[0], posting[1])].append(posting[2])
            
    np.savetxt('docids.txt', docs, fmt='%s')
    np.savetxt('termids.txt', terms, fmt='%s')   
    with open('doc_index.txt', mode='w') as doc_index:
        for key in postings:
            doc_index.write(str(key[0]) + '\t' + str(key[1]))
            for value in postings[key]:
                doc_index.write('\t' + str(value))
            doc_index.write('\n')
    doc_index.close()
    return
    
if __name__=="__main__":
    if len(sys.argv) != 2:
        print "usage: python tokenize <directory_name>"
        
    else:
        print sys.argv[1]
        main(sys.argv[1])    
   