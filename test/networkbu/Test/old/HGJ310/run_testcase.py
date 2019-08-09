import os
import sys
import datetime


def run_test(*argv):
    #os.system('netsh wlan disconnect')
    run_scripts = ''
    for i in range(1, len(sys.argv)):
        run_scripts += ' ' + str(sys.argv[i])

    os.system('python HGJ310_Webui.py ' + run_scripts + '> ../Report/report_'+str(datetime.datetime.now()).replace(' ', '_').replace(':', '-')+'.html')

    #os.system('netsh wlan connect name=HVNWifi')

    #os.chdir('C:\\jenkins-slave')
    #os.system('jenkins-slave-auto.cmd')


if __name__=='__main__':
   run_test(sys.argv)