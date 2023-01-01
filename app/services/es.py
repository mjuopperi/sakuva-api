from datetime import date
from typing import Callable, TypeVar, Type, List

from elasticsearch import Elasticsearch

from app.config import get_settings
from app.models import HasId

settings = get_settings()

es = Elasticsearch(settings.es_host)


def index(doc: HasId):
    res = es.index(index=settings.es_index, id=doc.get_id(), document=doc.dict())
    return res


T = TypeVar("T")


def search(query: dict, model: Callable[[dict], T]) -> List[T]:
    res = es.search(index=settings.es_index, query=query)
    hits = res.get("hits", {}).get("hits", [])
    return [model(**x.get("_source")) for x in hits]


def date_filter(field_name: str, start: date | None = None, end: date | None = None) -> dict | None:
    if not start and not end:
        return None
    start_filter = {"gte": start.isoformat()} if start else {}
    end_filter = {"lte": end.isoformat()} if end else {}
    return {"range": {field_name: {**start_filter, **end_filter}}}
