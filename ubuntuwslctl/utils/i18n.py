#    ubuntuwslctl.i18n - internationalization
#    Copyright (C) 2021 Canonical Ltd.
#
#    Authors: Patrick Wu <patrick.wu@canonical.com>

import os
import gettext

localedir = '/usr/share/locale'
build_mo = os.path.realpath(__file__ + '/../../build/mo/')
if os.path.isdir(build_mo):
    localedir = build_mo
translation = gettext.translation('ubuntuwslctl', localedir=localedir, fallback=True)