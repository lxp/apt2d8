#!/usr/bin/python
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

import apt
import os
import sys

def main(argv):
	if len(argv) > 1:
		os.environ['DEBIAN_FRONTEND'] = 'teletype'
		if argv[1] == 'update':
			update()
		elif argv[1] == 'upgrade':
			allowed = {}
			for i in argv[2:]:
				pkg, version = i.split('=')
				allowed[pkg] = version
			
			upgrade(allowed)
		else:
			raise SystemExit(2)
	else:
		raise SystemExit(2)

def update():
	cache = apt.Cache()
	cache.update()

def upgrade(allowed):
	cache = apt.Cache()
	with cache.actiongroup():
		cache.upgrade(dist_upgrade=True)
		for c in cache.get_changes():
			if c.candidate is not None:
				if c.name not in allowed or allowed[c.name] != c.candidate.version:
					print('Skipping %s %s' % (c.name, c.candidate.version))
					c.mark_keep()
		
		resolver = apt.cache.ProblemResolver(cache)
		resolver.resolve_by_keep()
		
		print('Installing the following packages:')
		for c in cache.get_changes():
			print('  %s %s' % (c.name, c.candidate.version))
	
	cache.commit(apt.progress.TextFetchProgress(), apt.progress.InstallProgress())

if __name__ == '__main__':
	main(sys.argv)

