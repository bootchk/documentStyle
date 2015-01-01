
import documentStyle.config as config


class DialogFactory(object):
  '''
  Produce style dialog to let user edit StyleSheet (which may be style of DocumentElement)
  
  Understands there are two different implementations (dispatches on config.useQML)

  When implemented by inheriting from QWidget QDialog, open() and signals accepted and rejected are inherited.
  
  StyleDialog Abstract Base Class API: (but it is not formally declared. TODO declare it and inherit.)
  isEditable()
  open()
  converseAppModal()
  connectSignals()
  
  Two subclasses of StyleDialog: editable and noneditable.
  Editable one has accept/reject buttons.  Noneditable can only be closed.
  For now, not exist a QML implementation of Noneditable
  
  Note there is no Qt method to show a dialog as a popup: under the cursor, but modal.
  print("here")
  self.move(0,0)  TODO to cursor
  self.show()
  '''


  def produceNoneditableDialog(self, parentWindow, formation, titleParts):
    if config.useQML:
      raise NotImplementedError
    else:
      from documentStyle.ui.widgetUI.styleDialogWidget import NoneditableStyleSheetDialogWidget
      result = NoneditableStyleSheetDialogWidget(parentWindow, formation, titleParts)
    return result
  
  
  def produceEditableDialog(self, parentWindow, formation, titleParts):
    if config.useQML:
      from documentStyle.ui.qmlUI.styleDialogQML import StyleSheetDialogQML
      result = StyleSheetDialogQML(parentWindow, formation, titleParts)
    else:
      from documentStyle.ui.widgetUI.styleDialogWidget import EditableStyleSheetDialogWidget
      result = EditableStyleSheetDialogWidget(parentWindow, formation, titleParts)
    return result
  
  
dialogFactory = DialogFactory() # singleton
