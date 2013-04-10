'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from documentStyle.selector import Selector


class StylingAct(object):
  '''
  An elemental change by user to a Formation.
  A record of change (a delta or diff.)
  Can be executed by StyleSheet on a (applyTo) Formation.
  
  TODO Subclasses: NamingStylingAct InlineStylingAct
  '''


  def __init__(self, selector, value):
    '''
    '''
    #print "new StylingAct", selector, value
    assert isinstance(selector, Selector)
    self._selector = selector
    self.value = value


  def selector(self):
    return self._selector
  

  def applyToFormation(self, formation):
    '''
    Copy self.value to formation's StyleProperty selected by my selector.
    
    This StylingAct need not be different than (changing) the Formation's value.
    In other words, superfluous.
    This might happen in these cases:
    - StylingAct deserialized from a handwritten stylesheet
    - Formation ancestors changed underneath StylingAct
    TODO rethink this.
    '''
    styleProperty = formation.selectStyleProperty(self._selector)
    if styleProperty is not None:
      #print "Overriding ", styleProperty, "with args", self.value
      # TODO, if not a change, won't set the inherit button
      styleProperty.set(self.value)
    else:
      # print "StylingAct not match ???"
      ''' It is NOT an assertion that self matches formation. '''
      pass

    
    
    
    