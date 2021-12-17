from __future__ import print_function, annotations
import re
import sys
import random
from pathlib import Path as pl
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython import paths as ip


DIR = pl(f"{ip.get_ipython_package_dir()}/extensions/randessay")

@magics_class
class Essay(Magics):

    url = 'http://www.paulgraham.com/articles.html'
    title_exp = '>(.+)</a.'
    href_exp = 'href="(.+)"'
    to_read = f'{DIR}/pg_essays.txt'
    cleanup = ['<u>(.+)</u>']
    have_read = f'{DIR}/pg_essays_read.txt'
    essay = None

    def __repr__(self):
        return f"Your essay for today is {self.essay[0]} at {self.essay[1]}. Drink some coffee and let the words percolate"

    @line_magic
    def essaycheck(self):
        from bs4 import BeautifulSoup as Soup
        from urllib.request import urlopen

        html = urlopen(self.url).read().decode("utf-8")
        soup = Soup(html, "html.parser")

        breakpoint()
        data = self._get_web_data(soup)
        processed_data = self._process_data(data)
        self._check_file(scraped_data)



    @line_magic
    def essay(self):
        to_read = self._read_file(to_read)
        if not to_read:
            self.essaycheck()
        have_read = self._read_file(have_read)
        options = list(set(to_read) - set(have_read))
        self.essay = random.choice(options).split("<>")



    def _read_file(self, file_path):
        file_data = []
        try:
            with open(file_path, "r") as file:
                file_data = [i for i in file.readline()]
        except FileNotFoundError:
            pass
        return file_data


    def _get_web_data(self, soup) -> list[tuple]:
        return [str(a) for a in soup.find_all("a")]

    def _process_data(self, data):
        breakpoint()
        anchor = re.compile(self.title_exp)
        href = re.compile(self.href_exp)
        proc_data = [f'{anchor.match(i).string} <> {href.match(i).string}' for i in data]
        for i, v in enumerate(proc_data):
            for expr in self.cleanup:
                temp_data = v.split("<>")
                temp_ex = re.compile(expr)
                for a, s in enumerate(temp_data):
                    ttdata = temp_ex.match(s).string
                    if ttdata: temp_data[a] = ttdata
                proc_data[i] = "<>".join(temp_data).replace("\\","")
        return proc_data



    def _check_file(self, scraped_data):
        file_date = self._read_file(self.path)
        if len(scraped_data) > len(file_data):
            with open(self.path, "w") as file:
                file.writelines([f"{str(i)}\n" for i in self.data_rep])


if __name__ == '__main__':
    runner = Essay()
    breakpoint()
    runner.essaycheck()
    breakpoint()
    runner.essay()
