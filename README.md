# Document Retrieval System
Program for retrieving documents on the basis of a query

Author: [Asad Raheem](https://github.com/tehmas)

Licensed under the GNU General Public License version 3.0

# Installation
<ul>
<li>Python 2.7</li>
<li>nltk 3.2.1</li>
<li>beautifulsoup 4.3.2</li>
<li>numpy 1.9.2</li>
</ul>

# Description
The system consists of three parts:
<ul>
<li>Tokenizer</li>
<li>Indexer</li>
<li>Index Reader</li>
</ul>

<h1>1. Tokenizer</h1>
Reads a document collection and creates documents containing indexable tokens. The tokenizer extracts text from HTML files and splits the text into tokens. Stop wording is also applied to ignore any stop words in the documents. All the tokens are converted to lower case (this is not always ideal and should be changed accordingly before using the code) and then Porter stemming is applied.

<h2>Outputs</h2>
<ul>
<li>docids.txt: Maps a document's file name to its document ID (DOCID).</li>
<li>termids.txt: Maps a token to its term ID (TERMID).</li>
<li>doc_index.txt: Forward index containing position of each term in each file.</li>
</ul>

<h2>Usage</h2>
In command prompt or terminal type: python tokenize_doc.py &lt;directory_name&gt;

<h1>2. Indexer</h1>
Reads a collection of tokenized documents and constructs an inverted index.

<h2>Outputs</h2>
<ul>
<li>term_index.txt: Inverted index containing file position for each occurence of each term in collection. Each line contains a completed inverted list for a single term i.e. a TERMID is followed by a list of DOCID:POSITION values. Delta encoding is applied to each list.</li>
<li>term_info.txt: Used for providing fast access time to the index reader. Each line contains a TERMID followed by offset in bytes (in term_index.txt), occurrences in entire corpus and number of documents in which term appears.</li>
</ul>

<h2>Usage</h2>
In command prompt or terminal type: python invert_index.py

<h1>3. Index Reader</h1>
Looks up offset in term_info.txt and jumps straight to the list in term_index.txt.

<h2>Usage</h2>
In command prompt or terminal type: 
<ul>
<li>python read_index.py --doc DOCNAME</li>
<li>python read_index.py --doc DOCNAME --term TERM</li>
<li>python --term TERM --doc DOCNAME</li>
</ul>
