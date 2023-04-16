# Nrtsearch Tutorial: Indexing Web Content for Search

Source code for mini-project. Tutorial available at: https://j.blaszyk.me/tech-blog/nrtsearch-tutorial-website-search/

Let's use [nrtsearch](https://github.com/Yelp/nrtsearch) - an open-source search engine built by Yelp - to support text search for any website.

I'm using my blog as an example dataset, but you can apply this approach to index any text content on the internet.

You need to have `docker` and `python3` installed on your system.

## How to

### start nrtseach cluster

First start `nrtsearch`, `search-ui`, `grpcox` (ui gRPC client) and `search-server`. Run in a separate terminal window:

```
make start
```

It will generate nrtsearch client code, build docker images and start them using docker compose. Check `docker-compose.yaml` to make sure that all exposed ports are available on your host machine.

### run blog crawler

The crawler fetches data from websites. In this tutorial I’m using my blog as an example dataset. We use beautifulsoup library for extracting website content. Run it with:

```
make start_crawler
```

### start nrtsearch index

In order to ingest the data into nrtsearch, we must first create an index and register the fields. Start the index with:

```
make start_index
```

### ingest your data

We use a python script, which will batch docs and ingest them into the primary and commit the index. Run it with:

```
make run_indexer
```

### Demo

On `localhost:3000` you should have access to search UI. You can explore the indexed data.

<img width="1420" alt="Screenshot 2023-04-16 at 09 47 02" src="https://user-images.githubusercontent.com/14121688/232282503-e098a8c4-5408-4c23-af2e-7b4c6461edbd.png">

On `localhost:6969` there is a running instance of gRPC web client - you can interact with nrtsearch nodes.

<img width="1205" alt="Screenshot 2023-04-16 at 09 47 43" src="https://user-images.githubusercontent.com/14121688/232282516-3922fee0-b090-43f9-8ca8-a6dd44bd39a0.png">

Full tutorial [here](https://j.blaszyk.me/tech-blog/nrtsearch-tutorial-website-search/)
