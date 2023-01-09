curl -X POST "localhost:9200/_reindex?pretty" -H 'Content-Type: application/json' -d'
{
  "source": {
    "index": "images"
  },
  "dest": {
    "index": "images-0001"
  }
}
'
