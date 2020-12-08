from get_conf_papers import GetConfPapers


class GetCvprPapers(GetConfPapers):
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
        save_htmls=True,
        # clear_cache=True,
    ) as get_cvpr_papers:
        get_cvpr_papers()
