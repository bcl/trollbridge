#!/usr/bin/env python

# TrollBridge Network Portal
# Copyright 2004 by Brian C. Lane <bcl@brianlane.com>
# All Rights Reserved
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA
#
# ------------------------------------------------------------------------
#
# This CGI script is skeleton code for authentication of a unauthorized
# user who has been captured by the system. The Apache Redirect will have
# passed the original target hostname in the 'redirect' variable.
#
# This code does no actual authentication. It allows any username/password
# combination to be used. It demonstrates how to communicate with the 
# trolld to authorize the user to pass through the TrollBridge by talking
# to the trolld fifo.
# 
# ==========================[ HISTORY ]===================================
# 04/02/2004   Preparing for initial release. Added configuration file
# bcl          support.
# ------------------------------------------------------------------------

import os, sys, cgi, urllib, string, ConfigParser
import cgitb; cgitb.enable()
#import cgitb; cgitb.enable(display=0, logdir="/tmp")

config_locations = ['/etc/trollbridge','/usr/local/etc/trollbridge']

config = ConfigParser.ConfigParser()
config.add_section("trolld")
config.read( config_locations )
password  = config.get("trolld","password")
fifoname  = config.get("trolld","fifoname") 

def permit_client( ip ):
	permit = password+";permit %s public" % (ip)
	pipeout = open( fifoname, "w" )
        pipeout.write(permit)
	pipeout.close

# For diagnostics, show all the environmental variables
def show_environment():
	for key in os.environ.keys():
		print "os.environ['"+key+"'] = "+os.environ[key]+"<br>"

# For diagnostics, Show all values passed in the form
def show_form():
	for key in form.keys():
		print "form['"+key+"'] = "+form[key]+"<br>"


# Main code starts here. Redirect the output to the browser so we can use
# print.
sys.stderr = sys.stdout		# Errors to browser
form = cgi.FieldStorage()	# Parse form elements

# Get the user's IP address
ip = os.environ['REMOTE_ADDR']

# See if they are passing us login info, or needs to be shown the initial
# splash page
if not form.has_key('login'):
	print "Content-type: text/html\n"

	# Display the client info and login request
	print """
		<head>
		<title>TrollBridge Example Login Page</title>
		</head>
		<body bgcolor=brown>
		<center>
		<b>You have been captured by TrollBridge, please log in:</b><br>
	      """
        
	# Get the name for the ip they have chosen
	name = ip

	print "Your IP is %s, known locally as %s<p>" % (ip, name)

	# Print the login form
	login_form = """
		<form method="POST" action="/">
		<input type="hidden" name="redirect" value="%s">
		<table><tr><td>
		Username: </td><td><input type="text" name="username"><br>
		</td></tr><tr><td>
		Password: </td><td><input type="password" name="password"><br>
		</td></tr><tr><td colspan=2>
		<center><input type="submit" name="login" value="Login"></center>
		</td></tr></table>
		</form>
	      """

	# Or if I want to use an image:
	#<input type="image" name="mode_login" src="images/login.gif" width="55" height="17" border="0">

	print login_form % (form.getfirst("redirect"))


else:
	# Here is where authentication would take place

	# And if it is successful:
	# Add this client to the iptables
	permit_client( ip )

	# Redirect them to their original destination
	print "Status: 302 Moved"
	print "Location: http://"+form.getfirst("redirect")+"\n"

	# Otherwise tell them why the failed and to try again (remember to
	# reserve the redirect information)
