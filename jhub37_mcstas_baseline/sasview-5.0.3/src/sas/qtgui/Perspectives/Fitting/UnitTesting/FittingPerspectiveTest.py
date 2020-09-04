import sys
import unittest
import webbrowser

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtTest
from PyQt5 import QtCore
from unittest.mock import MagicMock

# set up import paths
import sas.qtgui.path_prepare

# Local
import sas.qtgui.Utilities.GuiUtils as GuiUtils
from sas.qtgui.Plotting.PlotterData import Data1D
from sas.qtgui.Perspectives.Fitting.FittingPerspective import FittingWindow

if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)


class FittingPerspectiveTest(unittest.TestCase):
    '''Test the Fitting Perspective'''
    def setUp(self):
        class dummy_manager(object):
            def communicator(self):
                return GuiUtils.Communicate()
            communicate = GuiUtils.Communicate()

        '''Create the perspective'''
        self.widget = FittingWindow(dummy_manager())

    def tearDown(self):
        '''Destroy the perspective'''
        self.widget.close()
        self.widget = None

    def testDefaults(self):
        '''Test the GUI in its default state'''
        self.assertIsInstance(self.widget, QtWidgets.QWidget)
        self.assertIn("Fit panel", self.widget.windowTitle())
        self.assertEqual(self.widget.optimizer, "Levenberg-Marquardt")
        self.assertEqual(len(self.widget.tabs), 1)
        self.assertEqual(self.widget.maxIndex, 2)
        self.assertEqual(self.widget.getTabName(), "FitPage2")

    def testAddTab(self):
        '''Add a tab and test it'''

        # Add an empty tab
        self.widget.addFit(None)
        self.assertEqual(len(self.widget.tabs), 2)
        self.assertEqual(self.widget.getTabName(), "FitPage3")
        self.assertEqual(self.widget.maxIndex, 3)
        # Add an empty batch tab
        self.widget.addFit(None, is_batch=True)
        self.assertEqual(len(self.widget.tabs), 3)
        self.assertEqual(self.widget.getTabName(2), "BatchPage4")
        self.assertEqual(self.widget.maxIndex, 4)

    def testAddCSTab(self):
        ''' Add a constraint/simult tab'''
        self.widget.addConstraintTab()
        self.assertEqual(len(self.widget.tabs), 2)
        self.assertEqual(self.widget.getCSTabName(), "Const. & Simul. Fit")

    def testResetTab(self):
        ''' Remove data from last tab'''
        self.assertEqual(len(self.widget.tabs), 1)
        self.assertEqual(self.widget.getTabName(), "FitPage2")
        self.assertEqual(self.widget.maxIndex, 2)

        # Attempt to remove the last tab
        self.widget.resetTab(0)

        # see that the tab didn't disappear, just changed the name/id
        self.assertEqual(len(self.widget.tabs), 1)
        self.assertEqual(self.widget.getTabName(), "FitPage3")
        self.assertEqual(self.widget.maxIndex, 3)

        # Now, add data
        data = Data1D(x=[1,2], y=[1,2])
        GuiUtils.dataFromItem = MagicMock(return_value=data)
        item = QtGui.QStandardItem("test")
        self.widget.setData([item])
        # Assert data is on widget
        self.assertEqual(len(self.widget.tabs[0].all_data), 1)
        # Reset the tab
        self.widget.resetTab(0)
        # See that the tab contains data no more
        self.assertEqual(len(self.widget.tabs[0].all_data), 0)

    def testCloseTab(self):
        '''Delete a tab and test'''
        # Add an empty tab
        self.widget.addFit(None)

        # Remove the original tab
        self.widget.tabCloses(1)
        self.assertEqual(len(self.widget.tabs), 1)
        self.assertEqual(self.widget.maxIndex, 3)
        self.assertEqual(self.widget.getTabName(), "FitPage3")

        # Attemtp to remove the last tab
        self.widget.tabCloses(1)
        # The tab should still be there
        self.assertEqual(len(self.widget.tabs), 1)
        self.assertEqual(self.widget.maxIndex, 4)
        self.assertEqual(self.widget.getTabName(), "FitPage4")

    def testAllowBatch(self):
        '''Assure the perspective allows multiple datasets'''
        self.assertTrue(self.widget.allowBatch())

    def testSetData(self):
        ''' Assure that setting data is correct'''
        with self.assertRaises(AssertionError):
            self.widget.setData(None)

        with self.assertRaises(AttributeError):
            self.widget.setData("BOOP")

        # Mock the datafromitem() call from FittingWidget
        data = Data1D(x=[1,2], y=[1,2])
        GuiUtils.dataFromItem = MagicMock(return_value=data)

        item = QtGui.QStandardItem("test")
        self.widget.setData([item])

        # First tab should accept data
        self.assertEqual(len(self.widget.tabs), 1)

        # Add another set of data
        self.widget.setData([item])

        # Now we should have two tabs
        self.assertEqual(len(self.widget.tabs), 2)

        # Add two more items in a list
        self.widget.setData([item, item])

        # Check for 4 tabs
        self.assertEqual(len(self.widget.tabs), 4)

    def testSwapData(self):
        '''Assure that data swapping is correct'''

        # Mock the datafromitem() call from FittingWidget
        data1 = Data1D(x=[3,4], y=[3,4])
        GuiUtils.dataFromItem = MagicMock(return_value=data1)

        # Add a new tab
        item = QtGui.QStandardItem("test")
        self.widget.setData([item])

        # Create a new dataset and mock the datafromitemcall()
        data2 = Data1D(x=[1,2], y=[1,2])
        GuiUtils.dataFromItem = MagicMock(return_value=data2)

        # Swap the data
        self.widget.swapData(item)

        # Check that data has been swapped
        self.assertEqual(self.widget.tabs[0].data, data2)

        # We should only have one tab
        self.assertEqual(len(self.widget.tabs), 1)

        # send something stupid as data
        item = "foo"

        # It should raise an AttributeError
        self.assertRaises(AttributeError, self.widget.swapData, item)

        # Create a batch tab
        item = QtGui.QStandardItem("test")
        self.widget.addFit(None, is_batch=True)

        # It should raise an exception
        self.assertRaises(RuntimeError, self.widget.swapData, item)

        # Create a non valid tab
        self.widget.addConstraintTab()

        # It should raise a TypeError
        self.assertRaises(TypeError, self.widget.swapData, item)

    def testSetBatchData(self):
        ''' Assure that setting batch data is correct'''

        # Mock the datafromitem() call from FittingWidget
        data1 = Data1D(x=[1,2], y=[1,2])
        data2 = Data1D(x=[1,2], y=[1,2])
        data_batch = [data1, data2]
        GuiUtils.dataFromItem = MagicMock(return_value=data1)

        item = QtGui.QStandardItem("test")
        self.widget.setData([item, item], is_batch=True)

        # First tab should not accept data
        self.assertEqual(len(self.widget.tabs), 2)

        # Add another set of data
        self.widget.setData([item, item], is_batch=True)

        # Now we should have two batch tabs
        self.assertEqual(len(self.widget.tabs), 3)

        # Check the names of the new tabs
        self.assertEqual(self.widget.tabText(1), "BatchPage2")
        self.assertEqual(self.widget.tabText(2), "BatchPage3")

    def testSerialization(self):
        ''' Serialize fit pages and check data '''
        data = Data1D(x=[1,2], y=[1,2])
        GuiUtils.dataFromItem = MagicMock(return_value=data)
        item = QtGui.QStandardItem("test")
        self.widget.setData([item])
        tab = self.widget.tabs[0]
        cbCat = tab.cbCategory
        cbModel = tab.cbModel
        cbCat.setCurrentIndex(cbCat.findText("Cylinder"))
        cbModel.setCurrentIndex(cbModel.findText("barbell"))
        data_id = str(self.widget.currentTabDataId()[0])
        # check values - disabled control, present weights
        rowcount = tab._model_model.rowCount()
        self.assertEqual(rowcount, 8)
        state_default = self.widget.serializeAll()
        state_all = self.widget.serializeAllFitpage()
        state_cp = self.widget.serializeCurrentPage()
        page = self.widget.getSerializedFitpage(self.widget.currentTab)
        # Pull out params from state
        params = state_all[data_id]['fit_params'][0]
        # Tests
        self.assertEqual(len(state_all), len(state_default))
        self.assertEqual(len(state_cp), len(page))
        self.assertEqual(len(state_all), 1)
        # getPage should include an extra param 'data_id' removed by serialize
        self.assertNotEqual(len(params), len(page))
        self.assertEqual(len(params), 28)
        self.assertEqual(page.get('data_id', None), None)


if __name__ == "__main__":
    unittest.main()
