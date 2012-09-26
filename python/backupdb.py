#!/usr/bin/env python
import os
import sys
import getpass
from datetime import datetime
from subprocess import Popen, PIPE, call
from optparse import OptionParser as P

if __name__ == "__main__":
    p = P(description="",
          version="1.0",
          prog=os.path.basename(__file__),
          usage="%prog [options] [databases...]",
          epilog="Everything is ducky.")
    p.add_option("-u","--username",action="store",
                 help="Passes the user name to 'mysqldump'.")
    p.add_option("-p","--password",action="store_true",
                 help="Passes the '-p' flag to 'mysqldump' and prompts you to enter the password for the user.")
    p.add_option("-f","--filename",action="store_true",
                 help="Creates a file with the name pattern 'mysql_DATABASENAME_MM-DD-YYYY.dump' in the current working directory.")

    options, arguments = p.parse_args()
    if not arguments:
        p.print_help()
        sys.exit(1)
    
    current = datetime.timetuple(datetime.now())

    for database in arguments:
        if options.filename:
            out_file = open(os.path.abspath(os.curdir + os.sep + 'mysql_%s_%s-%s-%s.dump' % (database,current.tm_mon,current.tm_mday,current.tm_year)),'w')
        else:
            out_file = None

        #Construct command argument
        command = ['/usr/local/mysql/bin/mysqldump']
        if options.username:
            command.append('-u')
            command.append(options.username)
        if options.password:
            command.append('-p')
        command.append(database)

        #Execute command with and without PIPE
        p = Popen(command,stdout=PIPE)
        stdout, stderr = p.communicate()
        if out_file:
            try:
                out_file.write(stdout)
            except:
                pass
        else:
            print(stdout)
            
        try:
            out_file.close()
        except:
            pass
    sys.exit(0)
