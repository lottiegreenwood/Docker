# -*- coding: utf-8 -*-

def main():
    startApplication("sasview")
    mouseClick(waitForObject(":MainWindow_MainSasViewWindow"), 236, -17, 0, Qt.LeftButton)
    test.compare(waitForObjectExists(":qt_workspacechild.FitPage0_FittingWindow").count, 1)
    activateItem(waitForObjectItem(":MainWindow.menubar_QMenuBar", "Fitting"))
    activateItem(waitForObjectItem(":MainWindow.menuFitting_QMenu", "New Fit Page"))
    test.compare(waitForObjectExists(":qt_workspacechild.FitPage0_FittingWindow").count, 2)
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage1_TabItem").text, "FitPage1")
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage1_TabItem").type, "TabItem")
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage1_TabItem").index, 1)
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage1_TabItem").enabled, True)
    activateItem(waitForObjectItem(":MainWindow.menubar_QMenuBar", "Fitting"))
    activateItem(waitForObjectItem(":MainWindow.menuFitting_QMenu", "New Fit Page"))
    test.compare(waitForObjectExists(":qt_workspacechild.FitPage0_FittingWindow").currentIndex, 0)
    test.compare(waitForObjectExists(":qt_workspacechild.FitPage0_FittingWindow").count, 3)
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage2_TabItem").index, 2)
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage2_TabItem").enabled, True)
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage2_TabItem").text, "FitPage2")
    clickButton(waitForObject(":qt_workspacechild_CloseButton"))
    clickButton(waitForObject(":qt_workspacechild_CloseButton_2"))
    test.compare(waitForObjectExists(":qt_workspacechild.FitPage0_FittingWindow").count, 1)
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage2_TabItem").index, 0)
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage2_TabItem").text, "FitPage2")
    clickButton(waitForObject(":qt_workspacechild_CloseButton_3"))
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage3_TabItem").index, 0)
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.FitPage3_TabItem").text, "FitPage3")
    activateItem(waitForObjectItem(":MainWindow.menubar_QMenuBar", "Fitting"))
    activateItem(waitForObjectItem(":MainWindow.menuFitting_QMenu", "Fit Algorithms"))
    test.compare(waitForObjectExists(":FittingOptions_FittingOptions").enabled, True)
    test.compare(waitForObjectExists(":FittingOptions_FittingOptions").visible, True)
    test.compare(str(waitForObjectExists(":FittingOptions_FittingOptions").windowTitle), "Fit Algorithms")
    clickButton(waitForObject(":qt_workspacechild.Cancel_QPushButton"))
    activateItem(waitForObjectItem(":MainWindow.menubar_QMenuBar", "Fitting"))
    activateItem(waitForObjectItem(":MainWindow.menuFitting_QMenu", "Fit Results"))
