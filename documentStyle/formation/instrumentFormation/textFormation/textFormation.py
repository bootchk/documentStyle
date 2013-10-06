'''
'''
from PyQt5.QtGui import QTextCursor
from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation

class TextFormation(InstrumentFormation):
  '''
  InstrumentFormation for a block and char styled text document
  
  Base class.  Partially deferred.
  
  Responsibilty:
  - know how to apply self to a document (common to subclasses.)
  
  In Qt, style can be set on the selection of a cursor of document.
  In Qt, iteration over the structure of a document is read-only,
  no styling can be done during iteration of blocks and fragments.
  Hence this Formation subclass differs from others in that it applies itself
  to a Cursor of a DocumentElement instead of a DocumentElement.
  
  !!! Note that if an app creates a new cursor, style must be applied to it also,
  otherwise text in the cursor will not be styled.
  '''
  from documentStyle.debugDecorator import report
  
  @report
  def applyTo(self, morph):
    '''
    Redefined for text: apply to a cursor on morph.
    '''
    if not morph.document().isEmpty():
      cursor = self._getCursorSelectAll(morph)
      self.applyToCursor(cursor)
    
    
  def applyToCursor(self, cursor):
    raise NotImplementedError # Deferred
  
  
  def _getCursorSelectAll(self, morph):
    '''
    Cursor on entire document (text) of a morph (DocumentElement) of type Text.
    
    morph may be empty of text.
    !!! Cursor may not hasSelection() if morph is empty of text.
    '''
    cursor = QTextCursor(morph.document())
    cursor.setPosition(0)
    cursor.clearSelection()
    # programmatic selection requires movePosition(), not setPosition()
    cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
    # In Qt, cursor is valid for further operations regardless of whether hasSelection()
    # ensure document not empty => cursor.hasSelection
    assert morph.document().isEmpty() or cursor.hasSelection()
    return cursor
