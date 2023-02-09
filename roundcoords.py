# -*- coding: utf-8 -*-
'''
/***************************************************************************
 roundCoords for openland (cadastral engineer tools)
 copyright            : (C) 2012 by Dmitriy Biryuchkov
 email                : biryuchkov@gmail.com
 ***************************************************************************/
'''
#from PyQt4.QtCore import *
from qgis.PyQt.QtWidgets import QMessageBox, QProgressBar
from qgis.core import *
#from common import *


class RoundCoords:
    def __init__(self, iface, iround):

        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.iround=iround

        self.currentSpEl    = 0


    def toPrepare(self):
        layer = self.iface.mainWindow().activeLayer()
        selection = layer.selectedFeatures()
        l = len(selection)
        if l >= 1:

            return True
        else:
            QMessageBox.warning(self.iface.mainWindow(), u"Ошибка выбора данных", 
                                                        u'Необходимо выбрать не менее одного объекта векторного слоя.')
            return False

    def doRound(self, layer):
        #layer = self.iface.mainWindow().activeLayer()
        caps = layer.dataProvider().capabilities()
        selection = layer.selectedFeatures()
        featSelected=layer.selectedFeatureCount()

        #iround = int(self.spinBox.value())
        if (self.iround < 0):
            QMessageBox.warning(self.iface.mainWindow(), u"Ошибка параметра округления", 
                                                        u"Необходимо указать параметр округления не менее 0")
            return

        #self.progress       = QProgressBar()
        #progressMessageBar  = self.iface.messageBar().createMessage(u'Округление координат точек полигонов ЗУ...')
        #self.progress.setMaximum(featSelected)
        #self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        #progressMessageBar.layout().addWidget(self.progress)
        #self.iface.messageBar().pushWidget(progressMessageBar,                                         self.iface.messageBar().INFO)
        for s in selection:
            fid     = s.id()
            geom    = QgsGeometry(s.geometry())
            polygon1 = True
            ring1   = True
            xprev   = 0.0
            yprev   = 0.0
            if geom.isMultipart():
                polygons = geom.asMultiPolygon()
                for poly in polygons:
                    ring1 = True
                    for ring in poly:
                        self.currentSpEl += 1
                        #self.progress.setValue(self.currentSpEl)

                        polygon = []
                        for i in ring:
                            xnew = round(i.x(), self.iround)
                            ynew = round(i.y(), self.iround)
                            point = QgsGeometry.fromPointXY(QgsPointXY(xnew, ynew))
                            
                            #if self.checkBoxDeleteDouble.isChecked():
                                #if xnew != xprev or ynew != yprev:
                                    #polygon.append(point.asPoint())
                                    #xprev = xnew
                                    #yprev = ynew

                            #else:
                            polygon.append(point.asPoint())

                        if (ring1):
                            geompart = QgsGeometry().fromPolygonXY([polygon])
                            ring1 = False

                            if (polygon1):
                                geomnew = geompart
                                polygon1 = False
                            else:
                                geomnew.addPart(polygon)
                        else:
                            geomnew.addRing(polygon)
            else:
                rings = geom.asPolygon()
                for ring in rings:
                    self.currentSpEl += 1
                    #self.progress.setValue(self.currentSpEl)
                    
                    polygon = []
                    for i in ring:
                        xnew = round(i.x(), self.iround)
                        ynew = round(i.y(), self.iround)
                        point = QgsGeometry.fromPointXY(QgsPointXY(xnew, ynew))

                        #if self.checkBoxDeleteDouble.isChecked():
                            #if xnew != xprev or ynew != yprev:
                                #polygon.append(point.asPoint())
                                #xprev = xnew
                                #yprev = ynew

                        #else:
                        polygon.append(point.asPoint())

                    if (ring1):
                        geomnew = QgsGeometry().fromPolygonXY([polygon])
                        ring1 = False
                    else:
                        geomnew.addRing(polygon)

            if caps & QgsVectorDataProvider.ChangeGeometries:
                layer.startEditing()
                if layer.changeGeometry(fid, geomnew):
                    layer.commitChanges()
                else:
                    layer.rollBack()
                    QMessageBox.warning(self.iface.mainWindow(), u"Ошибка редактирования векторного объекта", 
                                                                u"Невозможно редактирование векторного объекта")
            else:
                QMessageBox.warning(self.iface.mainWindow(), u"Ошибка редактирования векторного слоя", 
                                                            u"Невозможно редактирование/добавление объекта для выбранного слоя")
        #del self.progress
        #del progressMessageBar
        #self.iface.messageBar().clearWidgets()
        self.canvas.refresh()
        #self.close()

    def doCancel(self):
        self.close()

#        QMessageBox.information(self.iface.mainWindow(), u'test', str())
