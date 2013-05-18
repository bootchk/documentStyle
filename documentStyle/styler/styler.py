'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''


class Styler(object):
  '''
  Styles a DocumentElement.
  
  Responsibiliies:
  - get/set a Formation that can be applied to a DocumentElement
  
  Subclasses:  Two designs for styling:
  - TemplateStyler: each DocumentElement has-a Formation, no cascading (but the Formation is created by AppStyleSheet)
  - DynamicStyler: each DocumentElement has-a StyleSheet (which returns a Formation) and StyleSheets cascade.

  Abstract.
  '''
  def formation(self):
    raise NotImplementedError, "Deferred"
    
  def setFormation(self, newFormation):
    raise NotImplementedError, "Deferred"

  def resetAfterDeserialization(self):
    raise NotImplementedError, "Deferred"

