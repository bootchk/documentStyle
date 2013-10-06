'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtCore import QCoreApplication
from .intermediateStyleSheet import IntermediateStyleSheet



class DocumentElementStyleSheet(IntermediateStyleSheet):
  '''
  StyleSheet attached to a DocumentElement.
  
  Specializes StyleSheet:
  - leaf. No NamedStylingActSet since nothing can refer to it (Design might change.)
  - ALWAYS parented to docStyleSheet
  - name is generic (not a user-given name to instance)
  '''
  def __init__(self):
    IntermediateStyleSheet.__init__(self, name="DocElement")
    '''
    Always parented to docStyleSheet.
    assert app has docStyleSheet attribute, i.e. parent style sheet exists.
    Note that when unpickling a document, its docStyleSheet must be unpickled first.
    '''
    self.setParent(QCoreApplication.instance().cascadion.docStyleSheet)
    
    
  
        