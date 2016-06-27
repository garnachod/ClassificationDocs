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

### PostgreSQL Table (documents_classification) PRIMARY KEY (submitfileid, categoryid)
| Name        | Data Type  |
| ------------- | -----:|
| submitfileid    | integer NOT NULL|
| hbasedocumentid  | character varying(255) NOT NULL |
| categoryid | integer NOT NULL |
|categoryname | character varying(255)|

### JSON REST Response
`{'status': 'ok', 'prediction':[{"tag":"Doc class 1", "probability":0.5},{"tag":"Doc class 2", "probability":0.3},{"tag":"Doc class 3", "probability":0.2}]}`


### Working in the documentation