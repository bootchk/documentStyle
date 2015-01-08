'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''


from PyQt5.QtWidgets import QListView, QLabel, QVBoxLayout, QHBoxLayout

from formationListModel import FormationListModel

class FormationListview(QListView):
  '''
  Listview of style property widgets.
  List means: single column (but indented like a tree).
  View means: scrolling.
  
  Collaborates with Formation, which recurses.
  '''


  def __init__(self, formation):
    super(FormationListview, self).__init__()
    
    self.model()
    """
    if formation.isSingleValued():
      self._singleChildLayout(formation)
    else:
      self._multipleChildLayout(formation, top=True)
    """

  
  def addTo(self, layout):
    '''
    Add self to a layout.
    Only self knows whether self is widget or layout.
    '''
    layout.addWidget(self)
  
  
  def model(self):
    model = FormationListModel()
    # model.
    self.setModel(model)
  
  
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
      label = QLabel(formation.name)
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
    