import requests
import re

BLOG_SITEMAP_URL = "https://j.blaszyk.me/sitemap/sitemap-index.xml"


def discover_sub_sitemaps(sitemap):
    r = requests.get(sitemap)

    sitemap = r.text
    sitemap_links = re.findall("<loc>(.*?)</loc>", sitemap, re.IGNORECASE)

    return sitemap_links


def discover_sitemap_urls(sitemap):
    r = requests.get(sitemap)

    sitemap = r.text
    page_links = re.findall("<loc>(.*?)</loc>", sitemap, re.IGNORECASE)

    return page_links


def get_source_urls(root_sitemap=BLOG_SITEMAP_URL):
    sitemaps = discover_sub_sitemaps(root_sitemap)

    urls = []

    for sitemap in sitemaps:
        sitemap_urls = discover_sitemap_urls(sitemap)
        urls.extend(sitemap_urls)

    return urls
