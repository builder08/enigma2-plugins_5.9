# -*- coding: utf-8 -*-
'''
general functions for FritzCall plugin

$Id: __init__.py 1260 2016-02-20 17:50:18Z michael $
$Author: michael $
$Revision: 1260 $
$Date: 2016-02-20 18:50:18 +0100 (Sat, 20 Feb 2016) $
'''

from Components.config import config #@UnresolvedImport
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE #@UnresolvedImport
import gettext, os
from enigma import eBackgroundFileEraser

lang = language.getLanguage()
os.environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("FritzCall", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/FritzCall/locale/"))

def _(txt): # pylint: disable=C0103
	td = gettext.dgettext("FritzCall", txt)
	if td == txt:
		td = gettext.gettext(txt)
	return td

# scramble text
def __(text, front=True):
	#===========================================================================
	# if len(text) > 5:
	#	if front:
	#		return '.....' + text[5:]
	#	else:
	#		return text[:-5] + '.....'
	# else:
	#	return '.....' 
	#===========================================================================
	out =""
	for i in range(len(text)/2):
		out = out + text[i*2] + '.'
	return out

import logging
from logging import debug
def initDebug():
#	try:
#		# os.remove("/tmp/FritzDebug.log")
#		eBackgroundFileEraser.getInstance().erase("/tmp/FritzDebugOld.log")
#	except OSError:
#		pass
	logging.basicConfig(filename='/tmp/FritzDebug.log',
					filemode='w',
					level=logging.DEBUG,
					# format='%(asctime)s %(levelname)s %(module)s %(name)s %(funcName)s %(message)s',
					format='%(asctime)s %(levelname)-8s %(name)-26s %(funcName)s %(message)-15s',
					datefmt='%Y-%m-%d %H:%M:%S')


#from time import localtime
#def debug(message):
#	if config.plugins.FritzCall.debug.value:
#		try:
#			# ltim = localtime()
#			# headerstr = u"%04d%02d%02d %02d:%02d " %(ltim[0],ltim[1],ltim[2],ltim[3],ltim[4])
#			deb = open("/tmp/FritzDebugOld.log", "aw")
#			# deb.write(headerstr + message.decode('utf-8') + u"\n")
#			deb.write(message + "\n")
#			deb.close()
#		except Exception, e:
#			debug("%s (retried debug: %s)" % (repr(message), str(e)))
#		logging.debug(message)

import re
def normalizePhoneNumber(intNo):
	
	found = re.match('^\+' + config.plugins.FritzCall.country.value.replace('00','') + '(.*)', intNo)
	if found:
		intNo = '0' + found.group(1)
	found = re.match('^\+(.*)', intNo)
	if found:
		intNo = '00' + found.group(1)
	intNo = intNo.replace('(', '').replace(')', '').replace(' ', '').replace('/', '').replace('-', '')
	found = re.match('^49(.*)', intNo) # this is most probably an error
	if found:
		intNo = '0' + found.group(1)
	found = re.match('.*?([0-9]+)', intNo)
	if found:
		return found.group(1)
	else:
		return '0'
