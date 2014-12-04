'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''


class Styler(object):
  '''
  Styles a DocumentElement or Tool (a Leaf of any cascade.)
  
  Responsibiliies:
  - get/set a Formation that can be applied to a DocumentElement or Tool.
  
  Subclasses:  Two designs for styling:
  - TemplateStyler: each DocumentElement has-a Formation, no cascading (but the Formation is created by AppStyleSheet)
  - DynamicStyler: each DocumentElement has-a StyleSheet (which returns a Formation) and StyleSheets cascade.

  Abstract.
  
  This has very similar API as a StyleSheet, but NOT is-a, has-a Stylesheet.
  The main difference is what happens after edit():
  - StyleSheet emits stylesheetChanged
  - Styler returns a Formation that a caller applies
  '''
  def formation(self):
    raise NotImplementedError("Deferred")
    
  def styleLeafFromFormation(self, editedFormation):
    ''' 
    Style leaf (DocumentElement or Tool) that owns this styler with the given editedFormation.
    (Template styling.)
    '''
    raise NotImplementedError("Deferred")
  
  def styleLeafFromStyleSheet(self, styleSheet):
    ''' 
    Style leaf (DocumentElement or Tool) that owns this styler with the given stylesheet.
    (Dynamic, cascaded styling.)
    '''
    raise NotImplementedError("Deferred")

  def addToStyleCascade(self):
    raise NotImplementedError("Deferred")

  def editStyleOfDocElement(self, parentWindow, titleParts, docElement):
    raise NotImplementedError("Deferred")