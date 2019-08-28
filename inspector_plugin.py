# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name			 	 : QGIS Plugin Inspector
Description          : Get various info about active plugins
Date                 : 2019-08-26
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from PyQt5.QtWidgets import QMenu, QToolBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSettings
from qgis.core import QgsProject
from functools import partial
from .inspector_dock import InspectorDock

class InspectorPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.pluginPath = os.path.dirname(__file__)

    def initGui(self):
        self.actionOpen = QAction("Open Inspector", self.iface.mainWindow())
        self.actionOpen.setIcon(QIcon(os.path.join(self.pluginPath, "inspector.png")))
        self.actionOpen.setToolTip("Opens the Inspector window")

        self.iface.addToolBarIcon(self.actionOpen)
        self.iface.addPluginToMenu("Plugin &Inspector", self.actionOpen)
        self.iface.registerMainWindowAction(self.actionOpen, 'F7')
        
        self.actionOpen.triggered.connect(self.openDock)

    def unload(self):
        self.iface.removePluginMenu("Plugin &Inspector",self.actionOpen)
        self.iface.removeToolBarIcon(self.actionOpen)
        self.iface.unregisterMainWindowAction(self.actionOpen)
    
    def openDock(self):
        self.inspectorDock = InspectorDock(self.iface)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.inspectorDock)
        