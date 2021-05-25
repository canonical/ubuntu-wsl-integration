#    ubuntuwslctl.decor - TUI decoration library
#    Copyright (C) 2021 Canonical Ltd.
#    Copyright (C) 2021 Patrick Wu
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

from urwid import Divider, WidgetWrap, AttrMap, Text, Button, Padding, CheckBox, Pile, AttrWrap, Edit, ListBox, \
    SimpleListWalker

blank = Divider()  # friendly name for Divider


class TuiButton(WidgetWrap):
    '''
    Custom button that used in the footer
    '''

    def __init__(self, label, on_press=None, user_data=None):
        self.widget = Text(label)
        self.widget = AttrMap(self.widget, 'footer')
        self._hidden_btn = Button(label, on_press, user_data)

        super().__init__(self.widget)

    def selectable(self):
        return True

    def keypress(self, *args, **kw):
        return self._hidden_btn.keypress(*args, **kw)

    def mouse_event(self, *args, **kw):
        return self._hidden_btn.mouse_event(*args, **kw)


class StyledText(Padding):

    def __init__(self, content, style=None, assigned_value=None):
        """
        General Text Field

        Args:
            content: the text.
            style: the style of the text, can be `title` or `subtitle`, leave for the plain padded text.
        """
        self.text = content
        self.assigned_value = assigned_value
        _text = self.text
        _min_width = None
        _align = "left"
        if style == 'title':
            _text = ('nv', self.text)
        elif style == 'subtitle':
            _text = ('subttl', "* " + self.text)
            _min_width = 20
        super().__init__(Text(_text, align=_align), left=2, right=2, min_width=_min_width)

    def get_text(self):
        return self.text

    def get_assigned_value(self):
        return self.assigned_value


class SelectableStyledText(StyledText):
    """
    General Selectable Text Field

    Args:
        content: the text.
        style: the style of the text, can be `title` or `subtitle`, leave for the plain padded text.
    """
    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class StyledCheckBox(Padding):
    def __init__(self, content, default, tooltip, left_margin, source=None):
        """
        General Checkbox Field

        Args:
            content: text of the checkbox
            default: default value of the checkbox
            tooltip: the tooltip of the checkbox
            left_margin: The left margin of the Checkbox
            source: there this item is from for value reference
        """
        self.core = CheckBox(content, state=default)
        self.source = source
        self.widget = Pile([
            self.core,
            Padding(Text(tooltip), left=4)
        ])
        super().__init__(self.widget, left=2 + left_margin - 4, right=2)

    def get_source(self):
        return self.source

    def get_core_value(self):
        return "true" if self.core.get_state() else "false"


class StyledEdit(Padding):
    def __init__(self, content, default, tooltip, left_margin, source=None):
        """
        General Edit Field

        Args:
            content: text of the editbox
            default: default value of the editbox
            tooltip: tooltip of the editbox
            left_margin: left_margin of the editbox
            source: there this item is from for value reference
        """
        text = u" *  "+content + u": "
        self.core = Edit(('editcp', ""), default)
        self.source = source
        self.widget = Pile([
            Text(text),
            Padding(AttrWrap(self.core, 'editbx', 'editfc'), left=4),
            Padding(Text(tooltip), left=4)
        ])
        super().__init__(self.widget, left=2 + left_margin - 4, right=2)

    def get_source(self):
        return self.source

    def get_core_value(self):
        return self.core.get_edit_text()


class SimpleListBox(ListBox):
    """
    A ListBox that exposes its walker.

    Args:
        content: a list of widgets.
    """
    def __init__(self, content):
        self.walker = SimpleListWalker(content)
        super(SimpleListBox, self).__init__(self.walker)
