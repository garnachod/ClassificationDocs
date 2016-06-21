# ClassificationDocs
API REST, for document classification in categories

* This program uses ZooKeeper, for solr servers discovery
* This program uses Solr with HBASE for documents saving and indexing
* PostgreSQL persist the training elements
* Spotify/Luigi is used for the training workflow
* Doc2Vec (Paragraph to Vec) word and doc embedding Gensim
* scikit-learn NN does the final classification
* Django, API REST
* Models are cached with memcached

## WorkFlow LUIGI
Get Documents from DB -> generate one file per language "Stopwords filter and Lemmatization" -> Doc2Vec training -> Neural Network training.

## WorkFlow API
GET Query -> Doc Solr -> doc embedding -> Neural Network -> JSON Response

### Working in the documentation