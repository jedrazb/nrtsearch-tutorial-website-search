import type { APIConnector } from "@elastic/search-ui";

class MyAPIConnector implements APIConnector {
  async onSearch(
    state: RequestState,
    queryConfig: QueryConfig
  ): Promise<ResponseState> {
    const { searchTerm, current, filters, sort, resultsPerPage } = state;
    // perform a request to your API with the request state
    const response = await fetch("http://localhost:5000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        searchTerm,
        current,
        filters,
        sort,
        resultsPerPage,
      }),
    });
    // response will need to be in the shape of ResponseState.
    // Alternatively you could transform the response here
    return response.json();
  }

  onAutocomplete: () => {
    // Not implemented
  };

  onResultClick: () => {
    // Not implemented
  };

  onAutocompleteResultClick(params): void {
    // Not implemented
  }
}

export default MyAPIConnector;
