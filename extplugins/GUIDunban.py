# GUIDunban Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)
# Copyright (c) 2018 Miltan aka WatchMiltan
#
# LOG:
# 25.05.2018 - v1.0 - WatchMiltan
# - first release.
# 05.06.2018 - v1.1 - WatchMiltan
# - bugfix
#

__version__ = '1.1gh'
__author__  = 'WatchMiltan'

#b3 libaries
import b3
import b3.events
import b3.plugin
from b3.clients import Client, Group

import fileinput
import sys
import re

file = "C:\Games\CallofDutyModernWarfare3\BanDB\Permanent_GUID.ban"

class GuidunbanPlugin(b3.plugin.Plugin):
    requiresConfigFile = False

    def onStartup(self):
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.debug("Admin Plugin not found!")
            return False
        else:
            self.debug("Plugin successfully loaded")

        self._adminPlugin.registerCommand(self, 'guidunban', 70, self.cmd_guidunban, 'gub') 
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

            f = open(file, 'r')
            if str(searchExp) not in f.read():
                client.message('No GUID-Ban found.')
                f.close()
            else:
                f.close()
                for line in fileinput.input(file, inplace=True):
                    if searchExp in line:
                        line = re.sub(searchExp+'.+',replaceExp, line)
                        client.message('GUID-Ban ^2lifted!')
                        self.debug(cid +" GUID unbanned by " + unbanner)
                    sys.stdout.write(line)
                for line in fileinput.input(file, inplace=1):
                    if line.rstrip():
                        sys.stdout.write(line)
