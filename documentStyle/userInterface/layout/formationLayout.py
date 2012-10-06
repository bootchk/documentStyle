'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtGui import QLabel, QVBoxLayout, QHBoxLayout


class FormationLayout(QVBoxLayout):
  '''
  Collaborates with Formation, which recurses.
  '''


  def __init__(self, formation):
    super(FormationLayout, self).__init__()
    
    if formation.isSingleValued():
      self._singleChildLayout(formation)
    else:
      self._multipleChildLayout(formation)
      
      
  def _multipleChildLayout(self, formation):
    '''
    A tree-like, indented layout/widget.
    
    
    name
    ------
      | (recursion)
      |
     '''
  
    label = QLabel(formation.name)
    self.addWidget(label)
    
    indentedLayout = QHBoxLayout()
    indentedLayout.addSpacing(20) # Apparently pixels
    
    # Create lower right quadrant via recursion
    vLayout = QVBoxLayout()
    formation.displayContentsInLayout(vLayout)
    
    indentedLayout.addLayout(vLayout)
    
    self.addLayout(indentedLayout)
    
    
  def _singleChildLayout(self, formation):
    '''
    Single row layout.
    
    name Label  |  value
     '''
    formation.displayContentsInLayout(self)  
    