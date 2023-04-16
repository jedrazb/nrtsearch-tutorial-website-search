import React from "react";
import {
  ErrorBoundary,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  WithSearch,
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import MyAPIConnector from "@/connector/Connector";

const connector = new MyAPIConnector();

const config = {
  debug: true,
  alwaysSearchOnInitialLoad: true,
  apiConnector: connector,
  hasA11yNotifications: true,
  initialState: { resultsPerPage: 20 },
  searchQuery: {
    result_fields: {
      title: { raw: {} },
      url: { raw: {} },
      id: { raw: {} },
    },
    search_fields: {
      title: {},
    },
    disjunctiveFacets: [""],
    facets: {},
  },
};

const ResultView = ({ result, onClickLink }) => {
  return (
    <li className="sui-result ds-result">
      <div className="result-header">
        <a href={result.url.raw}>
          <h2 className="ds-title">{result.title.raw}</h2>
        </a>
        <p className="ds-url">{result.url.raw}</p>
        <div
          className="sui-result__body"
          dangerouslySetInnerHTML={{
            __html: `<p>${result.highlights.join("... ")}</p>`,
          }}
        ></div>
      </div>
    </li>
  );
};

export default function Home() {
  return (
    <SearchProvider config={config}>
      <WithSearch
        mapContextToProps={({ wasSearched }) => ({
          wasSearched,
        })}
      >
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={<SearchBox debounceLength={0} />}
                  sideContent={
                    <div>
                      <h2>Nrtsearch Tutorial 🚀 </h2>
                      <h4>Indexing Web Content for Search</h4>
                      <h4>Blog search</h4>
                    </div>
                  }
                  bodyContent={<Results resultView={ResultView} />}
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
