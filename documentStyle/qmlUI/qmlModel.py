
from PyQt5.QtQml import qmlRegisterType
# qmlRegisterSingletonType #, QQmlComponent, QQmlEngine


from documentStyle.qmlUI.qmlDelegate import QmlDelegate
from documentStyle.qmlUI.person import Person
from documentStyle.styleProperty.resettableValue import BaseResettableValue


class QmlModel(object):
  '''
  App's model (of MVC pattern.)
  '''
  
  def __init__(self):
    pass
  
  def register(self):
    uri = "org.qtproject.demo.weather"
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
    
    # temp: model for business, i.e. a style property
    qmlRegisterType(Person, 'People', 1, 0, 'Person')
    
    '''
    Register a type which QML must know, but which we don't set in context.
    In this design, QML calls model (Formation.selectResettableValueByStringSelector('Any.Line.Pen.Color')
    to return an instance of this type.
    '''
    qmlRegisterType(BaseResettableValue, 'ResettableValue', 1, 0, 'ResettableValue')