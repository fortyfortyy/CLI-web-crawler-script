from urllib.parse import urlparse, urljoin

import aiohttp
import asyncio

import typer
from bs4 import BeautifulSoup

from node_class import Node
from utils import is_valid

# INTERNAL_URLS and EXTERNAL_URLS avoid duplications in links to check again
INTERNAL_URLS = set()
EXTERNAL_URLS = set()
REFERENCES = {}


async def get_html_async(url: str):
    async with aiohttp.ClientSession(trust_env=True, connector=aiohttp.TCPConnector(ssl=False)) as client:
        try:
            try:
                async with client.get(url) as resp:
                    return await resp.text() if resp.status == 200 else ""
            except aiohttp.TooManyRedirects:
                typer.secho(f"Too many redirects in {url} | Skipping to the next url..", fg=typer.colors.YELLOW)
                return ""
            except aiohttp.InvalidURL:
                typer.secho(
                    f"Invalid url {url}", fg=typer.colors.YELLOW
                )
                return ""
            except aiohttp.ServerTimeoutError:
                typer.secho(
                    f"Server Timeout Error... Skipping to the next url..", fg=typer.colors.YELLOW
                )
                return ""
            except aiohttp.ClientConnectorError:
                typer.secho(f"Can't connect to {url} | Skipping to the next url..",
                            fg=typer.colors.YELLOW)
                return ""
            except UnicodeDecodeError:
                typer.secho(f"Can't decode html page from {url} | Skipping to the next url..",
                            fg=typer.colors.YELLOW)
                return ""
            except AssertionError:
                typer.secho(f"Port is not free.",
                            fg=typer.colors.YELLOW)
                return ""

        except aiohttp.ClientConnectorError:
            typer.secho(f"\nCan't' connect to {url} | Skipping to the next url..", fg=typer.colors.YELLOW)
            return ""


def extract_page_data(base_url: str, html_page):
    # init number of internal sublinks of the current page
    number_of_internal_links = 0

    # init number of external links that are outside of base_url
    number_of_external_links = 0

    # set avoids duplicated links
    links_to_check_again = set()

    # domain name of the URL without the protocol
    domain_name = urlparse(base_url).netloc

    soup = BeautifulSoup(html_page, "lxml")
    title = soup.find("title").get_text()

    # temporary set of references to pages
    references_to_pages = set()
    INTERNAL_URLS.add(base_url)

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue

        # omit redirect link from subpage to main page
        if href == "/":
            number_of_internal_links += 1
            continue

        # join the URL if it's relative (not absolute link)
        href = urljoin(base_url, href)

        # remove URL GET parameters, ULR fragments, etc.
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        while href.endswith("/"):
            if href[-2] != "/":
                break
            href = href[:-1]

        if not href.endswith("/"):
            href = href + "/"

        # breakpoint()
        if not is_valid(href):
            # not a valid URL
            continue

        if not href.startswith('https://') or not href.startswith(f"https://{domain_name}"):
            # external link
            if href not in EXTERNAL_URLS:
                EXTERNAL_URLS.add(href)

            number_of_external_links += 1
            continue
        else:
            number_of_internal_links += 1

        # avoid link that points to the page that was pointed by another url
        if href not in references_to_pages:
            references_to_pages.add(href)

        if href in INTERNAL_URLS:
            # already in the set (link was checked)
            continue

        links_to_check_again.add(href)
        INTERNAL_URLS.add(href)

    for href in references_to_pages:
        if not REFERENCES.get(href):
            REFERENCES[href] = 1
        else:
            REFERENCES[href] += 1

    return links_to_check_again, title, number_of_internal_links, number_of_external_links


async def async_get_data(base_url: str, node: Node) -> None:
    # get html source
    html_page = await get_html_async(base_url.lower())

    if html_page is None or html_page == "":
        return

    # get data from the page
    sub_links, title, num_of_internal_links, num_of_external_links = extract_page_data(base_url, html_page)

    node.title = title
    node.num_of_internal_links = num_of_internal_links
    node.num_of_external_links = num_of_external_links

    coros = []
    for idx, link in enumerate(sub_links):
        node.add_child(link)
        coros.append(async_get_data(base_url=link, node=node.children[idx]))

    await asyncio.gather(*coros)
