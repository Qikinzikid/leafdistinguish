# coding:utf-8
import sys
from UI_Leaf import Ui_LeafWindow
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class LeafWindow(QMainWindow, Ui_LeafWindow):
    def __init__(self):
        super(LeafWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.fname_saves_name=""

    def Select(self):
        fname_saves = QFileDialog.getOpenFileName(
            self, '选择检测对象', "./", "(*.jpg)")
        if fname_saves[0]!="":
            self.fname_saves_name = fname_saves[0]
            self.FIGSHOW(self.fname_saves_name)

    def Feature(self,TrainName, TestName):
        Fig = []
        FigGray = []
        KP = []
        Des = []
        Match = []
        for temp in list(range(1, 30)):
            if 0 < temp <= 9:
                img = cv2.imread(TestName)
                fig = cv2.imread("./FIG/" + TrainName + "0" + str(temp) + ".jpg")
                Fig.append(fig)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                fig_gray = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
                FigGray.append(fig_gray)

                detect = cv2.xfeatures2d.SIFT_create(800)
                kp, des = detect.detectAndCompute(gray, None)
                temp_result = detect.detectAndCompute(fig_gray, None)

                KP.append(temp_result[0])
                Des.append(temp_result[1])

                bf = cv2.BFMatcher()
                Match.append(bf.knnMatch(des, temp_result[1], k=2))

            else:
                img = cv2.imread(TestName)
                fig = cv2.imread("./FIG/" + TrainName + str(temp) + ".jpg")
                Fig.append(fig)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                fig_gray = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
                FigGray.append(fig_gray)

                detect = cv2.xfeatures2d.SIFT_create(800)
                kp, des = detect.detectAndCompute(gray, None)
                temp_result = detect.detectAndCompute(fig_gray, None)
                KP.append(temp_result[0])
                Des.append(temp_result[1])

                bf = cv2.BFMatcher()
                Match.append(bf.knnMatch(des, temp_result[1], k=2))

        return Match

    # 图片显示
    def FIGSHOW(self,path):
        image = QPixmap()
        image.load(path)
        self.graphicsView.scene = QGraphicsScene()  # 创建一个图片元素的对象
        item = QGraphicsPixmapItem(image)  # 创建一个变量用于承载加载后的图片
        self.graphicsView.scene.addItem(item)  # 将加载后的图片传递给scene对象
        self.graphicsView.setScene(self.graphicsView.scene)
        self.graphicsView.sceneRect()

    def Run(self):
        DuJuan = self.Feature("DuJuan", self.fname_saves_name)
        BaJiaoJinPan = self.Feature("BaJiaoJinPan", self.fname_saves_name)
        WuTong = self.Feature("WuTong", self.fname_saves_name)
        YinXing = self.Feature("YinXing", self.fname_saves_name)

        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        for i in list(range(29)):
            for m, n in DuJuan[i]:
                if m.distance < 0.55 * n.distance:
                    sum1 = sum1 + 1

        for i in list(range(29)):
            for m, n in BaJiaoJinPan[i]:
                if m.distance < 0.55 * n.distance:
                    sum2 = sum2 + 1

        for i in list(range(29)):
            for m, n in WuTong[i]:
                if m.distance < 0.55 * n.distance:
                    sum3 = sum3 + 1

        for i in list(range(29)):
            for m, n in YinXing[i]:
                if m.distance < 0.55 * n.distance:
                    sum4 = sum4 + 1

        if max(sum1, sum2, sum3, sum4) == sum1:
            QMessageBox.about\
                (self, u'结果', u"杜鹃")

        if max(sum1, sum2, sum3, sum4) == sum2:
             QMessageBox.about \
                (self, u'结果', u"八角金盘")

        if max(sum1, sum2, sum3, sum4) == sum3:
            QMessageBox.about \
                (self, u'结果', u"梧桐")
        if max(sum1, sum2, sum3, sum4) == sum4:
            QMessageBox.about \
                (self, u'结果', u"银杏")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    leafwindow = LeafWindow()
    leafwindow.show()
    sys.exit(app.exec_())
