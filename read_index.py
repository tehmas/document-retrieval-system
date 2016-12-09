# -*- coding: utf-8 -*-

from nltk.stem import PorterStemmer
import sys

termids = {}
docids = {}
term_info = {}
forward_index = {}
def load_term_ids():
    f = open('termids.txt')
    data = f.readlines()
    for row in data:
        element=row.split('\t')
        termids[element[1].strip('\n')]=element[0]
    f.close()
    return termids
    
def load_doc_ids():
    f=open('docids.txt')
    data = f.readlines()
    for row in data:
        element=row.split('\t')
        docids[element[1].strip('\n')]=element[0]
    f.close()
    return docids
    
def load_term_info():
    f = open('term_info.txt')
    data = f.readlines()
    for row in data:
        element=row.split('\t')
        element[-1]=element[-1].strip('\n')
        term_info[element[0]]=element[1:]
    f.close()
    return term_info
    
def get_inverted(posting, doc_id):
    i = 2
    sum_id = 0
    doc_id_base = ''
    first_id = False
    while posting[i] != ':':
        doc_id_base += posting[i]
        i += 1
    
    index_found = False
    nid = ''
     
    if int(doc_id_base) == int(doc_id):
        sum_id = int(doc_id_base)
        first_id = True
        index_found = True

    
    # find index
    doc_check = False
    while posting[i]!='\n' and index_found == False:
        if doc_check:
            doc_check = False
            nid = ''
            # getting complete relative id
            while posting[i] != ':':
                nid += posting[i]
                i += 1
            sum_id += int(nid)
            if sum_id == int(doc_id):
                index_found = True
                break
            
        elif posting[i] == '\t':
            doc_check = True
            
        i += 1
        
    positions = []
    rsum = 0
    if index_found:
        doc_check = False
        position_flag = True
        i += 1
        while posting[i] != '\n':
            if position_flag:
                position = ''
                while posting[i] != '\t':
                    position += posting[i]
                    i+= 1
                    
                positions.append(int(position))
                position_flag = False
                doc_check = True
                
            elif doc_check:
                rid = ''
                while posting[i] != ':':
                    rid += posting[i]
                    i += 1
                    
                rsum += int(rid)
                if first_id == False and rsum != sum_id:
                    break
                
                elif first_id == True and rid != '0':
                    break
                position_flag = True
                doc_check = False
            i += 1
            
    i=0
    current = 0
    last = 0
    while i < len(positions):
        current = positions[i]
        positions[i] = last + current
        last = positions[i]
        i += 1
    return positions
    
def load_doc_info():
    f = open('doc_index.txt')
    data = f.readlines()
    for row in data:
        element=row.split('\t')
        element[-1]=element[-1].strip('\n')
        element=map(int,element)
        if forward_index.has_key((element[0],element[1]))==False:
            forward_index[(element[0],element[1])]=element[2:]
        else:
            print "duplicate found"
            
    f.close()

def show_term_info(term_id):
    info=term_info[term_id]
    print "TERMID: " + term_id
    print "Number of documents containing term: "+ info[2]
    print "Term frequency in corpus: "+info[1]
    print "Inverted list offset: "+info[0]
    return
    
def show_doc_info(doc_id):
    print "DOCID: "+ doc_id      
    distinct_terms=0
    total_terms=0
    i=0 
    for docid, termid in forward_index.keys():
        if doc_id == str(docid):        
            distinct_terms+=1
            total_terms+=len(forward_index[(docid,termid)])
            i+=1
    print "Distinct terms: "+str(distinct_terms)
    print "Total terms: "+str(total_terms)
    return total_terms

def get_doc_info(doc_id):      
    distinct_terms=0
    total_terms=0
    i=0 
    for docid, termid in forward_index.keys():
        if doc_id == str(docid):        
            distinct_terms+=1
            total_terms+=len(forward_index[(docid,termid)])
            i+=1
    return total_terms



load_term_ids()
load_doc_ids()

if (len(sys.argv)==3):
    if(sys.argv[1]=='--term'):
        term = sys.argv[2]
        stemmer = PorterStemmer()
        stemmed = stemmer.stem(term)
        if termids.has_key(stemmed):            
            load_term_info()
            term_id = termids[stemmed]
            print'Listing for term: '+term
            show_term_info(term_id)
        else:
            print "List for "+term+" not present."
    elif(sys.argv[1]=='--doc'):
        doc_name = sys.argv[2]
        if docids.has_key(doc_name):
            load_doc_info()
            doc_id=docids[doc_name]
            print'Listing for doc: '+doc_name
            show_doc_info(doc_id)
        else:
            print "Document not present"
            
if len(sys.argv)==5:
    if(sys.argv[1]=='--term' and sys.argv[3]=='--doc'):
        term=sys.argv[2]
        stemmer=PorterStemmer()
        stemmed=stemmer.stem(term)
        if termids.has_key(stemmed):
            term_id=termids[stemmed]
            doc_name=sys.argv[4]
            if docids.has_key(doc_name):
                doc_id=docids[doc_name]
                load_term_info()
                offset=(int)(term_info[term_id][0])
                print term_info[term_id]
                f=open('term_index.txt')
                f.seek(offset)
                line=f.readline()
                f.close()
                positions=get_inverted(line, doc_id)
                print 'Inverted list for term: ' + term
                print 'In document: ' + doc_name
                print 'TERMID: ' + term_id
                print 'DOCID: ' + doc_id
                print 'Term frequency in document: ' + str(len(positions))
                print 'Positions: ' + str(positions)