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

  Responsibilities:
   - maintain (get, set) a style value
   - know a default style (value of a new instrument)
   
   A Formation applies an instrument to a document element.
   The instruments provided by the framework can be applied to a document element
   by passing the instrument to a method of a document element.
   A formation applies the instruments in this directory to a document element
   via adaption: the formation extracts instrument value and passes that to the document element.
   (Probably document elements should be changed to accept even the instruments not provided by the framework.)
   
   Abstract and not inherited: only documentation.
  '''
  pass

        