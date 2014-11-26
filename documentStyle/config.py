'''
Globals

Internationalization requires that certain objects be built earlier:
- translated strings
- certain objects with translated strings (models for instruments)
'''

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication


# global, singletons created during init of StyleSheetCascadion (when can assert translator is installed.)

i18ns = None  # Eventually of type Translations

BrushModel = None # Eventually of type AdaptedBrushModel
PenModel = None # Eventuall of type AdaptedPenModel
LineSpacingModel = None # Eventually of type AdaptedLineSpacingModel
AlignmentModel = None

useQML = False # Whether GUI is QML or QWidget.  Also see EditableStyleDialog
QMLView = None  # not used?

class Translations(QObject):
  '''
  Holds (contains) translated (i18n) strings (accessed like constants, by name.)
  '''
  
  def __init__(self):
    super(Translations, self).__init__()
    
    '''
    Translated strings.
    
    We do not use leading or trailing spaces or punctuation; those are untranslated and inserted programatically
    '''
    self.Any = self.tr("Any")
    
    # Document Element Types
    self.Line = self.tr("Line")
    self.Shape = self.tr("Shape")
    self.Text = self.tr("Text")
    self.Pixmap = self.tr("Pixmap")
    
    # Formation names
    self.Pen = self.tr("Pen")
    self.Brush = self.tr("Brush")
    self.Block = self.tr("Block")
    self.Character = self.tr("Character")
    self.Opacity = self.tr("Opacity")
    self.Pen = self.tr("Pen")
    self.Effect = self.tr("Effect") # graphic effect
   
    # Role names (when one instrument is used in two different roles on same DEType)
    self.Frame = self.tr("Frame")
    self.Ground = self.tr("Ground")
    
    # Property (model) names
    # Shared among formations
    self.Color = self.tr("Color")
    # Note Opacity is both name of formation and name of property
    # Pen
    self.Width = self.tr("Width")
    self.Style = self.tr("Style")
    # Line
    self.Pattern = self.tr("Pattern")
    # Character
    self.Font = self.tr("Font")
    # Block
    self.Aligned = self.tr("Aligned")
    self.Spacing = self.tr("Spacing")
    #self. = self.tr("")
    
    # Property domain values
    # Pen Style
    # NoneName is below
    self.Solid = self.tr("Solid")
    self.Dashed = self.tr("Dashed")
    self.Dotted = self.tr("Dotted")
    self.DashDot = self.tr("DashDot")
    # Brush Pattern
    self.NoneName = self.tr("None")
    self.Solid = self.tr("Solid")
    self.HalfDense = self.tr("Half dense")
    self.Quadrule = self.tr("Quadrule")
    self.Crosshatch = self.tr("Crosshatch")
    # Line spacing
    self.Single = self.tr("Single")
    self.OnePointFive = self.tr("1.5")
    self.Double = self.tr("Double")
    # Text alignment
    self.Left = self.tr("Left")
    self.Right = self.tr("Right")
    self.Center = self.tr("Center")
    self.Justify = self.tr("Justify")
    
    
    self.AppStyleSheet = self.tr("App Style Defaults")
    
    # Parts (suffixes) of dialog titles
    self.App = self.tr("App")
    self.User = self.tr("User")
    self.Doc = self.tr("Doc")
    self.ToolStyle = self.tr("Tool Style")
    self.ElementStyle = self.tr("Element Style")
    self.StyleSheet = self.tr("Style Sheet")
    
    
  def styleTranslate(self, untranslated):
    '''
    Dynamically translate a string in a variable
    (part of an assemblage)
    but which should be in the 'Translations' context (usually under 'Parts')
    '''
    return QApplication.instance().translate('Translations', untranslated)