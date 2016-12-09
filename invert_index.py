# -*- coding: utf-8 -*-

from collections import OrderedDict

f = open('doc_index.txt')
matrix = f.readlines()

doc_term_position = {}
for row in matrix:
    element = row.split('\t')
    doc_term_position[(element[0],element[1])] = element[2:]
    
term_index={}
for key in doc_term_position:
    if term_index.has_key(key[1]) == False:
        term_index[key[1]]=[{key[0]:doc_term_position[(key[0],key[1])]}]    
    else:
        term_index[key[1]].append({key[0]:doc_term_position[(key[0],key[1])]})
    
# sorting terms
sorted_keys = sorted(map(int, list(term_index.keys())))
final_index = OrderedDict()
i=0
for key in sorted_keys:
    sub_arr = term_index[str(key)]
    whole_dict = {}
    
    for e in sub_arr:
        whole_dict[e.keys()[0]]=e[e.keys()[0]]
    
    elements=[]
    inner_arr=[]
    for item in sub_arr:
        elements.append(item.keys()[0])
    
    sub_keys = sorted(map(int, elements))
    z = 0
    for sub_key in sub_keys:
        sub_values = whole_dict[str(sub_key)]
        #sub_values = each[str(sub_key)]
        internal_dict = {}
        internal_dict[sub_key]=sorted(map(int,sub_values))
        
        if final_index.has_key(key) == False:
            final_index[key] = [internal_dict]
        else:
            final_index[key].append(internal_dict)
        z+=1
   
lines_length = []
length_index = 0
with open('term_index.txt', mode='w') as output_file:
    for key,value in final_index.iteritems():
        
        output_file.write(str(key)+'\t')
        lines_length.append(len(str(key)+'\t'))
        #lines_length[length_index] = len(str(key)+'\t')
        #flag=False
        current_doc_id = 0
     
        for doc_dict in value:
            last_doc_id = current_doc_id            
            current_doc_id = doc_dict.keys()[0]  
            
            last_position = 0
            first_time = True            
            for current_position in doc_dict[current_doc_id]:
                if first_time == False:
                    doc_id = 0
                    
                else:
                    doc_id = current_doc_id - last_doc_id
                    first_time = False
            
                line =str(doc_id)
                line +=':'
                line +=str(abs(current_position-last_position))
                line +=str('\t')
                
                output_file.write(line)
                lines_length[length_index] += len(line)
                last_position = current_position 
            
        output_file.write('\n')
        lines_length[length_index]+=len('\n')
        lines_length[length_index]+=1
        length_index+=1
output_file.close()

offset = 1
first_line = True
length_index=0
with open('term_info.txt',mode='w') as output_file:
    for key in final_index.keys():
        output_file.write(str(key)+'\t')        
        sub_list = final_index[key]
        if first_line == False:
            if length_index == 0:
                output_file.write(str(lines_length[length_index])+'\t')
            else:
                lines_length[length_index]+=lines_length[length_index-1]
                output_file.write(str(lines_length[length_index])+'\t')
            length_index+=1
        else:
            output_file.write('0'+'\t')
            first_line = False            
        corpus_count = 0        
        for doc_dict in sub_list:
            corpus_count+=len(doc_dict[doc_dict.keys()[0]])
        
        output_file.write(str(corpus_count)+'\t')
        document_occurences = len(sub_list)
        output_file.write(str(document_occurences)+'\n')
        
output_file.close()