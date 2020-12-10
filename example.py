from get_conf_papers import GetConfPapers, Paper


class GetCvprPapers(GetConfPapers):
    def handle_paper_list(self, soup):
        url_prefix = "https://openaccess.thecvf.com/"
        paper_list = []

        for title_dt in soup.find_all("dt", "ptitle"):
            paper = Paper()

            paper.title = title_dt.get_text().strip()
            paper.detail_url = url_prefix + title_dt.a["href"]

            authors_dd = title_dt.find_next("dd")
            paper.authors = [a.get_text().strip() for a in authors_dd.find_all("a")]

            for a in authors_dd.find_next("dd").find_all("a"):
                a_text = a.get_text()
                if "pdf" in a_text:
                    paper.pdf = url_prefix + a["href"]
                elif "supp" in a_text:
                    paper.supps.append(url_prefix + a["href"])
                elif "arXiv" in a_text:
                    paper.arxiv = a["href"]

            paper_list.append(paper)

        return paper_list

    def handle_paper_detail(self, soup, paper):
        pass


if __name__ == "__main__":
    with GetCvprPapers(
        "cvpr2020",
        "adv",
        [
            "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-16",
            "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-17",
            "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-18",
        ],
        # save_htmls=True,
        # clear_cache=True,
    ) as get_cvpr_papers:
        get_cvpr_papers()
