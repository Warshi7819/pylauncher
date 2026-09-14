###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import os.path


class Aliases:
    """
    Class implementing alias methods
    """

    def __init__(self, filename):
        """
        Class constructor
        Args:
          filename [STRING] = The path to the aliases.txt file
        """
        
        self.filename = filename


    def loadAliases(self):
        """
        Method to load aliases from file
        Args:
          filename = The name of the alias file

        Returns: A list of aliases [name, execute, args]
        """
        data = []

        if not os.path.isfile(self.filename):
            # Alias file does not exist. Create default file
            fp = open(self.filename, "w")
            fp.write("# Here you can add aliases\n")
            fp.write("#  name:app name\n")
            fp.write("#  execute:path to app or web address\n")
            fp.write("#  args:arguments if any\n")
            fp.write("# Example:\n")
            fp.write("name:AL Homepage\n")
            fp.write("execute:http://www.garageinnovation.org/AL\n")
            fp.close()

        if os.path.isfile(self.filename):
            fp = open(self.filename, "r")
            tmp = fp.readlines()
            fp.close()
            name = None
            args = None
            execute = ""
            
            for line in tmp:
                line = line.strip("\n").strip()
                if line.startswith("#"):
                    continue
                else:
                    if line.startswith("name:"):
                        if name:
                            if execute:
                                data.append([name, execute, args])
                        name = line[line.find(":") + 1 : ]
                        args = ""
                        execute = ""
                            
                    elif line.startswith("execute:"):
                        execute = line[line.find(":") + 1 : ]
                            
                    elif line.startswith("args:"):
                        args = line[line.find(":") + 1 : ]
                    else:
                        continue

            if name:
                if execute:
                    data.append([name, execute, args])

        return data


    def saveAliases(self, aliases):
        """
        Method to save the aliases to file
        Args:
          aliases [LIST] = The new aliases that we
                           want to save

        Returns: None
        """

        fp = open(self.filename, "w")
        for alias in aliases:
            fp.write("name:%s\n" % alias[0])
            fp.write("execute:%s\n" % alias[1])
            if alias[2] != "":
                fp.write("args:%s\n" % alias[2])
            
        fp.close()
        

    def default(self):
        """
        Override value return from default. Aliases should be a part of
        the default setup
        Args:
          None

        Returns: True, we want aliases to be a part of the default setup
        """
        return True

# TEST CODE
if __name__ == "__main__":
    alias = Aliases()
    print(alias.loadAliases("aliases.txt"))