"""
This script assists in adapting a command used in one of the steps of a larger procedure.
See README.md for the full instructions.
"""

from __future__ import print_function
import os
from sys import argv

if len(argv) != 2:
	raise Exception("Provide new path as argument")

cmd = r'''git filter-branch --prune-empty -f --tree-filter '
git ls-tree --name-only -r $GIT_COMMIT | egrep -v "^%newpath/" | xargs -L1 dirname | xargs -I thedir mkdir -pv %newpath/thedir
git ls-tree --name-only -r $GIT_COMMIT | egrep -v "^%newpath/" | xargs -I thepath mv -v thepath %newpath/thepath
'
'''

print(cmd.replace("%newpath", argv[1].strip("/")))
