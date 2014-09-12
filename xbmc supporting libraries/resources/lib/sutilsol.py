# -*- coding: utf-8 -*-
'''
Module contains utility methods which are primarily meant to be used on OpenELEC. 
Created on 6.12.2013

@author: Peter
'''

################################################################################
#  Copyright (C) Peter Smorada 2014 (smoradap@gmail.com)
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

import subprocess

flagEth0 = 2;
flagEth1 = 4;
flagWlan0 = 8;
flagWlan1 = 16;
flagProcCores = 32;
flagMbSerial = 64;

def getProcessorsCoreTypes():
    cmd = "cat /proc/cpuinfo | awk \"/name/\"\'{print substr($0, index($0,$4))}\'";            
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True);
    output, errors = p.communicate();
    output = output if output else " ";
    
    cores = output.split("\n");
    cores.sort()

    s = "";
    for core in cores:
        if core == "":
            continue;
        s += core.strip() + "\n"
    return s.strip();

def getMacAdressesOfAdapter(adapter = None):
    cmd = "ifconfig" + (" " + adapter if adapter else "" ) + " | awk \"/HWaddr/\"\'{print $5}\'";            
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True);
    output, errors = p.communicate();
    output = output.strip() if output else " ";
    
    if adapter == None:
        macs = output.split("\n");
        macs.sort();
        
        s = "";
        for mac in macs:
            if mac == "":
                continue;
            s += mac.strip() + "\n"
        return s.strip();
    else:
        return output.strip();

def getMotherBoardSerial():
    cmd = "cat /sys/class/dmi/id/product_uuid";            
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True);
    output, errors = p.communicate();
    return output.strip() if output else "";
    
def getHardwareKey(flag):
    s = "";
    
    '''sometimes not all requested information is available, therefore this flag is returned to reflect real used devices.'''
    usedFlag = 0; 
    
    if (flag  & (1 << 1)) != 0:
        eth0 = getMacAdressesOfAdapter("eth0");
        if eth0:
            s += eth0;
            usedFlag = usedFlag | flagEth0;
            
    if (flag  & (1 << 2)) != 0:
        eth1 = getMacAdressesOfAdapter("eth1");
        if eth1:
            s += "\n" +eth1;
            usedFlag = usedFlag | flagEth1;
            
    if (flag  & (1 << 3)) != 0:
        wlan0 = getMacAdressesOfAdapter("wlan0");
        if wlan0:
            s += "\n" + wlan0;
            usedFlag = usedFlag | flagWlan0;
        
    if (flag  & (1 << 4)) != 0:
        wlan1 = getMacAdressesOfAdapter("wlan1");
        if wlan1:
            s += "\n" + wlan1;
            usedFlag = usedFlag | flagWlan1;

    if (flag  & (1 << 5)) != 0:        
        cores = getProcessorsCoreTypes();
        if cores:
            s += "\n" + cores;
            usedFlag = usedFlag | flagProcCores;

    if (flag  & (1 << 6)) != 0:
        mb = getMotherBoardSerial();
        if mb:
            s += "\n" + mb;
            usedFlag = usedFlag | flagMbSerial;

    return s, usedFlag; 