import pandas as pd
from datetime import date


class pokecenter_strip_dupes():
    def setup_method(self, the_region, the_date=date.today()):
        self.region = the_region

        # self.current_file_name = 'pokecenter_output_' + self.region + '_current.txt'
        # self.current_file = pd.read_csv(
        #     'pokecenter_output_' + self.region + '_current.txt', encoding="utf-8",
        #     names=['relative_position', 'link', 'id', 'name',
        #            'price', 'in_stock', 'page_position', 'category']
        # )
        self.diff_file_name = 'pokecenter_output_' + \
            self.region + '_diff_{}.txt'.format(the_date)
        self.diff_file = pd.read_csv(
            self.diff_file_name, encoding="utf-8",
            names=['relative_position', 'link', 'id', 'name', 'price',
                   'in_stock', 'page_position', 'category', 'change']
        )
        self.complete_file_name = 'pokecenter_output_' + self.region + '_complete.txt'
        self.complete_file = pd.read_csv(
            self.complete_file_name, encoding="utf-8", header=0,
            names=['link', 'id', 'name', 'price',
                   'in_stock', 'category', 'search_status']
        )

    def deduplicate(self, file, filename):
        file = file.sort_values(by=["link"], ascending=True)
        file.drop_duplicates(subset=['link', 'id'], inplace=True)
        file.to_csv(filename, index=False)

    def run_dedupe(self):
        # self.deduplicate(self.current_file, self.current_file_name)
        self.deduplicate(self.diff_file, self.diff_file_name)
        self.deduplicate(self.complete_file, self.complete_file_name)


regions = ["en-ca", "en-gb", "en-us", "jp-jp"]
reader = pokecenter_strip_dupes()
for the_region in regions:
    reader.setup_method(the_region)
    ## manual mode
    # reader.setup_method(the_region, date(2023, 01, 17))
    reader.run_dedupe()
