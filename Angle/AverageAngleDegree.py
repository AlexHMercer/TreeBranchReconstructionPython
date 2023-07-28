import numpy as np
from xlwings import App
import os


class AverageAngleDegree:
    app = None
    wb = None

    def __init__(self, base_filename, index, end_index):
        self.end_index = end_index
        self.tree_id = index
        filename = "../resource/" + base_filename + "_angles/" + str(index) + "_angles_full_info.txt"
        self.infos = np.loadtxt(filename, delimiter=",")[:, -7:]
        self.file = open("../resource/" + base_filename + "_average_tree_angles.csv", "a")
        # 创建excel文件
        AverageAngleDegree.open_excel(index, base_filename)
        self.sheet = AverageAngleDegree.wb.sheets["sheet1"]
        self.level_mapper = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: []}
        self.string = "abcdefghijklmnopqrstuvwxyz"

    def generate_infos(self):
        for line in self.infos:
            direction1 = line[:3]
            direction2 = line[3:6]
            tree_id = int(line[6])
            cos_value = np.sum(direction1*direction2) / (np.sqrt(np.sum(direction1**2)) * np.sqrt(np.sum(direction2**2)))
            degree_value = np.arccos(cos_value) / np.pi * 180
            self.level_mapper[tree_id].append(degree_value)

    def run(self):
        self.generate_infos()
        print(self.level_mapper)
        line = ""
        counter = 0
        for key in self.level_mapper.keys():
            if counter < 26:
                cell = self.string[counter] + str(self.tree_id + 1)
            else:
                cell = self.string[(counter // 26) - 1] + self.string[(counter % 26)] + str(self.tree_id + 1)
            counter += 1
            cell_value = "level_" + str(key)
            self.sheet.range(cell).value = cell_value

            degrees = self.level_mapper[key]
            if len(degrees) > 0:
                value = np.mean(np.array(degrees))
                for degree in degrees:
                    if counter < 26:
                        cell = self.string[counter] + str(self.tree_id + 1)
                    else:
                        cell = self.string[(counter // 26) - 1] + self.string[(counter % 26)] + str(self.tree_id + 1)
                    counter += 1
                    # print(cell)
                    self.sheet.range(cell).value = degree
            else:
                value = 0
            if key == 8:
                line += str(value)
            else:
                line += str(value) + ","

        self.file.write(line + "\n")
        self.file.close()

        if self.tree_id == self.end_index - 1:
            AverageAngleDegree.destroy_excel()

    @staticmethod
    def open_excel(index, base_filename):
        if index != 1:
            return

        filename = "../resource/" + base_filename + "_tree_full_angles.xlsx"
        if index == 0 and os.path.exists(filename):
            os.remove(filename)

        app = App(visible=False, add_book=False)
        wb = app.books.add()
        wb.save(filename)
        wb.close()
        wb = app.books.open(filename)
        AverageAngleDegree.app = app
        AverageAngleDegree.wb = wb

    @staticmethod
    def destroy_excel():
        AverageAngleDegree.wb.save()
        AverageAngleDegree.wb.close()
        AverageAngleDegree.app.quit()
        AverageAngleDegree.app.kill()


def main():
    for index in range(20):
        base_filename = "../resource/five_years"
        average_angle_degree = AverageAngleDegree(base_filename, index)
        average_angle_degree.run()


if __name__ == "__main__":
    main()
