#    ubuntuwslctl.tui - TUI
#    Copyright (C) 2020 Canonical Ltd.
#    Copyright (C) 2020 Patrick Wu
#
#    Authors: Patrick Wu <patrick.wu@canonical.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This package is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  On Debian systems, the complete text of the GNU General
#  Public License version 3 can be found in "/usr/share/common-licenses/GPL-3".

import urwid
import urwid.raw_display
from ubuntuwslctl.core.generator import SuperHandler
from ubuntuwslctl.core.default import conf_def
from ubuntuwslctl.utils.helper import str2bool


class TuiButton(urwid.WidgetWrap):
    '''
    Custom button that used in the footer
    '''
    def __init__(self, label, on_press=None, user_data=None):
        self.widget = urwid.Text(label)
        self.widget = urwid.AttrMap(self.widget, 'footer')
        self._hidden_btn = urwid.Button(label, on_press, user_data)

        super().__init__(self.widget)

    def selectable(self):
        return True

    def keypress(self, *args, **kw):
        return self._hidden_btn.keypress(*args, **kw)

    def mouse_event(self, *args, **kw):
        return self._hidden_btn.mouse_event(*args, **kw)


blank = urwid.Divider() # friendly name for Divider


def tui_text(content):
    '''
    Text Field
    '''
    return urwid.Padding(urwid.Text(content), left=2, right=2)


def tui_title(content):
    return urwid.Padding(urwid.Text(('ttl', content)), left=2, right=2, min_width=20)


def tui_subtitle(content):
    return urwid.Padding(urwid.Text(('subttl', content)), left=2, right=2, min_width=20)


def tui_checkbox(content, default, tooltip, left_margin):
    cbset = urwid.Pile([
        urwid.CheckBox(content, state=default),
        urwid.Padding(urwid.Text(tooltip), left=4)
    ])
    return urwid.Padding(cbset, left=2 + left_margin - 4, right=2)


def tui_edit(content, default, tooltip, left_margin):

    text = content + u": "
    set = urwid.Pile([
        urwid.AttrWrap(urwid.Edit(('editcp', text), default), 'editbx', 'editfc'),
        urwid.Padding(urwid.Text(tooltip), left=len(text))
    ])
    return urwid.Padding(set, left=2 + left_margin - len(text), right=2)


class Tui:
    """
    Main class of the text-based UI for Ubuntu WSL config management
    """

    _palette = [
        ('body', '', '', 'standout'),                   # body
        ('header', 'black', 'white', 'bold'),           # header
        ('footer', 'black', 'dark cyan'),               # footer
        ('footerhlt', 'white', 'black'),                # footer highlight
        ('ttl', 'dark blue', 'white', 'standout'),      # section title
        ('subttl', 'light gray', '', 'standout'),       # section subtitle
        ('editfc', 'white', 'black', 'bold'),
        ('editbx', 'black', 'white'),
        ('editcp', '', '', 'standout'),
        ('selectable', 'white', 'black'),
        ('focus', 'black', 'light gray')
    ]

    def __init__(self, ubuntu, wsl):
        self.handler = SuperHandler(ubuntu, wsl)
        self.config = self.handler.get_config()
        self.content = [blank]

        self._parse_config()

        header = urwid.AttrWrap(urwid.Text(u"Ubuntu WSL Configuration UI (Experimental)"), 'header')
        footer = urwid.AttrWrap(self._footer(), 'footer')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.content))
        self._body = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header, footer=footer)
        self._loop = urwid.MainLoop(self._body, self._palette, urwid.raw_display.Screen(),
                                    unhandled_input=self._unhandled_key)

    def _fun(self, button=None, fun=None):
        if button is not None:
            fun = button.label
            fun = fun[2:].lower()
        if fun in ("", "exit"):
            raise urwid.ExitMainLoop()
        elif fun == "reset":

        else:
            self._popup_constructor(fun)

    def _footer(self):

        return urwid.GridFlow(
            (
                urwid.AttrWrap(TuiButton([('footerhlt', u'F1'), u'Save'], self._fun), 'footer'),
                urwid.AttrWrap(TuiButton([('footerhlt', u'F2'), u'Reset'], self._fun), 'footer'),
                urwid.AttrWrap(TuiButton([('footerhlt', u'F3'), u'Import'], self._fun), 'footer'),
                urwid.AttrWrap(TuiButton([('footerhlt', u'F4'), u'Export'], self._fun), 'footer'),
                urwid.AttrWrap(TuiButton([('footerhlt', u'F5'), u'Exit'], self._fun), 'footer')
            ),
            12, 0, 0, 'left')

    def _popup_constructor(self, fun):
        self._loop.widget = urwid.Overlay(self._popup_widget(fun), self._loop.widget, align='center',
                                          valign='middle', width=40, height=20)

    def _popup_rest_interface(self, button):
        self._loop.widget = self._body

    def _popup_widget(self, header, body=None, fun=None):
        '''
        Overlays a dialog box on top of the console UI
        '''

        # Header
        header_text = urwid.Text(('header', header.title()), align='center')
        header = urwid.AttrMap(header_text, 'header')

        # Body
        if body is None:
            body_text = urwid.Text(('This is a placeholder text that will only be displayed '
                                    'when _popup_widget.body received None. If you see this '
                                    'in a production version, Please report the bug.'), align='center')
            body = urwid.Filler(body_text, valign='top')

        body = urwid.Padding(body, left=1, right=1)

        # Footer
        if fun is None:
            fun = self._popup_rest_interface
        footer = urwid.Button('Okay', fun)
        footer = urwid.AttrWrap(footer, 'selectable', 'focus')
        footer = urwid.GridFlow([footer], 8, 1, 1, 'center')

        # Layout
        return urwid.ListBox(urwid.Filler(urwid.Pile([header, body, footer])))

    def _parse_config(self):
        # Widget margin calculation
        left_margin = 0
        for i in self.config.keys():
            i_tmp = self.config[i]
            for j in i_tmp.keys():
                j_tmp = i_tmp[j]
                for k in j_tmp.keys():
                    if isinstance(j_tmp[k], bool) and (left_margin < 4):
                        left_margin = 4
                    elif isinstance(j_tmp[k], str):
                        if j_tmp[k].lower() in ("yes", "no", "1", "0", "true", "false") and (left_margin < 4):
                            left_margin = 4
                        elif left_margin < len(k) + 2:
                            left_margin = len(k) + 2

        # Real config handling part
        for i in self.config.keys():
            self.content.append(tui_title(conf_def[i]['_friendly_name']))
            self.content.append(blank)
            i_tmp = self.config[i]
            for j in i_tmp.keys():
                self.content.append(tui_subtitle(conf_def[i][j]['_friendly_name']))
                self.content.append(blank)
                j_tmp = i_tmp[j]
                for k in j_tmp.keys():
                    if isinstance(j_tmp[k], bool):
                        self.content.append(tui_checkbox(conf_def[i][j][k]['_friendly_name'], j_tmp[k],
                                                         conf_def[i][j][k]['tip'], left_margin))
                    elif isinstance(j_tmp[k], str):
                        if j_tmp[k].lower() in ("yes", "no", "1", "0", "true", "false"):
                            self.content.append(tui_checkbox(conf_def[i][j][k]['_friendly_name'], str2bool(j_tmp[k]),
                                                             conf_def[i][j][k]['tip'], left_margin))
                        else:
                            self.content.append(tui_edit(conf_def[i][j][k]['_friendly_name'], j_tmp[k],
                                                         conf_def[i][j][k]['tip'], left_margin))
                self.content.append(blank)

    def _unhandled_key(self, key):
        if key in ('f5', 'ctrl c', 'esc'):
            self._fun(fun='exit')

    def run(self):
        self._loop.run()
