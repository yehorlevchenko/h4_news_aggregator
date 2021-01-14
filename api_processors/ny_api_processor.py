from api_processors.api_processor import APIProcessor
import logging


class NYAPIProcessor(APIProcessor):

    def __init__(self):
        super().__init__()
        self.url = "https://api.nytimes.com/svc/news/v3/content/all/podcasts.json"
        self.api_key = "6LWMg0c19nLU7dKwBR6QRXQ5A6elwqmp"
        self.news_fields = ["slug_name", "section", "subsection", "title",
                            "abstract", "url", "byline", "source",
                            "published_date", "kicker", "subheadline",
                            "related_urls", "multimedia"]
        self.log = logging.getLogger(__name__)

    def _clean_data(self, raw_data):
        clean_data = list()
        raw_news = raw_data['results']
        if not raw_news:
            self.log.error(f'{__name__} - _clean_data - '
                           f"can't received {raw_news}")
            raise RuntimeError("No news in received data")
        for item in raw_news:
            cleaned_data = {k: v for k, v in item.items()
                            if k in self.news_fields}
            clean_data.append(cleaned_data)
            self.log.info(f"{__name__} - _clean_data")

        return clean_data


if __name__ == '__main__':
    t = NYAPIProcessor()
    t.refresh_data()
