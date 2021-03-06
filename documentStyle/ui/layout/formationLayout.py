'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout


class FormationLayout(QVBoxLayout):
  '''
  Collaborates with Formation, which recurses.
  '''


  def __init__(self, formation, top):
    super(FormationLayout, self).__init__()
    
    if formation.isSingleValued():
      self._singleChildLayout(formation)
    else:
      self._multipleChildLayout(formation, top)
      
      
  def _multipleChildLayout(self, formation, top):
    '''
    A tree-like, indented layout/widget.
    
    
    name
    ------
      | (recursion)
      |
     '''
  
    if not top:
      # display formation name in the layout
      label = QLabel(formation.role + formation.name)
      self.addWidget(label)
    # else display name in window title
      
    
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
    