
# Helper function to print out a html page of the information
# retrieved when executing dir(obj) on a object
def Help(object):
    """
    Function to generate an HTML debug page for an object
    Args:
      object = The object to inspect

    Returns: None
    """
    d = dir(object)
    fp = open("debug.html", "w")
    fp.write("<html><body>\n")
    for element in d:
        doc = "Not available"
        try:
            exec("doc = object.%s.__doc__" % element)
        except Exception:
            pass
            
        fp.write("<br><br><b>%s</b>\n" % element)
        fp.write("<br>\n")
        fp.write("<pre>%s</pre>\n" % doc)
        fp.write("<br>\n</body></html>")
    fp.close()