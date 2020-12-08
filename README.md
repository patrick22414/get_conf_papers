# get_conf_papers

> WIP!!! DO NOT USE

`get_conf_papers` is a _very immature_ library that provides the boilerplate for scraping conference paper lists.

# Install

Python >= 3.7 is required, for `dataclasses` and `asyncio.run()`.

Packages `aiohttp` and `beautifulsoup4` are required for async web requests and html handling.

```sh
conda install aiohttp beautifulsoup4
```

Package `lxml` is recommanded for faster html parsing.

```sh
conda install lxml
```

# Usage

See `example.py` for an example.

First, subclass the `GetConfPapers` class

```python
from get_conf_papers import GetConfPapers

class GetCvprPapers(GetConfPapers):
```

And then implement the `handle_paper_list` method

Optionally, implement the `handle_paper_detail` method, if papers in the paper list links to a detail page

Optionally, implement the `filter_papers` method

Finally, call your class in the following way:

```python
with GetCvprPapers(
    name="cvpr2020",
    topic="object_detection",
    sources=[
        "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-16",
        "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-17",
        "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-18",
    ],
    # save_htmls=True,
    # clear_cache=True,
) as get_cvpr_papers:
    get_cvpr_papers()
```
