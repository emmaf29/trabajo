from utilities.tabulate import tabulate
from utilities.log import LOGGER, setupLogger

class Printer:
    NONE = 0
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    """
    One of simple, plain, grid, fancy_grid, pipe, orgtbl, jira,
    presto, psql, rst, mediawiki, moinmoin, youtrack, html, latex,
    latex_raw, latex_booktabs, tsv, or textile
    """
    DEFAULT_TABLEFMT = "fancy_grid"

    @classmethod
    def tabulated(self, data, headers = (), tablefmt = None, numalign = "decimal", stralign = "left"):
        tablefmt = self.DEFAULT_TABLEFMT if tablefmt is None else tablefmt
        return tabulate(data, headers=headers, tablefmt=tablefmt, numalign=numalign, stralign=stralign)

    @classmethod
    def str_with_color(self, value, styles = []):
        if (styles == []):
            return str(value)
        if (type(styles) == int):
            return "\033[{color}m{text}\033[0m".format(color=str(styles), text=str(value))
        styled = "\033["
        for style in styles:
            styled += str(style) + "m\033["
        styled += str(value) + "\033[0m"
        return styled

    @classmethod
    def initialize(self):
        setupLogger()

    @classmethod
    def show(self, value):
        LOGGER.info(value)

    @classmethod
    def error(self, value):
        LOGGER.error(self.str_with_color(value, self.RED))
