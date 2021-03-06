#!/usr/bin/python
import re
from math import *

better_names = [
	('ANSI_', ''),
	('([a-z]{1})([A-Z0-9]{1})', '\\1 \\2'), #Expand CamelCase
	('^Delete$', 'Backspace'),
	('^Forward Delete$', 'Delete')
]
	


f = open('/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/Headers/Events.h')
buf = {}
for l in f:
	#print l
	m = re.match("\s*kVK_(\w+)\s+= 0x([A-Fa-f0-9]+),?", l)
	if m:
		keycode = int(m.group(2),16)
		string  = m.group(1)
		for k, v in better_names:
			string = re.sub(k,v,string)
		
		buf[keycode] = string
		#buf += "\t0x%07x:\t'%s',\n" % (keycode,string)
		#print string
		#print string
		#print keycode
	#"  kVK_ANSI_A                    = 0x00,"
f.close()
if(buf):
	length = ceil(log(max(buf.iterkeys()),16))
	format = "\t0x%0"+str(length)+"x:\t'%s',\n"
	f = open('constants.py', 'w')
	f.write(
"""### This file has been automatically generated by gen_constants.py
keycode_to_string = {
"""
	)
	for key in sorted(buf.iterkeys()):
		f.write(format % (key,buf[key]))
	f.write('}');
	f.close()
