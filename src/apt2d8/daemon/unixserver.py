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
import SocketServer

import clientserviceimpl
from ..common import config

logger = logging.getLogger(__name__)

class ClientStreamRequestHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		service = clientserviceimpl.ClientServiceImpl(self.rfile, self.wfile)
		service.run()

def start():
	socket = '%s/apt2d8d.socket' % config.SOCKET_PATH
	if os.path.exists(socket):
		os.remove(socket)
	
	server = SocketServer.UnixStreamServer(socket, ClientStreamRequestHandler)
	logger.info('Listening for clients on unix socket %s', socket)
	server.serve_forever()

