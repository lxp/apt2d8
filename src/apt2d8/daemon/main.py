#
# This file is part of apt2d8.
#
# Copyright (C) 2013  David Gnedt
#
# apt2d8 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# apt2d8 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with apt2d8.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import os
import signal
import sys

import hostmanager
import sourcewatcher
import unixserver
from ..common import config
from ..common import version

silent_exit = False
logger = logging.getLogger(__name__)

def main():
	global silent_exit
	
	# Register cleanup function
	signal.signal(signal.SIGTERM, cleanup)
	
	# Setup logging
	setupLogging()
	
	try:
		# TODO: Add version
		logger.info('apt2d8d %s Startup', version.version_str)
		
		checkPrivileges()
		
		# Load ssh keys
		hostmanager.manager.loadKeys()
		
		dropPrivileges()
		
		# Read config file
		hostmanager.manager.loadConfig()
		
		daemonize()
		
		# Initial host update
		hostmanager.manager.updateHosts()
		
		# Start sourcewatcher
		sourcewatcher.manager.start()
		
		# Listen for clients on UNIX socket
		unixserver.start()
	except Exception, e:
		logger.exception(e)
		raise
	finally:
		if not silent_exit:
			logger.error('Unexpectedly reached end of code. Exiting.')
	
	return 0

def cleanup(signum, frame):
	global silent_exit
	
	if signum == signal.SIGTERM:
		logging.getLogger().setLevel(logging.NOTSET)
		logger.info('Signal SIGTERM received. Exiting.')
	
	# Remove pid file
	pidfile = '%s/apt2d8d.pid' % config.PID_PATH
	if os.path.exists(pidfile):
		os.remove(pidfile)
	
	else:
		logger.error('Unexpected signal received. Exiting.')
	
	silent_exit = True
	sys.exit(0)

def setupLogging():
	root_logger = logging.getLogger()
	root_logger.setLevel(logging.NOTSET)
	
	formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
	
	handler = logging.StreamHandler(sys.stderr)
	handler.setFormatter(formatter)
	root_logger.addHandler(handler)
	
	logfile = '%s/apt2d8d.log' % config.LOG_PATH
	try:
		#handler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight', 1, keep_days))
		handler = logging.FileHandler(logfile)
		handler.setFormatter(formatter)
		root_logger.addHandler(handler)
	except IOError:
		logger.error('Error while opening logfile %s. Exiting.', logfile)
		silent_exit = True
		sys.exit(1)

def checkPrivileges():
	global silent_exit
	
	if os.geteuid() == 0:
		logger.error('You should not run apt2d8d with root privileges. Exiting.')
		silent_exit = True
		sys.exit(1)
	
	# TODO: Check USER_CONFIG_PATH/ssh rights
	# TODO: Check USER_CONFIG_PATH not writeable
	# TODO: Check LOG_PATH, PID_PATH, SOCKET_PATH, SYSTEM_CONFIG_PATH writeable

def dropPrivileges():
	pass

def daemonize():
	global silent_exit
	
	logger.info('Forking into background...')
	
	# Fork daemon process
	pid = os.fork()
	if pid > 0:
		silent_exit = True
		sys.exit(0)
	
	# Setup environment
	os.chdir('/')
	os.umask(022)
	os.setsid()
	
	# Second fork
	pid = os.fork()
	if pid > 0:
		silent_exit = True
		sys.exit(0)
	
	# Write pid file
	pidfile = '%s/apt2d8d.pid' % config.PID_PATH
	try:
		with open(pidfile, 'w') as f:
			f.write('%d\n' % os.getpid())
	except IOError:
		logger.error('Error while writing pid file %s. Exiting.', pidfile)
		silent_exit = True
		sys.exit(1)
	
	# Setup standard input, output, error
	null_read = open('/dev/null', 'r')
	null_write = open('/dev/null', 'w')
	os.dup2(null_read.fileno(), sys.stdin.fileno())
	os.dup2(null_write.fileno(), sys.stdout.fileno())
	os.dup2(null_write.fileno(), sys.stderr.fileno())

if __name__ == '__main__':
	main()

