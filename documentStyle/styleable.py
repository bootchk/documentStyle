'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
try:
  import pickle as pickle
except ImportError:
  import pickle


from documentStyle.styler.dynamicStyler import DynamicStyler
from documentStyle.selector import DETypeSelector
                                                  
from documentStyle.debugDecorator import report



class Styleable(object):
  '''
  Behavior of DocumentElements.
  Mixin.
  
  Responsibilities:
  - create a styler
  - let user edit style using Dialog (for example on a context menu event for right mouse button.) 
  - polish: apply style
  
  
  No __init__: since mixin, let init pass up MRsheetO.
  However, must initialize with a call to setStylingDocumentElementType()
  
  ADT algebra, i.e. API
  
  1. Exceptional case
  editStyle()-> raises exception, must be preceded by setStylingDocumentElementType()
  
  2. Idempotent case (document element is Styleable, but not styled by user.)
  draw()-> succeeds, (where draw() is a framework method) an element can be drawn without any styling (framework supplies default look)
  
  3. Exceptional case
  polish()-> raises exception, must be preceded by setStylingDocumentElementType()
  
  4. Common case, user edits style of document element
  setStylingDocumentElementType()
  foo = editStyle(self)
  if foo is not None:
    applyStyle(foo)
  serializedStyle() -> returns emptySerializeableStyle (if user canceled) or foo, and visual style is equivalent to foo
  
  
  5.  Common case, user edits stylesheet
  setStylingDocumentElementType()
  'user change style sheet'
  polish() -> every document element matching style sheet change has visual style equivalent to stylesheet
  except for document elements which user has styled (inline)
  
  6.  Explanatory case
  setStylingDocumentElementType()
  getStyle()-> returns a style equivalent to the default of the framework (since document element not styled by user.)
  
  7.  Undo case
  setStylingDocumentElementType()
  bar = serializedStyle(): returns current style
  foo = editStyle(self)
  if foo is not None:
    applyStyle(foo)
  resetStyleFromSerialized(bar) -> visual style of document element restored to style prior to user edit of style

  
  8. Undo past stylesheet change case
  setStylingDocumentElementType()
  bar = serializedStyle(): returns current style
  foo = editStyle(self)
  if foo is not None:
    applyStyle(foo)
  'user change style sheet'
  resetStyleFromSerialized(bar) -> visual style of document element restored to style prior to user edit of style AND stylesheet
  
  9. Pickling case where other ancestors are not pickleable
  # Only pickle self.styler
  # Typically in __reduce__(self): return (callable, argsToCallable, {'styler', self.styler})
  serializedStyleable = cpickle.dumps(self.styler)
  self.styler = cpickle.loads(serializedStyleable)
  self.polishAfterDeserialization()  : visible style of element restored
  
  '''
  
  def setStylingDocumentElementType(self, DEType):
    '''
    Initialize with a styler.
    Styler depends on document element type.
    A DocumentElement has style (lower case, not Style) but no Style (to model, then from model to view.)r UNTIL user acts to style it.
    In other words, this can be done just before editStyle(), or earlier when DocumentElement is created.
    '''
    # Choose Dynamic or Template.  Defines the broad behaviour of app.  Need Factory?
    self.styler = DynamicStyler(DETypeSelector(DEType))
    #self.styler = TemplateStyler(self.selector)
    self.documentElementStyleType = DEType
  
  
  def getStylingDocumentElementType(self):
    result = self.documentElementStyleType
    assert isinstance(result,str) # See above: is a str to create a selector
    return result
  
  
  def _setStyle(self, styling=None):
    '''
    Set style of DocumentElement from a styling.
    
    The usual source of styling is editStyle().
    
    There is no getStyle() exported.  Only this module knows that 'style' is a Styler's Formation.
    Only serializableStyle is exported.
    
    Do not confuse with Qt.QBrush.setStyle().
    
    Hides implementation of Style (e.g. as a Formation derived by cascading.)
    !!! Styler (certain subclasses) may convert Formation into StylingActs on StyleSheet.
    !!! Does not apply style (i.e. send it to GraphicsFramework.
    '''
    self.styler.styleLeafFromFormation(formation=styling)
  
  
  @report
  def serializedStyle(self):
    '''
    Object attribute that is serializable e.g. via pickling.
    And suitable as parameter to setStyleFromSerializable.
    
    Since this is a mixin class, we explicitly expose serializiable part.
    A class that inherits Styleable might have attributes that are not pickleable.
    If your class that inherits Styleable IS pickleable, you don't need to call this,
    but then you do need to call a method to apply style after unpickling your class.
    (i.e. call self.styler.formation().applyTo(self) )
    
    Essentially, a StylingActSetCollection, but that fact is hidden.
    '''
    return pickle.dumps(self.styler, pickle.HIGHEST_PROTOCOL)

  
  @report
  def resetStyleFromSerialized(self, serializedStyle):
    '''
    Set style of DocumentElement from serialization by serializedStyle()
    
    serializedStyle is not changed.
    Current style is changed (a new DocumentStyleSheet is ultimately created.)
    '''
    self.styler = pickle.loads(serializedStyle)
    self.polishAfterDeserialization()
    
  
  def addToStyleCascade(self):
    '''
    Ensure self is a leaf in style cascade.
    
    Deserialized Styleables are not in style cascade.
    '''
    self.styler.addToStyleCascade()
    
    
  def polishAfterDeserialization(self):
    '''
    Polish an individual styleable after it is deserialized.
    E.G. called after an undo style change.
    Hides self.styler from callers.
    '''
    self.addToStyleCascade()
    self.polish()
    
  @report
  def applyStyle(self, styling):
    ' Apply given style to self.'
    '''
    From passed style to model.
    Essentially, create StylingActs on self's StyleSheet.
    '''
    self._setStyle(styling=styling)
    '''
    From model to view.
    Essentially, cascade StyleSheets and apply resulting Formation to Drawable.
    '''
    self.styler.formation().applyTo(self) 

    
  
  def editStyle(self, parentWindow):
    ''' 
    Let user edit style of DocumentElement.
    If not canceled, apply Style to DocumentElement
    
    Implementation: delegate to styler.
    Note styler may call back to self.applyStyle()
    '''
    '''
    assert getStylingDocumentElementType() is a string that describes document element type
    We say 'Element' to distinguish that this is a leaf(terminal) style sheet for a single element.
    Style type may be general, e.g. it may be 'Shape' whereas element is specifically a 'Rect' subclass of Shape.
    '''
    titleParts = (self.getStylingDocumentElementType(), "Element Style")
    self.styler.editStyleOfDocElement(parentWindow = parentWindow,
                                      titleParts=titleParts,
                                      docElement=self)
    

  @report
  def polish(self):
    '''
    Apply style to DocumentElement.
    
    E.G. called on StyleSheet changed. 
    Renews style Formation via cascading and applies. 
    '''
    #print 'Polish ', self.selector
    ## self.getStyle().applyTo(self)
    try:
      self.styler.formation().applyTo(self)
    except AttributeError:
      print('If no styler attribute, programming error: must call setStylingDocumentElementType()')
      raise


  