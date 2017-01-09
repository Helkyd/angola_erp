#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  asterisk.py
#
#  Copyright 2014 James Finstrom<jfinstrom at gmail>
#  Updated & Fixed Sep 2016 Jeff T - github jefft4
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
## note:  give the Manager user READ, WRITE on system and command (needed to run SIP commands) + read on whatever else it needs for other purposes.

import os
import sys
import socket
import ConfigParser

#Note: if you set up additional managers through FreePBX, change this to manager_additional.conf !
mgrcnf = '/etc/asterisk/manager.conf'
mgrusr = 'test'
extensao = ""

#config = ConfigParser.ConfigParser()
#config.read(mgrcnf)
username = mgrusr
password = '123456789' #config.get( mgrusr, 'amp111')
""" Initialize the dictionary in the global space """

def make_dict(lst):
        ret ={}
        for i in lst:
                i = i.strip()
                if i and i[0] is not "#" and i[-1] is not "=":
                        var,val = i.rsplit(":",1)
                        ret[var.strip()] = val.strip()
        return ret

class acli:
        def __init__(self):
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.serverip = '10.192.8.100'
                self.serverport = 5038
                self.username = 'admin'
                self.password = 'angola'

        def sendCmd(self,action,paraquem,**args):
		print action
		if action =="login":
			print "no login"
			self.sock.send("Action: %s\r\n" % action)
		else:
			if paraquem == "Quarto":
				self.sock.send("Action: Originate\r\n")
				self.sock.send("Channel: SIP/%s\r\n" % action)
				self.sock.send("Exten: 100\r\n")
				self.sock.send("Application: Playback\r\n")
				self.sock.send("Data: custom/TempoTerminou\r\n")
				self.sock.send("CallerID: 100\r\n")
			else:
				#recepcao
				self.sock.send("Action: Originate\r\n")
				self.sock.send("Channel: SIP/%s\r\n" % action)
				self.sock.send("Exten: 100\r\n")
				self.sock.send("Application: Playback\r\n")
				self.sock.send("Data: custom/QuartoTempoTerminou\r\n")
				self.sock.send("CallerID: 100\r\n")


                for key, value in args.items():
                        self.sock.send("%s: %s\r\n" % (key,value))
                self.sock.send("\r\n")
                data = []
                while '\r\n\r\n' not in ''.join(data)[-4:]:
                        buf = self.sock.recv(1)
                        data.append(buf)
                l = ''.join(data).split('\r\n')
                return l


        def conn(self):
                self.sock.connect((self.serverip, self.serverport))
                #need Events OFF with the login else event text pollutes our command response
                ret = self.sendCmd("login","Quarto", Username=self.username, Secret=self.password, Events="OFF")
                print "Connect response: ", ret
                if 'Response: Success' in ret:
                        print 'Connected.'
                        return True
                else:
                        print "Connect failed!"
                        callCavalry(value['Message'], 'api call')
                        return False


def callCavalry( mesg, doing ):
        #put your action here
        print 'Ouch!', mesg, doing
        return True

def main(paraquem,extensao):
        ast = acli()
        ast.username = username
        ast.password = password
	print "usuario ", username
        if ast.conn():
        	if paraquem == "Quarto":
			dev = ast.sendCmd(extensao,"Quarto")
		else:
			#Recepcao
			dev = ast.sendCmd(extensao,"Rececao")
		
                print "Command response1: ", dev
                value = make_dict(dev)
                if value['Response'] == 'Success':
                        #print "Status = #", value['Status'], "#"
                        #don't test only for "OK" here, some return longer strings with ping time etc
                        if 'OK' in value['Status']:
                                print 'OK: trunk is up.'
                                pass
                        else:
                                callCavalry(value['Status'], 'peer myvoiptrunkname')
                else:
                        callCavalry(value['Message'], 'api call')

        return 0

if __name__ == '__main__': 
	#main(sys.argv[2:2])
	main(sys.argv[1],sys.argv[2])
