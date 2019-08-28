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
from PyQt5 import uic
from PyQt5.QtWidgets import QTreeWidgetItem
from qgis.core import QgsApplication
from qgis.utils import plugins, findPlugins

pluginPath = os.path.dirname(__file__)
WIDGET, BASE = uic.loadUiType(os.path.join(pluginPath, 'main_dock.ui'))

class InspectorDock(BASE, WIDGET):
    
    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.iface = iface

        self.profilePath = QgsApplication.qgisSettingsDirPath()
        self.pluginPath = os.path.join(self.profilePath, 'python', 'plugins')

        self.pluginMetadata = findPlugins(self.pluginPath)

        for name, info in self.pluginMetadata:
            self.cmbPlugins.addItem(name, info)

        self.btnInvestigate.clicked.connect(self.inspect)

    def inspect(self):
        suspectName = self.cmbPlugins.currentText()
        suspectConfig = self.cmbPlugins.currentData()
        suspectVersion = suspectConfig.get("general", "version")
        
        self.txtLog.setPlainText(f'Inspecting {suspectName} version {suspectVersion} ... ')

        # # Log metadata
        # for section in suspectConfig.sections():
        #     self.txtLog.appendPlainText(section)
        #     for k, v in dict(suspectConfig[section]).items():
        #         self.txtLog.appendPlainText('\t' + k + ' : ' + v)
        #     self.txtLog.appendHtml('<br>')

        # Log some instance vars
        if not suspectName in plugins:
           self.txtLog.setPlainText(f'Seems like {suspectName} is not activated. Please consult the plugin manager.')
           return

        pluginInstance = plugins[suspectName]
        self.txtLog.appendPlainText(f'Vars of main plugin class "{pluginInstance.__class__.__name__}" ')
        for key, var in vars(pluginInstance).items():
            if hasattr(var, '__dict__'):
                self.txtLog.appendPlainText('\t' + str(key) + ' : ' + str(var.__class__.__name__))
            else:
                self.txtLog.appendPlainText('\t' + str(key) + ' : ' + str(var))
        
        self.treeObjects.clear()
        self.fillTree(suspectName)
    
    def fillTree(self, suspectName):
        pluginInstance = plugins[suspectName]

        rootItem = self.treeObjects.invisibleRootItem()

        self.recursiveInspection(rootItem, pluginInstance, [pluginInstance.__class__.__name__])
        self.treeObjects.addTopLevelItem(rootItem)
        rootItem.setExpanded(True)
        
    def recursiveInspection(self, parent, obj, path):
        """appends a QTreewidgetItem to the given parent"""
        try:
            item = QTreeWidgetItem(parent, [path[-1], str(obj)], 0)
        except:
            print('couldnt create an item')
            item = QTreeWidgetItem(parent, ['',''], 0)
        item.setExpanded(True)
        if ((obj!=None) and (not isinstance(obj, (str,float,int,list,dict,set)))):
            for attr, val in obj.__dict__.items():
                temp_path = path[:]
                temp_path.append(attr)
                try:
                    self.recursiveInspection(item, getattr(obj, attr), temp_path)
                except:
                    pass
        

