'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from styleSheet import StyleSheet
from documentStyle.selector import newAllSelector

from documentStyle.formation.formation import Formation

from documentStyle.formation.instrumentFormation.penFormation import PenFormation
from documentStyle.formation.instrumentFormation.brushFormation import BrushFormation
from documentStyle.formation.instrumentFormation.opacityFormation import OpacityFormation
from documentStyle.formation.instrumentFormation.graphicEffectFormation import GraphicEffectFormation

from documentStyle.formation.morphFormation import ShapeFormation, LineFormation, TextFormation, PixmapFormation

from documentStyle.userInterface.styleDialog.styleDialog import NoneditableStyleSheetDialog


class AppStyleSheet(StyleSheet):
  '''
  Specializes StyleSheet:
  - root stylesheet. Parent is None.  Terminal for cascading.
  - has no StylingActSet (edit is view only, not changeable.)
  
  Singleton
  '''
  
  def __init__(self):
    '''
    appStyleSheet is a singleton, but its formation is not.
    Alternative for performance: keep a readonly copy of appStyleSheetFormation.
    Since user will rarely look at the appStyleSheet, not important.
    # self.appReadOnlyFormation = 
    '''
    super(AppStyleSheet, self).__init__(name="App")
    
    
  def _allSharedInstrumentFormationClasses(self):
    '''
    List of all classes of InstrumentFormation that are shared between morph formations.
    
    Note missing since not shared :
    - CharFormation only of Text morph.
    - GraphicEffectFormation only of Pixmap morph.
    '''
    return [PenFormation, BrushFormation, OpacityFormation ]
    
    
  def _allDocumentElementTypeFormationClasses(self):
    '''
    List of all classes of MorphFormation (for each document element type.)
    '''
    return [LineFormation, ShapeFormation, TextFormation, PixmapFormation]
    
    
  def _newAppStyleSheetFormation(self):
    '''
    Return a new formation that covers all DocumentElement types.
    
    This also defines what can appear in an editing dialog.
    (Although an editing dialog can prune this.)
    
    Configures what Formations the app supports.
    An app need not support all the Formations the framework does.
    EG an app need not support opacity even though the framework does.
    
    Default values of Formations defined by the Framework.
    The app does not necessarily need to define defaults if the framework does.
    If the framework defaults change with new versions, the app defaults will also.
    
    Must create a new formation, since caller may edit it.
    '''
    formation = Formation( name="Application Style Sheet", selector = newAllSelector() )
    
    '''
    Configure instrumentFormations.  
    Less selective.  If user edits, affects many DEType formations.
    Optional: if not defined, the app does not allow user to edit.
    E.G. if opacity is not here, user can not edit opacity of whole document in one place.
    '''
    for instrumentFormationClass in self._allSharedInstrumentFormationClasses():
      formation.append(instrumentFormationClass(parentSelector=newAllSelector()))
    
    '''
    Configure DEType formations.
    Not optional: each DocumentElement type that the app can draw must be represented here.
    '''
    for shapeFormationClass in self._allDocumentElementTypeFormationClasses():
      formation.append(shapeFormationClass())
    
    return formation
  
    
  def getFormation(self, selector):
    '''
    Redefine.
    Selector selects one, or all, of default DocumentElementFormat (MorphFormation).
    '''
    assert self.parent is None  # invariant: AppStyleSheet is root
    assert selector.DEType in ("Shape", "Line", "Text", "Pixmap", "*"), "Unknown document element type" + selector.DEType
    appFormation = self._newAppStyleSheetFormation()
    result = appFormation.selectSubformation(selector)
    assert result is not None
    return result
    
    
  def edit(self):
    '''
    Display read-only a form comprising section ror each DocumentElementType.
    TODO also display InstrumentFormations??
    
    This may not seem useful, but user needs to know what styling is default,
    so can understand inheritance via cascading.
    '''
    dialog = NoneditableStyleSheetDialog(formation=self._newAppStyleSheetFormation(), title="App Style Defaults")
    dialog.exec_()
    
  
        