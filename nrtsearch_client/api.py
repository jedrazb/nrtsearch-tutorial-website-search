from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from searcher import Searcher

app = Flask(__name__)
CORS(app)
searcher = Searcher()


@app.route("/search", methods=['POST'])
def search():
    data = request.get_json()
    search_term = data.get("searchTerm", "")
    current_page = data.get("current", 1)
    results_per_page = data.get("resultsPerPage", 20)
    start_hit = current_page * results_per_page - results_per_page

    results, total_results = searcher.search(
        query_text=search_term, start_hit=start_hit, top_hits=results_per_page
    )

    for i in range(len(results)):
        results[i]["id"] = {"raw": results[i]["url"]}
        results[i]["title"] = {"raw": results[i]["title"]}
        results[i]["url"] = {"raw": results[i]["url"]}

    response = dict()
    response["results"] = results
    response["resultSearchTerm"] = search_term

    # Calculate pagination data
    response["totalResults"] = total_results
    # Rounds total pages up if necessary
    response["totalPages"] = total_results // results_per_page + (
        total_results % results_per_page > 0
    )
    response["pagingStart"] = start_hit
    # Calculate the paging end based on total results
    response["pagingEnd"] = (
        start_hit + results_per_page
        if start_hit + results_per_page < total_results
        else total_results
    )

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=False)
