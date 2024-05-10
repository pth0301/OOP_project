# Ranking based on titles
import csv
import numpy as np
import nltk  
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# Text acquisition: identifies and stores documents
def read_csv(input_file):
    documents = []
    with open(input_file, 'r', encoding='utf-8',errors='ignore') as input_file:
        csv_reader = csv.reader(input_file)
        rows = list(csv_reader)
        for row in rows:
            documents.append(row[3]) # keywords based on the title
    return documents, rows    

# Text transformation: transforms documents into index terms or features
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    # Tokenize the text : process of splitting a text into individual words
    words = word_tokenize(text)
    # Remove stopwords and perform stemming - reduce words to their root
    filtered_words = [stemmer.stem(word.lower()) for word in words if word.lower() not in stop_words] # check word in stopwords or not
    return filtered_words

# Index creation: takes index terms created by text transformations and create data structures to support fast searching
def create_inverted_index(documents):
    inverted_index = {}
    for doc_id, document in enumerate(documents):
        # Preprocess the document text
        tokens = preprocess_text(document)
        # Update the inverted index
        for token in tokens: # add token after preprocessing into set index
            if token not in inverted_index:
                inverted_index[token] = set() # create a token with a set of id --> add doc_id
            inverted_index[token].add(doc_id)
    return inverted_index                     # return the inverted_index(data structure dict)

# TF-IDF ranking
def tfidf_ranking(query, documents):
    vectorizer = TfidfVectorizer()
    # Fit and transform the documents into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform(documents)
    # Transform the query into a TF-IDF vector
    query_vec = vectorizer.transform([query])
    # Calculate cosine similarity between query vector and document vectors
    cosine_sim = np.dot(tfidf_matrix, query_vec.T).toarray().flatten()
    # Get indices of documents sorted by relevance
    ranked_indices = np.argsort(cosine_sim)[::-1]
    return ranked_indices

# search engine with ranking
def search_engine(search_key, inverted_index, rows, documents):
    output_documents = []
    ranked_indices = tfidf_ranking(search_key, documents)
    for key in inverted_index.keys():
        for idx in ranked_indices:                                            
            if key in search_key:
                output_index = inverted_index[key] # output_index is a list of doc_id
                if idx in output_index:
                    output_documents.append(rows[idx])
    return output_documents

def return_new_csv(output_file, output_documents):
    with open(output_file, "w", newline='',encoding='utf-8',errors='ignore') as output_file: # write new information into new cvs file
            csv_writer = csv.writer(output_file)
            for row in output_documents:
                csv_writer.writerow(row)

def main():
    file_path = 'Search_engine/newBlockchaintablechangeUpdated.csv' # Relative Path
    documents, rows = read_csv(file_path)
    inverted_index = create_inverted_index(documents)
    # for term, postings in inverted_index.items():
    #     print(f'{term}: {postings}')
    output_documents = search_engine("Blockchain", inverted_index, rows, documents)
    return_new_csv('search_results.csv', output_documents)

if __name__ == "__main__":
    main()
