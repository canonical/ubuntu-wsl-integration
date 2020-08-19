import os
import gettext

localedir = '/usr/share/locale'
build_mo = os.path.realpath(__file__ + '/../../build/mo/')
if os.path.isdir(build_mo):
    localedir = build_mo
translation = gettext.translation('ubuntuwslctl', localedir=localedir, fallback=True)