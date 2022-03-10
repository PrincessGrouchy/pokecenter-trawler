import os
from datetime import date


class pokecenter_output_reader():
    def setup_method(self):
        self.region = "en-ca"
        # self.region = "en-us"
        # self.region = "en-gb"

        self.current_file = open(
            'pokecenter_output_' + self.region + '_current.txt', 'r', encoding="utf-8")
        self.new_file = open(
            'pokecenter_output_' + self.region + '_new.txt', 'r', encoding="utf-8")
        self.diff_file = open(
            'pokecenter_output_' + self.region + '_diff.txt', 'w', encoding="utf-8")

    def teardown_method(self):
        self.current_file.close()
        self.new_file.close()
        self.diff_file.close()

    def rename_files(self):
        today = date.today()
        os.rename('pokecenter_output_' + self.region + '_current.txt',
                  'pokecenter_output_' + self.region + '_current_{}.txt'.format(today))
        os.rename('pokecenter_output_' + self.region + '_diff.txt',
                  'pokecenter_output_' + self.region + '_diff_{}.txt'.format(today))
        os.rename('pokecenter_output_' + self.region + '_new.txt',
                  'pokecenter_output_' + self.region + '_current.txt')

    def search_lines(self):
        current_lines = self.current_file.readlines()
        new_lines = self.new_file.readlines()

        for new_line in new_lines:
            foundLineMatch = False
            new_line = new_line.replace("\n", "")
            new_no_number = new_line.split(",")
            new_no_number.pop(6)
            new_no_number.pop(0)
            for current_line in current_lines:
                current_no_number = current_line.split(",")
                current_no_number.pop(6)
                current_no_number.pop(0)
                # comparing product numbers
                if current_no_number[1] == new_no_number[1]:
                    foundLineMatch = True
                    self.compare_lines(
                        new_no_number, current_no_number, new_line)
                    break
            if not foundLineMatch:
                self.diff_file.write(
                    "{}, New? couldn't find match\n".format(new_line))
        # search for removed listings
        # there's gotta be a better way :(
        for current_line in current_lines:
            foundLineMatch = False
            current_line = current_line.replace("\n", "")
            current_no_number = current_line.split(",")
            current_no_number.pop(6)
            current_no_number.pop(0)
            for new_line in new_lines:
                new_no_number = new_line.split(",")
                new_no_number.pop(6)
                new_no_number.pop(0)
                # comparing product numbers
                if current_no_number[1] == new_no_number[1]:
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

    # stringToPrint= "{},{},{},{},{},{},{}-{}\n".format(
    # real_number,
    # self.link,
    # product_number,
    # self.name,
    # self.price,
    # in_stock,
    # self.page_count, self.loop_count
    # )


try:
    x = pokecenter_output_reader()
    x.setup_method()
    x.search_lines()
    x.teardown_method()
    x.rename_files()
finally:
    x.teardown_method()
