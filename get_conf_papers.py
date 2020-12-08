import asyncio
import csv
import dataclasses
import pickle
from typing import List, Dict
import os
import aiohttp
from bs4 import BeautifulSoup, FeatureNotFound

# try using the faster lxml parser
try:
    BeautifulSoup("<html />", "lxml")
    print("Using the faster 'lxml' parser")
    HTML_PARSER = "lxml"
except FeatureNotFound:
    print("Using the slower 'html.parser' parser. Install 'lxml' for faster parsing")
    HTML_PARSER = "html.parser"


@dataclasses.dataclass
class Paper:
    title: str

    authors: List[str] = dataclasses.field(default_factory=list)
    keywords: List[str] = dataclasses.field(default_factory=list)

    pdf: str = ""
    code: str = ""
    supps: List[str] = ""

    detail_url: str = ""

    abstract: str = ""
    tldr: str = ""

    arxiv: str = ""
    semsch: str = ""
    bibtex: str = ""

    _id: int = None


class GetConfPapers:
    def __init__(
        self,
        name: str,
        topic: str,
        sources: List[str],
        save_htmls=False,
        webpage_cache="webpage_cache.pkl",
        clear_cache=False,
    ):
        super().__init__()
        self.name = name
        self.topic = topic
        self.sources = sources

        if not os.path.isdir("tsv"):
            os.mkdir("tsv")
        self.tsv_filename = f"tsv/{self.name}-{self.topic}.tsv"

        self.save_htmls = save_htmls
        if self.save_htmls:
            if not os.path.isdir("html"):
                os.mkdir("html")

        self.webpage_cache = webpage_cache
        self.clear_cache = clear_cache

        self._cache = None

    def __enter__(self):
        if not self.clear_cache and os.path.isfile(self.webpage_cache):
            with open(self.webpage_cache, "rb") as f:
                self._cache = pickle.load(f)
        else:
            self._cache = {}

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        with open(self.webpage_cache, "wb") as f:
            pickle.dump(self._cache, f)

    def __call__(self):
        urls = []
        local_files = []
        for src in self.sources:
            if src.startswith(("http://", "https://")):
                urls.append(src)
            else:
                local_files.append(src)

        # Fetch URLs not in cache
        urls_to_fetch = [u for u in urls if u not in self._cache]

        print(f"Fetching {len(urls)} pages, {len(urls_to_fetch)} not in cache")
        webpages = asyncio.run(_fetch_all(urls_to_fetch))
        count_fetched = 0
        for url, webpage in zip(urls_to_fetch, webpages):
            if isinstance(webpage, str):
                count_fetched += 1
                self._cache[url] = webpage
            else:
                print("Failed", url)
        print(
            f"Fetched {len(urls_to_fetch)} pages, {count_fetched}/{len(urls_to_fetch)} OK"
        )

        # Make soups from fetched webpages and local files
        soups: Dict[str, BeautifulSoup] = {}
        for url in urls:
            if url in self._cache:
                soups[url] = BeautifulSoup(self._cache[url], HTML_PARSER)
        for file in local_files:
            with open(file, "r") as fin:
                soups[file] = BeautifulSoup(fin, HTML_PARSER)

        print(f"Created {len(soups)} soups")

        if self.save_htmls:
            for name, soup in soups.items():
                with open(
                    os.path.join("html", os.path.basename(name)) + ".html", "w"
                ) as fo:
                    fo.write(soup.prettify())

        # pass to handle paper list
        pass

    def handle_paper_list(soup: BeautifulSoup) -> List[Paper]:
        raise NotImplementedError

    def handle_paper_unit(html: str):
        raise NotImplementedError

    @classmethod
    def filter_papers(cls, all_papers):
        raise NotImplementedError


async def _fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            print("OK", url)
            text = await response.text()
            return text
        else:
            print("Failed", url, response.reason)


async def _fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(_fetch(session, url))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results


if __name__ == "__main__":
    with GetConfPapers(
        "cvpr2020",
        "adv",
        [
            "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-16",
            "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-17",
            "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-18",
        ],
        save_htmls=True,
        # clear_cache=True,
    ) as get_cvpr_papers:
        get_cvpr_papers()
