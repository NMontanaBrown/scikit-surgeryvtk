import pytest
import PySide2

import sys
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton
from sksurgeryvtk.widgets.vtk_overlay_window import VTKOverlayWindow

from sksurgeryvtk.widgets.QVTKRenderWindowInteractor \
        import QVTKRenderWindowInteractor

def test_qapp():

    app = QApplication()
    dialog = QDialog()
    dialog.show()

# This should pass
def test_qvtkrenderwindowinteracto_dont_start():
    widget = QVTKRenderWindowInteractor()

# This should fail/crash
def test_qvtkrenderwindowinteractor():
    widget = QVTKRenderWindowInteractor()
    widget.Start()

def test_vtkoverlaywindow():
    widget = VTKOverlayWindow()


