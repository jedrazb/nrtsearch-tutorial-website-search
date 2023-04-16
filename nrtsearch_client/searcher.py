import grpc

from client import INDEX_NAME

from yelp.nrtsearch.luceneserver_pb2_grpc import LuceneServerStub
from yelp.nrtsearch.search_pb2 import BooleanClause
from yelp.nrtsearch.search_pb2 import BooleanQuery
from yelp.nrtsearch.search_pb2 import Highlight
from yelp.nrtsearch.search_pb2 import MatchPhraseQuery
from yelp.nrtsearch.search_pb2 import MatchQuery
from yelp.nrtsearch.search_pb2 import PhraseQuery
from yelp.nrtsearch.search_pb2 import Query
from yelp.nrtsearch.search_pb2 import SearchRequest


class Searcher:
    def __init__(self):
        # For client-side round robin load balancing by gRPC client
        # we need to setup DNS to point single hostname to multiple replicas.
        # In docker-compose all replicas are available from at replica-node hostname
        # https://groups.google.com/g/grpc-io/c/ZtBCw4ZqLqE
        channel = grpc.insecure_channel(
            "replica-node:8000", [("grpc.lb_policy_name", "round_robin")])
        self._client = LuceneServerStub(channel)

    def get_highlights(self, hit):
        len_content = len(hit.highlights["content"].fragments)
        len_analyzed = len(hit.highlights["content.analyzed"].fragments)

        if len_content > len_analyzed:
            key = "content"
        else:
            key = "content.analyzed"

        return [str(fragment) for fragment in hit.highlights[key].fragments]

    def search(
        self,
        query_text,
        top_hits=50,
        start_hit=0,
    ):
        match_content_query = Query(
            matchQuery=MatchQuery(
                field="content",
                query=query_text,
                minimumNumberShouldMatch=1,
            )
        )
        match_phrase_content_query = Query(
            matchPhraseQuery=MatchPhraseQuery(
                field="content.analyzed",
                query=query_text,
                slop=3,
            ),
        )
        exact_phrase_content_query = Query(
            phraseQuery=PhraseQuery(
                field="content",
                terms=[query_text],
            ),
            boost=2
        )
        match_title_query = Query(
            matchQuery=MatchQuery(
                field="title",
                query=query_text,
                minimumNumberShouldMatch=1,
            ),
            boost=1.5,
        )
        match_phrase_title_query = Query(
            matchPhraseQuery=MatchPhraseQuery(
                field="title",
                query=query_text,
                slop=3,
            ),
            boost=0.75
        )
        match_description_query = Query(
            matchQuery=MatchQuery(
                field="description",
                query=query_text,
                minimumNumberShouldMatch=1,
            ),
            boost=0.75
        )
        match_headings_query = Query(
            matchQuery=MatchQuery(
                field="headings",
                query=query_text,
                minimumNumberShouldMatch=1,
            ),
            boost=0.75
        )
        match_url_query = Query(
            matchQuery=MatchQuery(
                field="title",
                query=query_text,
                minimumNumberShouldMatch=1,
            ),
            boost=1.5,
        )

        clauses = [
            BooleanClause(
                query=Query(
                    booleanQuery=BooleanQuery(
                        minimumNumberShouldMatch=2,
                        clauses=[
                            BooleanClause(query=match_content_query),
                            BooleanClause(query=match_headings_query),
                            BooleanClause(query=match_phrase_content_query),
                            BooleanClause(query=match_title_query),
                            BooleanClause(query=match_url_query),
                        ],
                    )
                ),
                occur=BooleanClause.Occur.MUST,
            ),
            BooleanClause(query=match_content_query),
            BooleanClause(query=exact_phrase_content_query),
            BooleanClause(query=match_phrase_title_query),
            BooleanClause(query=match_description_query),
        ]

        search_request = SearchRequest(
            indexName=INDEX_NAME,
            startHit=start_hit,
            topHits=start_hit + top_hits,
            retrieveFields=["url", "title", "description"],
            terminateAfter=250000,
            query=Query(
                booleanQuery=BooleanQuery(
                    minimumNumberShouldMatch=1, clauses=clauses)
            ),
            highlight=Highlight(
                fields=["content", "content.analyzed"],
                settings=Highlight.Settings(
                    pre_tags=["<em>"], post_tags=["</em>"]),
            ),
        )

        response = self._client.search(search_request)

        result = []

        for hit in response.hits:
            hit_result = {}
            for field in hit.fields.keys():
                values = hit.fields[field].fieldValue
                if values:
                    if len(values) > 1:
                        hit_result[field] = [
                            value.textValue for value in values]
                    else:
                        hit_result[field] = values[0].textValue
                else:
                    hit_result[field] = ""

            hit_result["highlights"] = self.get_highlights(hit)
            result.append(hit_result)

        return result, response.totalHits.value
