#!/usr/bin/env python
# coding: utf-8
#
# Urwid tour.  It slices, it dices..
#    Copyright (C) 2004-2011  Ian Ward
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Urwid web site: http://excess.org/urwid/

"""
Urwid tour.  Shows many of the standard widget types and features.
"""

import urwid
import urwid.raw_display
from ubuntuwslctl.core.generator import SuperHandler
from ubuntuwslctl.core.default import conf_def
from ubuntuwslctl.utils.helper import str2bool


def tui_main(ubuntu, wsl):
    text_header = u"Ubuntu WSL Configuration UI (Experimental)"
    text_footer = u"UP / DOWN / PAGE UP / PAGE DOWN: scroll F5: save F8: exit"
    config = SuperHandler(ubuntu, wsl, '', 'json').get_config()

    # general_text = lambda x : urwid.Padding(urwid.Text(x), left=2, right=2)
    general_title = lambda x: urwid.Padding(urwid.Text(('important', x)), left=2, right=2, min_width=20)
    general_subtitle = lambda x: urwid.Padding(urwid.Text(('subimportant', x)), left=2, right=2, min_width=20)
    general_edit = lambda x, y: urwid.Padding(urwid.AttrWrap(urwid.Edit(('editcp', x), y), 'editbx', 'editfc'), left=2,
                                              width=50)
    general_checkbox = lambda x, y: urwid.Padding(urwid.CheckBox(x, state=y), left=2, right=2)

    blank = urwid.Divider()

    listbox_content = []

    listbox_content.append(blank)
    for i in config.keys():
        listbox_content.append(general_title(conf_def[i]['_friendly_name']))
        listbox_content.append(blank)
        i_tmp = config[i]
        for j in i_tmp.keys():
            listbox_content.append(general_subtitle(conf_def[i][j]['_friendly_name']))
            listbox_content.append(blank)
            j_tmp = i_tmp[j]
            for k in j_tmp.keys():
                if isinstance(j_tmp[k], bool):
                    listbox_content.append(general_checkbox(conf_def[i][j][k]['_friendly_name'], j_tmp[k]))
                elif isinstance(j_tmp[k], str):
                    if j_tmp[k].lower() in ("yes", "no", "1", "0", "true", "false"):
                        listbox_content.append(general_checkbox(conf_def[i][j][k]['_friendly_name'], str2bool(j_tmp[k])))
                    else:
                        listbox_content.append(general_edit(conf_def[i][j][k]['_friendly_name'], j_tmp[k]))
            listbox_content.append(blank)

    header = urwid.AttrWrap(urwid.Text(text_header), 'header')
    footer = urwid.AttrWrap(urwid.Text(text_footer), 'header')
    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
    frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header, footer=footer)

    palette = [
        ('body', '', '', 'standout'),
        ('reverse', 'light gray', 'black'),
        ('header', 'black', 'white', 'bold'),
        ('important', 'dark blue', 'light gray', ('standout', 'underline')),
        ('subimportant', 'dark blue', 'light gray', 'bold'),
        ('editfc', 'white', 'black', 'bold'),
        ('editbx', 'black', 'white'),
        ('editcp', '', '', 'standout'),
        ('bright', 'dark gray', 'light gray', ('bold', 'standout')),
        ('buttn', 'black', 'dark cyan'),
        ('buttnf', 'white', 'dark blue', 'bold'),
    ]

    # use appropriate Screen class
    screen = urwid.raw_display.Screen()

    def unhandled(key):
        if key == 'f8':
            raise urwid.ExitMainLoop()

    urwid.MainLoop(frame, palette, screen,
                   unhandled_input=unhandled).run()
