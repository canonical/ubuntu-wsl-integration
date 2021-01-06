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
    """
    General Text Field

    Args:
        content: text of the content.
    Returns:
        a Padded Text
    """
    return urwid.Padding(urwid.Text(content), left=2, right=2)


def tui_title(content):
    """
    General Title Field

    Args:
        content: text of the title.
    Returns:
        a themed title
    """
    return urwid.Padding(urwid.Text(('ttl', content)), left=2, right=2, min_width=20)


def tui_subtitle(content):
    """
    General Subtitle Field

    Args:
        content: text of the subtitle.
    Returns:
        a themed subtitle
    """
    return urwid.Padding(urwid.Text(('subttl', content)), left=2, right=2, min_width=20)


def tui_checkbox(content, default, tooltip, left_margin):
    """
    General Checkbox Field

    Args:
        content: text of the checkbox
        default: default value of the checkbox
        tooltip: the tooltip of the checkbox
        left_margin: The left margin of the Checkbox
    Returns:
        a general checkbox field
    """
    cbset = urwid.Pile([
        urwid.CheckBox(content, state=default),
        urwid.Padding(urwid.Text(tooltip), left=4)
    ])
    return urwid.Padding(cbset, left=2 + left_margin - 4, right=2)


def tui_edit(content, default, tooltip, left_margin):
    """
    General Edit Field

    Args:
        content: text of the editbox
        default: default value of the editbox
        tooltip: tooltip of the editbox
        left_margin: left_margin of the editbox
    Returns:
        a general edit field
    """
    text = content + u": "
    edset = urwid.Pile([
        urwid.AttrWrap(urwid.Edit(('editcp', text), default), 'editbx', 'editfc'),
        urwid.Padding(urwid.Text(tooltip), left=len(text))
    ])
    return urwid.Padding(edset, left=2 + left_margin - len(text), right=2)


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
        self.content = []

        self._body_builder()
        self._loop = urwid.MainLoop(self._body, self._palette, urwid.raw_display.Screen(),
                                    unhandled_input=self._unhandled_key)

    def _fun(self, button=None, fun=None):
        """
        Core function for different actions.
        This function can accept button callback from `button` or function name from `func`

        Args:
            button: the `urwid.Button` instance returned from a button callback.
            fun: the name of the function
        """
        if button is not None:
            fun = button.label
            fun = fun[2:].lower()
        if fun in ("", "exit"):
            raise urwid.ExitMainLoop()
        elif fun == "reload":
            self._body_builder()
            self._popup_constructor(fun, urwid.Text(u"Configuration Reloaded.", align='left'))
        elif fun == "reset":
            def _reset(button):
                self.handler.reset_all()
                self._body_builder()
                self._popup_constructor(fun, urwid.Text(u"Reset complete. Restart Ubuntu to take effect.",
                                                        align='left'))
            body = urwid.Text(u"Do you really want to reset?", align='left')
            ok_btn = urwid.AttrWrap(urwid.Button('Yes', _reset), 'selectable', 'focus')
            cc_btn = urwid.AttrWrap(urwid.Button('No', self._reload_ui), 'selectable', 'focus')
            footer = urwid.GridFlow([ok_btn, cc_btn], 10, 1, 1, 'center')
            self._popup_constructor(fun, body, footer)
        elif fun == "export":
            exp_name = urwid.Edit(u"", "")

            def _export(button):
                ef = self.handler.export_file(exp_name.edit_text)
                self._popup_constructor(fun, urwid.Text(u"Exported as {}.".format(ef),
                                                        align='left'))
            body = urwid.Pile([
                        urwid.Text(u"file name to export(optional): ", align='left'),
                        urwid.AttrWrap(exp_name, 'editbx', 'editfc')
                   ])
            ok_btn = urwid.AttrWrap(urwid.Button('Yes', _export), 'selectable', 'focus')
            cc_btn = urwid.AttrWrap(urwid.Button('No', self._reload_ui), 'selectable', 'focus')
            footer = urwid.GridFlow([ok_btn, cc_btn], 10, 1, 1, 'center')
            self._popup_constructor(fun, body, footer)
        elif fun == "import":
            exp_name = urwid.Edit(u"", "")

            def _import(button):
                ef = self.handler.import_file(exp_name.edit_text)
                self._popup_constructor(fun,
                                        urwid.Text(u"{} imported. Please restart Ubuntu to take effect.".format(ef),
                                        align='left'))
            body = urwid.Pile([
                        urwid.Text(u"file name to import: ", align='left'),
                        urwid.AttrWrap(exp_name, 'editbx', 'editfc')
                   ])
            ok_btn = urwid.AttrWrap(urwid.Button('Yes', _import), 'selectable', 'focus')
            cc_btn = urwid.AttrWrap(urwid.Button('No', self._reload_ui), 'selectable', 'focus')
            footer = urwid.GridFlow([ok_btn, cc_btn], 10, 1, 1, 'center')
            self._popup_constructor(fun, body, footer)
        else:  # unhandled input all went here
            self._popup_constructor(fun)

    def _footer(self):
        return urwid.GridFlow(
            (
                urwid.AttrWrap(TuiButton([('footerhlt', u'F1'), u'Save'], self._fun), 'footer'),

                urwid.AttrWrap(TuiButton([('footerhlt', u'F2'), u'Reset'], self._fun), 'footer'),
                urwid.AttrWrap(TuiButton([('footerhlt', u'F3'), u'Import'], self._fun), 'footer'),
                urwid.AttrWrap(TuiButton([('footerhlt', u'F4'), u'Export'], self._fun), 'footer'),
                urwid.AttrWrap(TuiButton([('footerhlt', u'F5'), u'Reload'], self._fun), 'footer'),
                urwid.AttrWrap(TuiButton([('footerhlt', u'F6'), u'Exit'], self._fun), 'footer')
            ),
            10, 0, 0, 'left')

    def _popup_constructor(self, fun, body=None, footer=None):
        """
        Construct a popup widget that overlays the UI.

        Args:
            fun: title of the Popup
            body: content of the Popup. Leave empty for the placeholder.
            footer: footer of the Popup. Leave empty for the single Okay button.
        """
        self._loop.widget = urwid.Overlay(self._popup_widget(fun, body, footer), self._loop.widget, align='center',
                                          valign='middle', height='pack', width=40)

    def _reload_ui(self, button):
        """
        Clear the Overlay and reload everything again.
        """
        self._loop.widget = self._body

    def _popup_widget(self, header, body=None, footer=None):
        """
        Content of the Popup Widget.

        Args:
            header: title of the Popup
            body: content of the Popup. Leave empty for the placeholder.
            footer: footer of the Popup. Leave empty for the single Okay button.
        Returns:
            `urwid.LineBox` that hold the widget.
        """
        # Body
        if body is None:
            body = urwid.Text(('This is a placeholder text that will only be displayed '
                               'when _popup_widget.body received None. If you see this '
                               'in a production version of ubuntuwsl, Please report the '
                               'bug to WSL team at Canonical.'), align='left')

        body = urwid.Padding(body, left=1, right=1)

        # Footer
        if footer is None:
            footer = urwid.Button('Okay', self._reload_ui)
            footer = urwid.AttrWrap(footer, 'selectable', 'focus')
            footer = urwid.GridFlow([footer], 8, 1, 1, 'center')

        # Layout
        return urwid.LineBox(urwid.Pile([blank, body, blank, footer]),
                             title=header.title(), title_attr='header', title_align='center')

    def _parse_config(self):
        self.content = [blank]

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

    def _body_builder(self):
        """
        Allows building the body.
        Also used in page refreshing after a reset and when pressing reload botton
        """
        self._parse_config()

        header = urwid.AttrWrap(urwid.Text(u"Ubuntu WSL Configuration UI (Experimental)"), 'header')
        footer = urwid.AttrWrap(self._footer(), 'footer')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.content))
        self._body = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header, footer=footer)

    def _unhandled_key(self, key):
        """
        handle keys
        """
        if key in ('f6', 'ctrl c', 'esc'):
            self._fun(fun='exit')
        elif key == 'f5':
            self._fun(fun='reload')
        elif key == 'f4':
            self._fun(fun='export')
        elif key == 'f3':
            self._fun(fun='import')
        elif key == 'f2':
            self._fun(fun='reset')
        elif key == 'f1':
            self._fun(fun='save')

    def run(self):
        """
        Start the UI
        """
        self._loop.run()
