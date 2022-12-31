import os
import pandas as pd
from datetime import date


class pokecenter_strip_dupes():
    def setup_method(self, the_region):
        self.region = the_region

        # self.current_file = pd.read_csv(
        #     'pokecenter_output_' + self.region + '_current.txt', encoding="utf-8",
        #     names=['relative_position', 'link', 'id', 'name',
        #            'price', 'in_stock', 'page_position', 'category']
        # )
        self.complete_file = pd.read_csv(
            'pokecenter_output_' + self.region + '_complete.txt', encoding="utf-8",
            names=['link', 'id', 'name', 'price',
                   'in_stock', 'category', 'search_status']
        )

    def teardown_method(self):
        # self.current_file.close()
        self.complete_file.close()

    def deduplicate(self, file):
        self.current_lines = file.readlines()
        self.current_lines.drop_duplicates(subset=['link', 'id'], inplace=True)
        self.current_lines.to_csv(file)

    def run_dedupe(self):
        # self.deduplicate(self.current_file)
        self.deduplicate(self.complete_file)


regions = ["en-ca", "en-gb", "en-us", "jp-jp"]
reader = pokecenter_strip_dupes()
for the_region in regions:
    try:
        reader.setup_method(the_region)
        reader.run_dedupe()
        reader.teardown_method()
    finally:
        reader.teardown_method()
