'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from documentStyle.selector import Selector

from documentStyle.debugDecorator import report

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
    self.selector = selector
    self.value = value


  def __repr__(self):
    return "StylingAct(" + str(self.selector) + "," + str(self.value) + ")"
  
  
  #@report
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
    #print "Applying styling Act", self
    styleProperty = formation.selectStyleProperty(self.selector)
    if styleProperty is not None:
      self._overrideStyleProperty(styleProperty)
    else:
      # print "StylingAct not match ???"
      ''' It is NOT an assertion that self matches formation. '''
      pass

  #@report
  def _overrideStyleProperty(self, styleProperty):
    '''
    StyleProperty has value from upstream (defaulted or already overridden.)
    Ensure it has my value (which is not necessarily different value.)
    
    If my value is not a different value, then self is non-effective now,
    but self may become effective later if the cascade changes.
    That is, self (StylingAct) exists even if non-effective at times.
    (The "Inherit" button will not be enabled when self is non-effective,
    so user cannot delete self StylingAct when it is non-effective.)
    Is that a user interface problem?
    '''
    # print "Overriding ", styleProperty, "with args", self.value
    if styleProperty.get() != self.value:
      styleProperty.set(self.value)
    
    
    