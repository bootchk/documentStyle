'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''



class Instrument(object):
  '''
  An Instrument applies style attributes to DocumentElements.
  
  Also known as "Format"
  
  Stereotype: information holder.  It is simply a set of parameters.
  
  Most Instruments are provided by Qt framework, but not called Instruments e.g. QPen, QBrush.
  
  Instrument subclasses here are missing from Qt,
  and unlike Qt Instruments they cannot be set() on a Document Element
  (only their attribute is copied.)
  
  Abstract and not inherited: only documentation.
  '''
  pass

        