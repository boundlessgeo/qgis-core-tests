# -*- coding: utf-8 -*-

"""
***************************************************************************
    testerplugin.py
    ---------------------
    Date                 : May 2016
    Copyright            : (C) 2016 by Boundless, http://boundlessgeo.com
                         : (C) 2020 by QCooperative, https://www.qcooperative.net
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'May 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'

import os
import sys

from qgis.core import QgsSettings
from qgis.utils import iface


def functionalTests():
    try:
        from qgistester.test import Test
    except:
        return []

    # advanced setting editing are reset after closing of options gui - #26327
    testAdvancedSettings = Test('Advanced settings editor saves changes')
    testAdvancedSettings.setIssueUrl('https://github.com/qgis/QGIS/issues/26327')
    testAdvancedSettings.addStep('Open QGIS Settings and change some values using Advanced Settings Editor and close dialog by pressing OK button.', prestep=lambda:_showOptions())
    testAdvancedSettings.addStep('Open QGIS Settings again. Check that previously changed settings have correct values.', prestep=lambda:_showOptions(), isVerifyStep=True)

    # adding WMTS from Browser paner - #36264
    testBrowserAddWmts = Test('Adding WMTS from Browser')
    testBrowserAddWmts.setIssueUrl('https://github.com/qgis/QGIS/issues/36264')
    testBrowserAddWmts.addStep('Create test WMTS connection.', function=lambda: _addWmtsConnection())
    testBrowserAddWmts.addStep('Expand "WMS/WMTS" node in the Browser panel. Then expand "TesterPlugin" connection.')
    testBrowserAddWmts.addStep('Try to add layer "112 Par satellite" from the Browser to QGIS canvas. Check that QGIS prompts for date and after setting a date layer added to canvas and visible.')
    testBrowserAddWmts.setCleanup(lambda: _removeWmtsConnection())

    # Verify if message log shows errors
    logTest = Test("Verify in-app message log has no errors for default install. QGIS-62")
    logTest.addStep("Open log messages panel",
                    prestep=lambda:_openLogMessagesDialog())
    logTest.addStep("Review 'General' tab output. Check it has no errors",
                    isVerifyStep=True)
    logTest.addStep("Check there are no errors in 'Plugins' tab",
                    isVerifyStep=True)
    logTest.addStep("If exists, check there are no errors in 'Python warning' tab",
                    isVerifyStep=True)
    logTest.addStep("If exists, check there are no errors in 'Qt' tab",
                    isVerifyStep=True)
    logTest.addStep("Review the Init Script, check there are no errors in 'Qt' tab",
                    isVerifyStep=True)
    logTest.addStep("Review any other existing tabs, check that there are no errors",
                    isVerifyStep=True)

    return [testAdvancedSettings,
            testBrowserAddWmts,
            logTest
           ]


def _showOptions():
    iface.showOptionsDialog(None, 'mOptionsPageSettingsEditor')


def _addWmtsConnection():
    settings = QgsSettings()
    key = 'qgis/connections-wms/TesterPlugin'

    settings.setValue(key + '/url', 'http://wmts.geo.admin.ch/1.0.0/WMTSCapabilities.xml?lang=fr')
    settings.setValue(key + '/dpiMode', 7)
    settings.setValue(key + '/ignoreAxisOrientation', False)
    settings.setValue(key + '/ignoreGetFeatureInfoURI', False)
    settings.setValue(key + '/ignoreGetMapURI', False)
    settings.setValue(key + '/ignoreReportedLayerExtents', False)
    settings.setValue(key + '/invertAxisOrientation', False)
    settings.setValue(key + '/referer', '')
    settings.setValue(key + '/smoothPixmapTransform', False)

    iface.browserModel().reload()

def _removeWmtsConnection():
  settings = QgsSettings()
  settings.remove('qgis/connections-wms/TesterPlugin')
  settings.remove('qgis/WMS/TesterPlugin')
  iface.browserModel().reload()

def _openLogMessagesDialog():
    widgets = [el for el in iface.mainWindow().children() if el.objectName() == "MessageLog"]
    widgets[0].setVisible(True)