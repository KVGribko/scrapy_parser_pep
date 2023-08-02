import csv
from collections import defaultdict
from datetime import datetime

from pep_parse.settings import BASE_DIR, RESULT_DIR, TIME_FORMAT


class PepParsePipeline:
    def open_spider(self, spider):
        self.status = defaultdict(int)

    def process_item(self, item, spider):
        self.status[item["status"]] += 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / RESULT_DIR
        results_dir.mkdir(exist_ok=True)
        time = datetime.now().strftime(TIME_FORMAT)
        file_name = results_dir / f"status_summary_{time}.csv"
        with open(file_name, mode="w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(
                (
                    ("Статус", "Количество"),
                    *self.status.items(),
                    ("Total", sum(self.status.values())),
                )
            )
