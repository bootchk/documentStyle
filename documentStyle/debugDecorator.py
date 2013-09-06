'''
A decorator to print indented program traces to console.

Author: Paul Butler
'''

# Number of times to indent output
# A list is used to force access by reference
__indentCount = [0]


'''
[a.__repr__() for a in params] is all params, including self
[a.__repr__() for a in params[1:]] excludes self
'''

DOC_STYLE_DEBUG = False     # <<<<<<<<<<<<<<<<<<<<<<<<<<<< 


if DOC_STYLE_DEBUG:


  def report(fn):
      '''
      Decorator to print information about a function call for use while debugging.
      Prints function name, arguments, and call number when the function is called. 
      Prints this information again along with return value when function returns.
      '''
  
      def wrap(*params,**kwargs):
          call = wrap.callcount = wrap.callcount + 1
  
          indent = '  ' * __indentCount[0]
          fc = "%s(%s)" % (fn.__name__, ', '.join(
              [a.__repr__() for a in params[1:]] +
              ["%s = %s" % (a, repr(b)) for a,b in kwargs.items()]
          ))
  
          print "%s%s called [#%s]" % (indent, fc, call)
          __indentCount[0] += 1
          ret = fn(*params,**kwargs)
          __indentCount[0] -= 1
          print "%s%s returned %s [#%s]" % (indent, fc, repr(ret), call)
  
          return ret
      wrap.callcount = 0
      return wrap

  
  
  def reportReturn(fn):
      '''
      Prints only the return
      '''
  
      def wrap(*params,**kwargs):
          call = wrap.callcount = wrap.callcount + 1
  
          indent = '  ' * __indentCount[0]
          fname = "%s" % fn.__name__
          args = "(%s)" % ', '.join(
              [a.__repr__() for a in params] +
              ["%s = %s" % (a, repr(b)) for a,b in kwargs.items()]
          )
          ret = fn(*params,**kwargs)
          print "%s %s call returns %s [#%s] for args %s " % (indent, fname, repr(ret), call, args)
  
          return ret
      wrap.callcount = 0
      return wrap
      
      
else:
  
  # Null decorators
  
  def report(fn):
    return fn
  
  def reportReturn(fn):
    return fn
  