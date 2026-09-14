###################################################
# Application : AL                                #
#  * Program to quickly launch other programs     #
#                                                 #
# Author      : Rune Devik                        #
# Date        : 16:55 04.30.2006                  #
# License     : GNU General Public License (GPL)  #
###################################################

# Import standard modules
import time

# Import 3rdparty modules
from ctypes import * # 3rdparty in python 2.3


class LastInputInfoStruct(Structure):
	"""
	Class that defines the LastInputInfo struct
	"""
	_fields_ = [("cbSize", c_uint), ("dwTime", c_uint)]


class DetectIdleTime:
	"""
	Class that implements methods to detect how long the
	Windows system has been idle. Idle means how long it has been since
	Windows has received either keyboard or mouse input
	"""

	def __init__(self):
		"""
		Class constructor. Initializes the windows stuff we need to
		figure out the stuff
		Args:
		  None
		"""
		
		self.getTickCount = windll.kernel32.GetTickCount
		self.getLastInputInfo = windll.user32.GetLastInputInfo
		self.lastInputInfo = LastInputInfoStruct()
		self.lastInputInfo.cbSize = sizeof(self.lastInputInfo)
		
	
	def getIdleTime(self):
		"""
		Method that fetches the current number of seconds since last user input.
		(Mouse or keyboard)
		Args:
		  None
		  
		Returns: [FLOAT] - the number of secs since last user input
		"""

		self.getLastInputInfo(byref(self.lastInputInfo))
		idleDelta = float(self.getTickCount() - self.lastInputInfo.dwTime) / 1000
		return idleDelta
		
		
if __name__ == "__main__":
	import time
	idleTime = DetectIdleTime()
	for i in range(0,10):
		print(idleTime.getIdleTime())
		time.sleep(1)