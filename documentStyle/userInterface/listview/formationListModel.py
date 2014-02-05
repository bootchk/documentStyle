'''
Created on May 10, 2013

@author: bootch
'''

from PyQt5.QtCore import QAbstractListModel, Qt

class FormationListModel(QAbstractListModel):
  '''
  Model a Formation as an indented list of labels and editing widgets (of style properties.)
  '''
  
  def rowCount(self, parent):
    '''
    Implement virtual.
    '''
    return 1
  
  def data(self, index, role ):
    if role == Qt.DisplayRole:
      if index.row() == 0:
        return 'foo'
      else:
        print('Index', index)
    else:
      print('Role', role)
      
    #setIndexWidget ( const QModelIndex & index, QWidget * widget )