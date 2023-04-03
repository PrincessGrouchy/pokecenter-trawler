import os
from datetime import date
import pandas as pd


class pokecenter_output_reader():
    def setup_method(self, the_region):
        self.region = the_region

        self.current_file_name = 'pokecenter_output_' + self.region + '_current.txt'
        self.current_file = pd.read_csv(
            self.current_file_name, encoding="utf-8", header=0,
            names=['link', 'id', 'name', 'price',
                   'in_stock', 'img_link' 'category', 'search_status']
        )
        self.new_file_name = 'pokecenter_output_' + self.region + '_new.txt'
        self.new_file = pd.read_csv(
            self.new_file_name, encoding="utf-8", header=0,
            names=['index', 'link', 'id', 'name', 'price',
                   'in_stock', 'img_link', 'page_position', 'category']
        )
        self.diff_file_name = 'pokecenter_output_' + self.region + '_diff.txt'
        self.diff_file = pd.DataFrame({
            'index': [],
            'link': [],
            'id': [],
            'name': [],
            'price': [],
            'in_stock': [],
            'img_link': [],
            'page_position': [],
            'category': [],
            'change': []
        })

        self.current_complete_file_name = 'pokecenter_output_' + \
            self.region + '_complete.txt'
        self.current_complete_file = pd.read_csv(
            self.current_complete_file_name, encoding="utf-8", header=0,
            names=['link', 'id', 'name', 'price',
                   'in_stock', 'category', 'search_status']
        )
        self.new_complete_file_name = 'pokecenter_output_' + \
            self.region + '_complete_new.txt'
        self.new_complete_file = pd.DataFrame({
            'link': [],
            'id': [],
            'name': [],
            'price': [],
            'in_stock': [],
            'img_link': [],
            'category': [],
            'search_status': []
        })

    def teardown_method(self):
        self.current_file.close()
        self.new_file.close()
        self.diff_file.close()
        self.current_complete_file.close()
        self.new_complete_file.close()

    def rename_files(self):
        today = date.today()
        os.rename('pokecenter_output_' + self.region + '_current.txt',
                  'past_pages/' + 'pokecenter_output_' + self.region + '_current_{}.txt'.format(today))
        os.rename('pokecenter_output_' + self.region + '_diff.txt',
                  'pokecenter_output_' + self.region + '_diff_{}.txt'.format(today))
        os.rename('pokecenter_output_' + self.region + '_new.txt',
                  'pokecenter_output_' + self.region + '_current.txt')
        os.remove('pokecenter_output_' + self.region + '_complete.txt')
        os.rename('pokecenter_output_' + self.region + '_complete_new.txt',
                  'pokecenter_output_' + self.region + '_complete.txt')

    def search_lines(self):
        current_lines = self.current_file.readlines()
        self.new_lines = self.new_file.readlines()

        for new_line in self.new_lines:
            foundLineMatch = False

            for current_line in current_lines:
                # comparing product numbers
                if current_line['id'] == current_line['id']:
                    foundLineMatch = True
                    self.compare_lines(
                        new_line, current_line, new_line)
                    break
            if not foundLineMatch:
                self.diff_file.append(
                    "{}, New? couldn't find match\n".format(new_line))
        # search for removed listings
        # there's gotta be a better way :(
        for current_line in current_lines:
            foundLineMatch = False

            for new_line in self.new_lines:

                # comparing product numbers
                if current_line['id'] == new_line['id']:
                    foundLineMatch = True
                    # self.compare_lines(
                    #     new_no_number, current_no_number, new_line)
                    break
            if not foundLineMatch:
                self.diff_file.write(
                    "{}, missing! might have been delisted\n".format(current_line))

    def compare_lines(self, new_no_number, current_no_number, new_line):
        foundDifference = False
        differencesList = []
        for new_var, current_var in zip(new_no_number, current_no_number):
            if new_var != current_var:
                foundDifference = True
                differencesList.append(
                    "{} used to be {}. ".format(new_var, current_var))
        if foundDifference:
            self.diff_file.write("{}, Difference: {} \n".format(
                new_line, ''.join(differencesList)))
        return foundDifference

    # stringToPrint = "{},{},{},{},{},{},{}-{},{}\n".format(
    # real_number,
    # self.link,
    # product_number,
    # self.name,
    # self.price,
    # in_stock,
    # self.page_count, self.loop_count,
    # self.category.replace("/", "")
    # )

# I mean, there's definitely a better way to do this
#  oh well, gotta get me some O^2
    def search_lines_complete(self):
        current_complete_lines = self.current_complete_file.readlines()
        # new_lines = self.new_file.readlines() # can you not do this twice??

        for new_line in self.new_lines:
            foundLineMatch = False
            new_line = new_line.replace("\n", "")
            new_no_number = new_line.split(",")
            new_no_number.pop(6)
            new_no_number.pop(0)
            new_no_number.append("searchable")
            for current_complete_line in current_complete_lines:
                current_complete_line = current_complete_line.replace("\n", "")
                current_no_number = current_complete_line.split(",")
                # comparing product numbers
                if current_no_number[1] == new_no_number[1]:
                    foundLineMatch = True
                    self.new_complete_file.write(
                        "{}\n".format(','.join(new_no_number)))
                    self.compare_lines_complete_print(
                        new_no_number, current_no_number, new_line)
                    break
            if not foundLineMatch:
                self.new_complete_file.write(
                    "{}\n".format(','.join(new_no_number)))
                # print("(complete) {}, New? couldn't find match\n".format(
                #     ','.join(new_no_number)))
        # search for removed listings
        # there's gotta be a better way :(
        for current_complete_line in current_complete_lines:
            foundLineMatch = False
            current_complete_line = current_complete_line.replace("\n", "")
            current_no_number = current_complete_line.split(",")
            for new_line in self.new_lines:
                new_line = new_line.replace("\n", "")
                new_no_number = new_line.split(",")
                new_no_number.pop(6)
                new_no_number.pop(0)
                new_no_number.append("searchable")
                # comparing product numbers
                if current_no_number[1] == new_no_number[1]:
                    foundLineMatch = True
                    # self.new_complete_file.write(
                    #     "{}\n".format(new_no_number))
                    break
            if not foundLineMatch:
                current_no_number.pop()
                current_no_number.append(
                    "delisted, missing {}".format(date.today()))
                self.new_complete_file.write(
                    "{}\n".format(','.join(current_no_number)))
                # print("(complete) {}, missing! might have been delisted\n".format(
                #     ','.join(current_no_number)))

    def compare_lines_complete_print(self, new_no_number, current_no_number, new_line):
        foundDifference = False
        differencesList = []
        for new_var, current_var in zip(new_no_number, current_no_number):
            if new_var != current_var:
                foundDifference = True
                differencesList.append(
                    "{} used to be {}. ".format(new_var, current_var))
        if foundDifference:
            print("(complete) {}, Difference: {} \n".format(
                new_line, ''.join(differencesList)))
        return foundDifference


regions = ["jp-jp"]
reader = pokecenter_output_reader()
for the_region in regions:
    try:
        reader.setup_method(the_region)
        reader.search_lines()
        reader.search_lines_complete()
        reader.teardown_method()
        reader.rename_files()
    finally:
        reader.teardown_method()
