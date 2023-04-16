import json
import requests
from bs4 import BeautifulSoup

from source import get_source_urls


def run_crawler(urls):
    website_data = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.title.text.strip() if soup.title else None
        description = (
            soup.find("meta", attrs={"name": "description"})["content"].strip()
            if soup.find("meta", attrs={"name": "description"})
            else None
        )
        headings = [
            h.text.strip() for h in soup.find_all(["h1", "h2", "h3", "h4", "h5"])
        ]
        content = soup.get_text(" ", strip=True)

        website_data.append(
            {
                "url": url,
                "title": title,
                "description": description,
                "headings": headings,
                "content": content,
            }
        )

    return website_data


def save_data(website_data):
    with open("index_resources/website_data.json", "w") as outfile:
        json.dump(website_data, outfile)


def main():
    urls = get_source_urls()  # url's from website sitemap
    website_data = run_crawler(urls)
    print(f'Crawled {len(website_data)} urls.')
    save_data(website_data)


if __name__ == "__main__":
    main()
