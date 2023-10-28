import cv2
from scipy.spatial.transform import Rotation as R

from MainWindow_ui import Ui_MainWindow
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsEllipseItem,QGraphicsRectItem, QGraphicsItemGroup
from PySide6.QtGui import QPixmap, QPen, QColor, QBrush, QVector3D
from PySide6.QtWidgets import *
from PySide6.QtCore import QTranslator
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, BarGraphItem, PlotItem, PlotDataItem, Vector
import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLScatterPlotItem, GLMeshItem, MeshData
from TOFCam import TOFCam
import pyvista as pv
from pyvista import _vtk as vtk

class MainWindow(QMainWindow, Ui_MainWindow):


    def __init__(self, par=None):
        self.cam = TOFCam("COM3", 115200, 3, 5, 100, 100, 65, 65)
        self.cam.dataUpdated.connect(self.cam_dataUpdated)
        self.cam.start()
        self.updated = False
        super().__init__(par)
        self.setupUI()

    def setupUI(self):
        super().setupUi(self)

        #view = gl.GLViewWidget()
        #view.show()
        self.plotWidget.show()
        ## create three grids, add each to the view
        self.data = GLScatterPlotItem()

        rect = gl.GLSurfacePlotItem()
        colors = (((0,0,255,100),(0,0,255,100)),(((0,0,255,100)),(0,0,255,100)))
        rect.setData(x=np.array((0,60)),y=np.array((0,163)),z=np.array(((765,765),(765,765))),colors=colors)
        rect.translate(dx=-30.0,dy=-81.5,dz=0)
        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()
        xaxis = gl.GLAxisItem()
        xaxis.setSize(400,0,0)
        xaxis.translate(-200,0,0)
        yaxis = gl.GLAxisItem()
        yaxis.setSize(0,400,0)
        yaxis.translate(0,-200,0)
        zaxis = gl.GLAxisItem()
        zaxis.setSize(0,0,400)
        zaxis.translate(0,0,-200)

        #self.plotWidget.addItem(xgrid)
        #self.plotWidget.addItem(ygrid)
        #self.plotWidget.addItem(zgrid)
        #self.plotWidget.addItem(rect)
        self.plotWidget.addItem(xaxis)
        self.plotWidget.addItem(yaxis)
        self.plotWidget.addItem(zaxis)
        self.plotWidget.addItem(self.data)
        #pos:Vector = Vector()
        self.plotWidget.setCameraPosition(pos=Vector(0,0,-500),azimuth=180,elevation=-90)
        self.ax = 0.0
        self.ay = 10.0
        self.az = 3.0
        self.tx = 0.0
        self.ty = 0.0
        self.tz = 0.0
        self.rotXBox.setValue(self.ax)
        self.rotYBox.setValue(self.ay)
        self.rotZBox.setValue(self.az)
        self.rotXBox.valueChanged.connect(self.rotXBox_valueChanged)
        self.rotYBox.valueChanged.connect(self.rotYBox_valueChanged)
        self.rotZBox.valueChanged.connect(self.rotZBox_valueChanged)
        self.tlXBox.valueChanged.connect(self.tlXBox_valueChanged)
        self.tlYBox.valueChanged.connect(self.tlYBox_valueChanged)
        self.tlZBox.valueChanged.connect(self.tlZBox_valueChanged)

        ## rotate x and y grids to face the correct direction
        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)
        zgrid.rotate(90, 0, 0, 1)

        ## scale each grid differently
        xgrid.scale(0.1, 0.1, 0.1)
        ygrid.scale(0.1, 0.1, 0.1)
        zgrid.scale(1, 1, 1)

    def rotXBox_valueChanged(self, value):
        self.ax = value

    def rotYBox_valueChanged(self, value):
        self.ay = value

    def rotZBox_valueChanged(self, value):
        self.az = value

    def tlXBox_valueChanged(self, value):
        self.tx = value

    def tlYBox_valueChanged(self, value):
        self.ty = value

    def tlZBox_valueChanged(self, value):
        self.tz = value

    def cam_dataUpdated(self, frame:np.ndarray):
        print("new frame")

        #RM =  self.rotate_matrix(self.ax, self.ay, self.az)
        rot_frame = self.move_and_rotate(frame)
        #rot_frame = np.dot(RM, frame.T)
        hst_y = np.histogram2d(rot_frame[:,0], rot_frame[:,2], [255,255])
        hst_y = np.round(hst_y[0] * (255.0/hst_y[0].max())).astype(dtype=np.uint8)
        hst_x = np.histogram2d(rot_frame[:,1], rot_frame[:,2], [255,255])
        hst_x = np.round(hst_x[0] * (255.0/hst_x[0].max())).astype(dtype=np.uint8)
        hst_z = np.histogram2d(rot_frame[:,0], rot_frame[:,1], [255,255])
        hst_z = np.round(hst_z[0] * (255.0/hst_z[0].max())).astype(dtype=np.uint8)
        cv2.imwrite("y.png", hst_y)
        cv2.imwrite("x.png", hst_x)
        cv2.imwrite("z.png", hst_z)
        self.data.setData(pos = rot_frame, color=(0,1,0,1), size=0.1)
        #    self.updated = True

    def move_and_rotate(self,frame):
        h_frame = np.hstack((frame, np.ones((frame.shape[0], 1))))
        T_mat = np.eye(4)
        T_mat[:3,:3] = self.rotate_matrix(self.ax, self.ay,self.az)[:3,:3]
        T_mat[:3, 3] = np.array([self.tx,self.ty,self.tz])
        new_points = np.dot(T_mat, h_frame.T).T
        return new_points[:,:3] /  new_points[:,3][:,np.newaxis]

    def rotate_matrix(self, ax, ay, az):
        cos_x = np.cos(ax * np.pi /180)
        sin_x = np.sin(ax * np.pi / 180)
        cos_y = np.cos(ay * np.pi /180)
        sin_y = np.sin(ay * np.pi / 180)
        cos_z = np.cos(az * np.pi /180)
        sin_z = np.sin(az * np.pi / 180)
        r_x = np.array([[1, 0, 0, 0], [0, cos_x, -sin_x, 0], [0, sin_x, cos_x, 0], [0, 0, 0, 1]])
        r_y = np.array([[cos_y, 0, sin_y, 0], [0, 1, 0, 0], [sin_y, 0, cos_y, 0], [0, 0, 0, 1]])
        r_z = np.array([[cos_z, -sin_z, 0, 0], [sin_z, cos_z, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        rotVec = np.array([ax * np.pi / 180, ay * np.pi / 180, az * np.pi / 180])
        #return R.from_euler('XYZ', rotVec).as_matrix(), r_x @ r_y @ r_z
        return r_x @ r_y @ r_z

if __name__ == "__main__":

    import sys
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    #
    # sys.exit(app.exec())
    #pg.mkQApp()

    main.show()
    ## Start the Qt event loop
    app.exec()