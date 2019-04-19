import glob
import os
import sys

from PIL import Image, ImageStat
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QFileDialog, QApplication

global Images_Path
global Path


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # buttons
        QToolTip.setFont(QFont("SansSerif", 10))

        importButton = QPushButton("Load Images", self)
        importButton.setToolTip("Load your images")
        importButton.resize(importButton.sizeHint())
        importButton.move(50, 30)
        importButton.clicked.connect(self.importImages())

        deflickerimages = QPushButton("Deflicker", self)
        deflickerimages.setToolTip("Analyze the flicker of your images")
        deflickerimages.resize(deflickerimages.sizeHint())
        deflickerimages.move(200, 30)
        deflickerimages.clicked.connect(self.deflicker_images())

        exportButton = QPushButton("Save Images", self)
        exportButton.setToolTip("Save your images to [...]")
        exportButton.resize(exportButton.sizeHint())
        exportButton.move(820, 30)
        exportButton.clicked.connect(self.export_images())

        self.setWindowTitle("Timelapse Deflicker")
        self.setGeometry(300, 300, 960, 640)
        self.setMinimumWidth(960)
        self.setMinimumHeight(640)
        self.showMaximized()

    def importImages(self):

        Image_Path = QFileDialog.getExistingDirectory(self, "Open folder", "C:\\Users")
        print(Image_Path)
        counter = 0

        for file in glob.glob(os.path.join(Image_Path, "*.jpg")):
            Images_Path.append(file)
            counter += 1

        global image_count

        print(Images_Path)
        image_count = len(Images_Path)

        print(image_count)

    def deflicker_images(self):
        lumR = [0] * image_count
        lumG = [0] * image_count
        lumB = [0] * image_count

        for i in range(0, image_count):
            image_path = Image.open(Images_Path[i])
            lumR[i], lumG[i], lumB[i] = ImageStat.Stat(image_path).mean
            print(i + 1)

        print(lumR)
        print(lumG)
        print(lumB)

        x1 = 1
        x2 = image_count

        y1_red = float(lumR[0])
        y2_red = float(lumR[image_count - 1])
        y1_green = float(lumG[0])
        y2_green = float(lumG[image_count - 1])
        y1_blue = float(lumB[0])
        y2_blue = float(lumB[image_count - 1])

        m_red = (y2_red - y1_red) / (x2 - x1)
        n_red = y1_red - x1 * m_red
        m_green = (y2_green - y1_green) / (x2 - x1)
        n_green = y1_green - x1 * m_green
        m_blue = (y2_blue - y1_blue) / (x2 - x1)
        n_blue = y1_blue - x1 * m_blue

        ideal_red = [0] * image_count
        ideal_green = [0] * image_count
        ideal_blue = [0] * image_count

        counter = 1

        for image_number in range(1, (image_count + 1)):
            y3_red = m_red * counter + n_red
            y3_green = m_green * counter + n_green
            y3_blue = m_blue * counter + n_blue
            ideal_red[counter - 1] = round(y3_red - lumR[counter - 1])
            ideal_green[counter - 1] = round(y3_green - lumG[counter - 1])
            ideal_blue[counter - 1] = round(y3_blue - lumB[counter - 1])
            counter += 1

        global lumRGB
        lumRGB = [0] * image_number

        for image_number in range(image_number):
            lumRGB[image_number] = ideal_red[image_number] + ideal_green[image_number] + ideal_blue[image_number]
            lumRGB[image_number] = round(lumRGB[image_number] / 3)
            print(image_number)

        print(lumRGB)

    def export_images(self):
        File_Directory_Save = QFileDialog.getExistingDirectory(self, "Save to Folder", "C:\\Users")
        print(File_Directory_Save)

        for i in range(image_count):
            zero = 6 - len(str(i + 1))
            original_image = Image.open(Images_Path[i])
            image_modified = original_image.point(lambda p: p + lumRGB[i])
            image_modified.save((str(File_Directory_Save) + "/" + "Image_" + "0" * zero + str(i + 1) + ".jpg"), 'JPEG',
                                100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec_()
