class curry:
     """
     Create a curry class used to supply additional arguments for
     registered callback events
     Based on an example from the pythonCookbook
     http://aspn.activestate.com/ASPN/Python/Cookbook/
     """
     
     def __init__(self, fun, *args, **kwargs):
          """
          Class constructor
          Args:
          *args = arguments
          **kwargs = keyword arguments
          """

          self.fun = fun
          self.pending = args[:]
          self.kwargs = kwargs.copy()

     def __call__(self, *args, **kwargs):
          """
          Class constructor
          Args:
          *args = arguments
          **kwargs = keyword arguments
          """
               
          if kwargs and self.kwargs:
               kw = self.kwargs.copy()
               kw.update(kwargs)
          else:
               kw = kwargs or self.kwargs

          return self.fun(*(self.pending + args), **kw)