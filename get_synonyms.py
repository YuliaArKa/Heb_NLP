import requests
import sparql

session = requests.Session()
URL = 'https://www.wikidata.org/w/api.php'

def wbgetentities(name):
    res = session.post(URL, data={
        'action': 'wbsearchentities',
        'search': name,
        'language':'he',
        'format': 'json',
    })
    try:
        res_json = res.json()['search'][0]['id']
    except:
        res_json = None
    return res_json

def create_query(first_id):
    q = ('''
    PREFIX entity: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    SELECT ?syno
    WHERE {
      ?O ?P ?id .
      OPTIONAL{?id skos:altLabel ?syno
          filter (lang(?syno) = 'he')}
      VALUES ?id {entity:'''+ first_id +'''}   
      SERVICE wikibase:label {bd:serviceParam wikibase:language "he" .}}''')
    return q

term="עבירה"
Q_id = wbgetentities(term)
print(Q_id)

synonyms = []
query = create_query(Q_id)
result = sparql.query('https://query.wikidata.org/sparql', query)
for r in result:
     values = sparql.unpack_row(r)
     if values[0] not in synonyms:
           synonyms.append(values[0])
     
print(synonyms)