# -*- coding: utf-8 -*-

################################################################################
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with OpenELEC.tv; see the file COPYING.  If not, write to
#  the Free Software Foundation, 51 Franklin Street, Suite 500, Boston, MA 02110, USA.
#  http://www.gnu.org/copyleft/gpl.html
################################################################################

# v 1.0.0

import xbmc;  # @UnresolvedImport
import xbmcgui; # @UnresolvedImport
import xbmcaddon; # @UnresolvedImport

addon= xbmcaddon.Addon(id='plugin.program.smartmontools');


def getStringFromUser(heading, hidden = False, default = ""):
    keyboard = xbmc.Keyboard('default', 'heading', True)
    keyboard.setDefault(default);
    keyboard.setHeading(heading);
    keyboard.setHiddenInput(hidden);
    keyboard.doModal();
    if (keyboard.isConfirmed()):
        return keyboard.getText();
    else:
        return "";

def getConfirmedPassword(header1 = xbmc.getLocalizedString(12340), header2 = xbmc.getLocalizedString(12341)):   # Enter password   # Re-Enter password
    while True:
        str1 = getStringFromUser(header1, True);
        str2 = getStringFromUser(header2, True); 
        if str1 == str2:
            break;
        else :
            xbmcgui.Dialog().ok(addon.getLocalizedString(50012), addon.getLocalizedString(50010));  # Info,  "Passwords don't match."
            del str2;
            del str1;
    del str2;
    return str1;

def getFilePathFromUser(type, heading, shares = "files"):
    """
    type:
    0 : ShowAndGetDirectory
    1 : ShowAndGetFile
    2 : ShowAndGetImage
    3 : ShowAndGetWriteableDirectory
    """
    return xbmcgui.Dialog().browse(type, heading, shares);

def getAvailableAudioStreams(path):
    '''
    Returns names of audio streams contained in the video file. Previous playback is stopped. 
    :param path: path to the file
    :type path: str
    :rtype []
    '''
    player = xbmc.Player();
    player.stop();
    player.play(path);
    while not player.isPlayingVideo():
        xbmc.sleep(15);
    audioStreams = player.getAvailableAudioStreams();
    player.stop(); 
    return audioStreams;

def getNumberFromUser(type, title, default=""):
    """
    Types:
      0 : ShowAndGetNumber    (default format: #)
      1 : ShowAndGetDate      (default format: DD/MM/YYYY)
      2 : ShowAndGetTime      (default format: HH:MM)
      3 : ShowAndGetIPAddress (default format: #.#.#.#)
    """
    string = xbmcgui.Dialog().numeric(type, title, default);
    return string;

def createParamStringFromDictionairy(dic, includeQuestionMark = True):
    s = "?" if includeQuestionMark else "";
    for key in dic.keys():
        s += ("&" if len(s) > 1 else "" ) + str(key) + "=" + str(dic[key]);
    return s;
        

def refeshCurrentWindow():
    windowID = xbmcgui.getCurrentWindowId();
    xbmc.executebuiltin('ReplaceWindow('+ str(windowID)+")");

def refreshCurrentListing():
    xbmc.executebuiltin("Container.Refresh");
    
def showTextView(header = "", text = ""):
    window = TextWindow();
    window.header = header;
    window.body = text;
    window.doModal();

    
class TextWindow(WindowXMLDialog):

    def __new__(cls):
        return super(TextWindow, cls).__new__(cls, "DialogTextViewer.xml", "");

    def onInit(self):
        self.getControl(1).setLabel(self.header if self.header else "");
        self.getControl(5).setText(self.body if self.body else "");
        
    def onAction(self, action):        
        if action == 10 or action == 92 or action == 9:
            self.close();