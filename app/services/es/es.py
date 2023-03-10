from datetime import date
from typing import Callable, TypeVar, List

from elasticsearch import Elasticsearch

from app.config import get_settings
from app.models import HasId

settings = get_settings()

es = Elasticsearch(settings.es_host)


def index(doc: HasId):
    res = es.index(index=settings.es_index, id=doc.get_id(), document=doc.dict())
    return res


T = TypeVar("T")


def search(query: dict, model: Callable[[dict], T], size: int = 15, from_: int = 0) -> (int, List[T]):
    res = es.search(index=settings.es_index, query=query, size=size, from_=from_)
    hits = res.get("hits", {}).get("hits", [])
    total = res.get("hits").get("total").get("value")
    if not isinstance(total, int):
        total = 0
    return total, [model(**x.get("_source")) for x in hits]


def date_filter(field_name: str, start: date | None = None, end: date | None = None) -> dict | None:
    if not start and not end:
        return None
    start_filter = {"gte": start.isoformat()} if start else {}
    end_filter = {"lte": end.isoformat()} if end else {}
    return {"range": {field_name: {**start_filter, **end_filter}}}


def bool_filter(field_name: str, value: bool | None) -> dict | None:
    if value is None:
        return None
    return {"term": {field_name: value}}


def multi_match(value: str) -> dict | None:
    if value:
        return {
            "multi_match": {
                "query": value,
                "type": "bool_prefix",
                "fields": [
                    "caption^3",
                    "caption._2gram^3",
                    "caption._3gram^3",
                    "description",
                    "description._2gram",
                    "description._3gram",
                    "location",
                    "location._2gram",
                    "location._3gram",
                ],
            }
        }
    return None
