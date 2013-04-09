'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import QCoreApplication
from intermediateStyleSheet import IntermediateStyleSheet



class DocumentElementStyleSheet(IntermediateStyleSheet):
  '''
  StyleSheet attached to a DocumentElement.
  
  Specializes StyleSheet:
  - leaf. No NamedStylingActSet since nothing can refer to it (Design might change.)
  - ALWAYS parented to docStyleSheet
  - name is generic
  '''
  def __init__(self):
    # assert the application has docStyleSheet attribute
    IntermediateStyleSheet.__init__(self, parent=QCoreApplication.instance().docStyleSheet, name="DocElement")
    
    
  
        