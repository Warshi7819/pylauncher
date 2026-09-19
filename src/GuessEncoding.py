###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author(s)   : Michael Foord / Rune Devik        #
# Date        : 16:55 04.30.2006                  #
# License     : Free (I think :) )                #
###################################################

# Import standard modules
import locale

class GuessEncoding:
    """
    Class implementing methods that guesses the best encoding for a given
    string and converts it to unicode. The implementation is based on the code
    from an article in pyzine:
      http://www.pyzine.com/Issue008/Section_Articles/article_Encodings.html
    """

    def __init__(self):
        """
        Class constructor
        Args:
          None
        """
        
        # We *must* first call 
        locale.setlocale(locale.LC_ALL, '')


    def convertToUnicode(self, data):
        """
        Method to encode a given byte string into utf-8
        using the guessEncoding method.
        Args:
          data [STRING] = The byte string we want to encode

        Returns: [STRING] The string utf-8 encoded
        """

        # Guess encoding and try to convert it
        result = self.guessEncoding(data)
        return result[0]


    def guessEncoding(self, data):
        """
        Given a byte string, attempt to decode it.
        Tries the standard 'UTF8' and 'latin-1' encodings,
        Plus several gathered from locale information.
        Args:
          data [STRING] = The string we want to decode

        Returns: [TUPLE] (decoded_unicode, successful_encoding) or if
                          we fail we raise a UnicodeError
        """

        if type(data) == type(u""):
            return [data, "unknown but unicode"]

        successfulEencoding = None

        # we make 'utf-8' the first encoding
        encodings = ['utf-8']

        # next we add anything we can learn from the locale
        try:
            encodings.append(locale.nl_langinfo(locale.CODESET))
        except AttributeError:
            pass
        try:
            encodings.append(locale.getlocale()[1])
        except (AttributeError, IndexError):
            pass
        try:
            encodings.append(locale.getdefaultlocale()[1])
        except (AttributeError, IndexError):
            pass
        
        # we try 'latin-1' last
        encodings.append('latin-1')

        for enc in encodings:
            # some of the locale calls 
            # may have returned None
            if not enc:
                continue
            try:
                decoded = str(data, enc)
                successfulEncoding = enc

            except (UnicodeError, LookupError):
                pass
            else:
                break
            
        if not successfulEncoding:
            raise UnicodeError(
                'Unable to decode input data.  Tried the following encodings: %s.'
                % ', '.join([repr(enc) for enc in encodings if enc]))
        else:
            return [decoded, successfulEncoding]



