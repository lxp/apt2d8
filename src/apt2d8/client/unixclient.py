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

import os
import socket

from ..common import config
from ..rpc import clientstub

class UnixClientStub(clientstub.ClientStub):
	def __init__(self, sfile='%s/apt2d8d.socket' % config.SOCKET_PATH):
		s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		s.connect(sfile)
		f = s.makefile()
		clientstub.ClientStub.__init__(self, f, f)

