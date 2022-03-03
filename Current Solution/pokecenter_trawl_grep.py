import os
from datetime import date

class pokecenter_output_reader():
    def setup_method(self):
        self.current_file = open('pokecenter_output_current.txt', 'r', encoding="utf-8")
        self.new_file = open('pokecenter_output_new.txt', 'r', encoding="utf-8")
        self.diff_file = open('pokecenter_output_diff.txt', 'w', encoding="utf-8")

    def teardown_method(self):
        self.current_file.close()
        self.new_file.close()
        self.diff_file.close()

    def rename_files(self):
        today = date.today()
        os.rename('pokecenter_output_current.txt', "pokecenter_output_current_{}.txt".format(today))
        os.rename('pokecenter_output_diff.txt', "pokecenter_output_diff_{}.txt".format(today))
        os.rename('pokecenter_output_new.txt', "pokecenter_output_current.txt".format(today))

    def search_lines(self):
        current_lines = self.current_file.readlines()
        new_lines = self.new_file.readlines()

        for new_line in new_lines:
            foundLineMatch = False
            new_line = new_line.replace("\n","")
            new_no_number = new_line.split(",")
            new_no_number.pop(6)
            new_no_number.pop(0)
            for current_line in current_lines:
                current_no_number = current_line.split(",")
                current_no_number.pop(6)
                current_no_number.pop(0)
                if current_no_number[1] == new_no_number[1]:
                    foundLineMatch = True
                    self.compare_lines(new_no_number, current_no_number, new_line)
                    break
            if not foundLineMatch:
                self.diff_file.write("{}, couldn't find match\n".format(new_line))

    def compare_lines(self, new_no_number, current_no_number, new_line):
        foundDifference = False
        differencesList = []
        for new_var, current_var in zip(new_no_number, current_no_number):
            if new_var != current_var:
                foundDifference = True
                differencesList.append("{} used to be {}. ".format(new_var, current_var))
        if foundDifference:
            self.diff_file.write("{}, Difference: {} \n".format(new_line, ''.join(differencesList)))
        return foundDifference


    # self.file1.write(
    # "{},".format(realnumber)
    # + "{},".format(self.vars["link"])
    # + "{},".format(product_number)
    # + "{},".format(self.vars["name"])
    # + "{},".format(self.vars["price"])
    # + "{},".format(in_stock)
    # + "{}-{}".format(self.vars["page_count"], self.vars["loop_count"])
    # + '\n')

try:
  x = pokecenter_output_reader()
  x.setup_method()
  x.search_lines()
  x.teardown_method()
  x.rename_files()
finally:
  x.teardown_method()
