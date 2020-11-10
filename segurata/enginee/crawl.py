import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main(*args)-> None:
    """Get a spider name and a config file path and start a spider
    crawler process.
    """

    def _parse_args():
        'Assert crawl arguments are correct and parse them. '
        crawl_args = {}
        for arg in args[1:]:
            arg_name = arg.split("=")[0]
            arg_value = arg.split("=")[1]
            crawl_args[arg_name] = arg_value
        return crawl_args

    process = CrawlerProcess(get_project_settings())
    crawl_args = _parse_args()
    process.crawl(crawl_args['name'], config=crawl_args['config'])
    process.start()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise IndexError('The script takes two arguments.')
    main(*sys.argv)
