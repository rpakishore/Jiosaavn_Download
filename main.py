#!/usr/bin/env python
# coding: utf-8

import argparse
from util import main_util_class

version_number = '0.1'

def ParseCmdLine(cmd_line=None):
    # https://docs.python.org/zh-tw/3/howto/argparse.html
    # https://docs.python.org/zh-tw/3/library/argparse.html#module-argparse
    parser = argparse.ArgumentParser(description='Template Title')
    parser.add_argument('-v', '--version', action='version', version=version_number)
    parser.add_argument('-f', '--filename', type=str, default='nosync_userinput.json')
    parser.add_argument('-p', '--playlist', type=str, default=None)
    parser.add_argument('-s', '--song', type=str, default=None)
    parser.add_argument('-sd', '--skipdownloaded', default=False, action='store_true', help='Skips previously downloaded songs')
    parser.add_argument('-wc', '--writecache', default=False, action='store_true', help='Write to Cache file')
    parser.add_argument('-dp', '--defaultplaylist', default=False, action='store_true', help='Downloads song from default playlists definied in `-f` file.')
    parser.add_argument('-pc', '--printcache', default=False, action='store_true', help='Prints the contents of cache file')
    #parser.add_argument('-b', '--Blessing', type=int, choices=range(0, 6), help='Blessing - 0: profile; 1:Eng; 2:Atk; 3:Def; 4:Health; 5:STA')
    #parser.add_argument('-AB', '--ArenaBattle', type=int, help='Auto Battle [NumOfTimes] - [NumOfTimes]: Number of battles to do')
    #parser.add_argument('-g', '--Guild', choices=['Any', 'YoPing', 'Fu', 'Lu'], default='Any', type=str, help='Specify guild to do actions')
    #parser.add_argument('--verbose', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='ERROR', type=str, help='Level of information, default=%(default)s')
	#parser.add_argument('--delay_time', default=90, type=CheckPositive, help='Delay time between tests (secs) >0, default=%(default)s')
	#parser.add_argument('--no_setup', dest='setup', default=True, action='store_false', help='Do not setup test')
	
    if cmd_line:
        args = parser.parse_args(cmd_line)
    else:
        args = parser.parse_args()

    print(args)
    return args


def Main(args): 
    Task = main_util_class.main_instance(args)
    Task.do_actions()
    del Task
    return 1

if __name__ == '__main__':
	rc = -1
	args = ParseCmdLine()

	rc = Main(args)
	exit(rc)
