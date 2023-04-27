"This file will be used to test the bibtex function and output."
from final_pkg import Works
EX_BIBTEX = """@article{Kitchin2015,
        author =	 {John R. Kitchin},
        title =	 {Examples of Effective Data Sharing in Scientific Publishing},
        journal =	 {American Chemical Society},
        volume =	 5,
        number =	 6,
        pages =	 {3894 - 3899},
        year =	 2015,
        doi =		 {10.1021/acscatal.5b00538},
        url =		 {https://doi.org/10.1021/acscatal.5b00538},
        DATE_ADDED =	 {2023-04-26 17:35:05.965963},
        }
        """

def test_bibtex():
    "Function for the assert test."
    works_ex = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert EX_BIBTEX.split(
        'DATE_ADDED',maxsplit=1
                          )[0] == works_ex.bibtex.split(
        'DATE_ADDED',maxsplit=1
                                                       )[0]
