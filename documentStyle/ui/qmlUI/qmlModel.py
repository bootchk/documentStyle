
from PyQt5.QtQml import qmlRegisterType
# qmlRegisterSingletonType #, QQmlComponent, QQmlEngine


from documentStyle.ui.qmlUI.qmlDelegate import QmlDelegate


class QmlModel(object):
  '''
  App's model (of MVC pattern.)
  '''
  
  def __init__(self):
    pass
  
  def register(self):
    # uri = "org.qtproject.demo.weather"
    '''
    Register Python types.
    - URI is 'People' (i.e. library or module e.g. 'import People 1.0' in QML
    - it's v1.0 
    - type will be called 'Person' in QML.
    '''
    # C++ qmlRegisterSingletonType(uri, 1, 0, "ApplicationInfo", systeminfo_provider)
    # Python signature: qmlRegisterSingletonType(type, str, int, int, str, callable)
    #qmlRegisterSingletonType("ApplicationInfo", 1, 0, "ApplicationInfo")
    '''
    Unlike c++, where you cast result to a type, in Python first arg is type
    '''
    qmlRegisterType(QmlDelegate, 'QmlDelegate', 1, 0, 'DialogDelegate')
    
    '''
    BaseResettableValue is a type which QML interacts with, but need not know (be registered.)
    In this design, a Formation is set in the QML context,
    and QML calls model (Formation.selectResettableValueByStringSelector('Any.Line.Pen.Color') 
    to get an instance of this type, used as a model for individual style property controls.
    '''
    #qmlRegisterType(BaseResettableValue, 'ResettableValue', 1, 0, 'ResettableValue')
    
    