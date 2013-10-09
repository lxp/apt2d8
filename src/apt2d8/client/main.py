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
import sys

import unixclient
from ..common import version

class AbortException(Exception):
	pass

def main(argv):
	if len(argv) == 2:
		if argv[1] == 'update':
			# TODO: Implement
			pass
		elif argv[1] == 'upgrade':
			upgrade()
		else:
			usage(argv)
	else:
		usage(argv)

def upgrade():
	try:
		client = unixclient.UnixClientStub()
		changes = loadChanges(client)
		
		print('')
		
		hosts = selectHosts(changes)
		
		for h in hosts:
			schanges = sortChanges(h.changes)
			
			print('')
			print('Host %s' % h.host.id)
			printChanges(schanges)
			
			while True:
				res = raw_input('Do you want to continue? [Y/n/?] ')
				if res == '' or res == 'y' or res == 'Y':
					break
				elif res == 'n' or res == 'N':
					raise AbortException()
				else:
					print('Commands:')
					print('  y: continue with the installation')
					print('  n: abort and quit')
					# TODO: Implement more features
					#print('  i: show information about one or more packages; the package names should follow the \'i\'')
					#print('  c: show the Debian changelogs of one or more packages; the package names should follow the \'c\'')
					#print('  d: toggle the display of dependency information')
					#print('  s: toggle the display of changes in package sizes')
					#print('  v: toggle the display of version numbers')
			
			client.writeUpgradeRequest([h])
			while True:
				response = client.readUpgradeResponse()
				if response.status == response.FINISHED:
					break
				elif response.status == response.CONSOLE:
					if response.stdout is not None:
						os.write(sys.stdout.fileno(), response.stdout)
					if response.stderr is not None:
						os.write(sys.stderr.fileno(), response.stderr)
			
			print('Upgrade of host %s finished.' % h.host.id)
	except AbortException, e:
		if e.message:
			print(e.message)
		
		print('Abort.')
	finally:
		client.quit()

def loadChanges(client):
	sys.stdout.write('Loading hosts... ')
	sys.stdout.flush()
	hosts = client.getHosts()
	print('Done')
	
	sys.stdout.write('Loading changes... ')
	sys.stdout.flush()
	changes = client.getChanges([h.host.id for h in hosts.hosts])
	print('Done')
	
	return changes

def selectHosts(changes):
	available_hosts = [h for h in changes.hosts if len(h.changes) > 0]
	unknown_hosts = [h for h in changes.hosts if h.last_update == 0]
	
	if len(unknown_hosts) > 0:
		print('The following hosts are unreachable:')
		for h in unknown_hosts:
			print('  %s' % h.host.id)
		
		print('')
	
	if len(available_hosts) < 1:
		print('All hosts are up-to-date.')
		return []
	
	print('The following hosts need upgrades:')
	for h in available_hosts:
		if len(h.changes) > 0:
			print('  %s' % h.host.id)
	
	res = raw_input('Which hosts do you want to upgrade? [all] ')
	
	if res == '':
		hosts = available_hosts
	else:
		selected_hosts = res.split(',')
		hosts = []
		for h in available_hosts:
			for sel in selected_hosts:
				if h.host.id == sel:
					hosts.append(h)
	
	if len(hosts) < 1:
		raise AbortException('No host selected.')
	
	return hosts

def sortChanges(changes):
	install = []
	reinstall = []
	upgrade = []
	downgrade = []
	remove = []
	keep = []
	for c in changes:
		if c.operation == c.INSTALL:
			install.append(c.package)
		elif c.operation == c.REINSTALL:
			reinstall.append(c.package)
		elif c.operation == c.UPGRADE:
			upgrade.append(c.package)
		elif c.operation == c.DOWNGRADE:
			downgrade.append(c.package)
		elif c.operation == c.REMOVE:
			remove.append(c.package)
		elif c.operation == c.KEEP:
			keep.append(c.package)
	
	install.sort(key=lambda p: p.name)
	reinstall.sort(key=lambda p: p.name)
	upgrade.sort(key=lambda p: p.name)
	downgrade.sort(key=lambda p: p.name)
	remove.sort(key=lambda p: p.name)
	keep.sort(key=lambda p: p.name)
	
	return {'install': install, 'reinstall': reinstall, 'upgrade': upgrade, 'downgrade': downgrade, 'remove': remove, 'keep': keep}

def printChanges(schanges):
	desc = {
		'install': 'The following NEW packages will be installed:',
		'reinstall': 'The following packages will be REINSTALLED:',
		'upgrade': 'The following packages will be upgraded:',
		'downgrade': 'The following packages will be DOWNGRADED:',
		'remove': 'The following packages will be REMOVED:',
		'keep': 'The following packages have been kept back:'
	}
	total_size = 0
	total_install_size = 0
	for operation, changes in schanges.iteritems():
		if len(changes) > 0:
			print(desc[operation])
			printPackages(changes)
			size, install_size = calculateSize(changes)
			total_size = total_size + size
			total_install_size = total_install_size + install_size
	
	# TODO: What to do with reinstall, downgrade?
	print('%d packages upgraded, %d newly installed, %d to remove and %d not upgraded.' % (len(schanges['upgrade']), len(schanges['install']), len(schanges['remove']), len(schanges['keep'])))
	
	if total_install_size >= 0:
		print('Need to get %s of archives. After unpacking %s will be used.' % (formatSize(total_size), formatSize(total_install_size)))
	else:
		print('Need to get %s of archives. After unpacking %s will be freed.' % (formatSize(total_size), formatSize(-total_install_size)))

def printPackages(pkgs):
	sys.stdout.write(' ')
	linelen = 3
	for p in pkgs:
		l = len(p.name) + 1
		if linelen + l > 80:
			sys.stdout.write('\n  ')
			linelen = l + 3
		else:
			sys.stdout.write(' ')
			linelen = linelen + l
		
		sys.stdout.write('%s' % p.name)
	
	print('')

def calculateSize(pkgs):
	size = 0
	install_size = 0
	
	for p in pkgs:
		if p.candidate is not None:
			size = size + p.candidate.size
			install_size = install_size + p.candidate.installed_size
		
		if p.installed is not None:
			install_size = install_size - p.installed.installed_size
	
	return size, install_size

SUFFIXES = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
def formatSize(size):
	suffix = 0
	while size > 1024:
		suffix = suffix + 1
		size = size / 1024
	
	return '%.1f %s' % (size, SUFFIXES[suffix])

def usage(argv):
	print('apt2d8 %s  Copyright (C) 2013  David Gnedt' % version.version_str)
	print('This program comes with ABSOLUTELY NO WARRANTY.')
	print('This is free software, and you are welcome to redistribute it')
	print('under certain conditions.')
	print('')
	print('Usage: apt2d8 [options] <action>') # [host]
	print('')
	print('Actions:')
	print(' update  - Force check for new/upgradable packages.')
	print(' upgrade - Perform an upgrade.')
	print('')
	print('Options:')
	print(' -h  This help text.')

if __name__ == '__main__':
	main(sys.argv)

