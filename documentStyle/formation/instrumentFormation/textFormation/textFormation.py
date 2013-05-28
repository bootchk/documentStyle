'''
'''
from PySide.QtGui import QTextCursor
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
  '''
  
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
    Cursor with selection of entire document of morph.
    '''
    cursor = QTextCursor(morph.document())
    assert not morph.document().isEmpty()  #require: can't select empty document
    cursor.setPosition(0)
    cursor.clearSelection()
    # programmatic selection requires movePosition(), not setPosition()
    cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
    assert cursor.hasSelection()  #ensure
    return cursor
