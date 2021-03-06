#
# ################################################################### #
#                                                                     #
#  GUIDunban Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)     #
#  Copyright (c) 2018 Miltan aka WatchMiltan                          #
#                                                                     #
#  This program is free software; you can redistribute it and/or      #
#  modify it under the terms of the GNU General Public License        #
#  as published by the Free Software Foundation; either version 2     #
#  of the License, or (at your option) any later version.             #
#                                                                     #
#  This program is distributed in the hope that it will be useful,    #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the       #
#  GNU General Public License for more details.                       #
#                                                                     #
#  You should have received a copy of the GNU General Public License  #
#  along with this program; if not, write to the Free Software        #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA      #
#  02110-1301, USA.                                                   #
#                                                                     #
# ################################################################### #
#
# NOTE: There is a working parser for b3, rendering this plugin useless.
#
# PLEASE RESTART MAP AFTER PLUGIN IS LOADED!
#
#  LOG:
#  25.05.2018 - v1.0 - WatchMiltan
#  - first release.
#  05.06.2018 - v1.1 - WatchMiltan
#  - bugfix
#  24.06.2018 - v1.2 - WatchMiltan
#  - added multigame support
#  - retrieving data from config
#  28.01.2019 - v1.3 - WatchMiltan
#  - bugfix
#

__version__ = '1.2gh'
__author__  = 'WatchMiltan'

#b3 libaries
import b3
import b3.events
import b3.plugin
from b3.clients import Client, Group

import fileinput
import sys
import re

class GuidunbanPlugin(b3.plugin.Plugin):

    def onLoadConfig(self):
        self.file = str(self.config.get('settings', 'filepath'))
        return
    
    def onStartup(self):
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.debug("Admin Plugin not found!")
            return False
        else:
            self.debug("Plugin successfully loaded")

        self._adminPlugin.registerCommand(self, 'guidunban', 70, self.cmd_guidunban, 'gub') # change "70" to desired power level
        self.debug("Command registered in admin plugin")

    def stripColors(self, s):
        return re.sub('\^[0-9]{1}','',s)

    def cmd_guidunban(self, data, client=None, cmd=None):
        m = self._adminPlugin.parseUserCmd(data)
        if not data:
            client.message('^7Correct syntax: ^7!gub/!guidunban @PlayerID')
            return False

        cid = str(m[0])
        sclient = self._adminPlugin.findClientPrompt(cid, client)
        unbanner = self.stripColors(client.exactName)
        if sclient:
            searchExp = getattr(sclient, "guid")
            ip = getattr(sclient, "ip")
            replaceExp = ''
                             
            if "cod8" in game.lower():
                try:
                    f = open(self.file, 'r')
                    if str(searchExp) not in f.read():
                        client.message('No GUID-Ban found.')
                        f.close()
                    else:
                        f.close()
                        for line in fileinput.input(self.file, inplace=True):
                            if searchExp in line:
                                line = re.sub(searchExp+'.+',replaceExp, line)
                                client.message('GUID-Ban ^2lifted!')
                                self.debug(cid +" GUID unbanned by " + unbanner)
                            sys.stdout.write(line)
                        for line in fileinput.input(self.file, inplace=1):
                            if line.rstrip():
                                sys.stdout.write(line)
                except:
                    client.message('^7MW3-GUID Unban ^1failed.')
                    #troubleshooting: correct filepath? is file being accessed?
