# -*- coding: utf-8 -*-
import urwid
import urwid_readline
import gkeepapi
from . import labels
from .. import constants
import logging

from typing import List

NEXT_SELECTABLE = 'next selectable'
PREV_SELECTABLE = 'prev selectable'

class Color(urwid.AttrMap):
    def __init__(self, color: gkeepapi.node.ColorValue, selected=False):
        self.color = color
        super(Color, self).__init__(
            urwid.Text(''),
            'c' + self.color.value,
            'cu' + self.color.value
        )
        self.selected = selected
        self.update()

    def keypress(self, size, key):
        if key == ' ':
            self.selected = not self.selected
            self.update()
            key = None

        return key

    def update(self):
        self.original_widget.set_text(' ✔ ' if self.selected else '   ')

    def selectable(self):
        return True

class Colors(urwid.GridFlow):
    def __init__(self):
        super(Colors, self).__init__([
            Color(color) for color in gkeepapi.node.ColorValue
        ], 3, 1, 0, urwid.LEFT)

    def getSelected(self) -> List[gkeepapi.node.ColorValue]:
        return [item.color for item, _ in self.contents if item.selected]

class Item(urwid.Columns):
    def __init__(self, item: gkeepapi.node.ListItem, indented=None):
        self.id = item.id
        self.checked = item.checked
        self.indented = indented if indented is not None else item.indented
        self.w_indent = urwid.Text('')
        self.w_checkbox = urwid.Text('')
        self.w_text = urwid_readline.ReadlineEdit(edit_text=item.text)
        super(Item, self).__init__([
            (urwid.PACK, self.w_indent),
            (urwid.PACK, self.w_checkbox),
            self.w_text,
        ], dividechars=1)

        self._updateIndent()
        self.updateChecked(self.checked)

    def indent(self):
        self.indented = True
        self._updateIndent()

    def dedent(self):
        self.indented = False
        self._updateIndent()

    def _updateIndent(self):
        self.w_indent.set_text(' ' if self.indented else '')
        self._invalidate()

    def toggleCheck(self):
        self.updateChecked(not self.checked)

    def updateChecked(self, checked):
        self.checked = checked
        self.w_checkbox.set_text(u'☑' if checked else u'☐')
        self._invalidate()

    def setPos(self, pos):
        self.w_text.edit_pos = pos

    def getText(self):
        return self.w_text.get_edit_text()

    def appendText(self, s):
        pos = len(self.getText())
        self.w_text.edit_pos = pos
        self.w_text.insert_text(s)
        self.w_text.edit_pos = pos

    def cutToEnd(self):
        text = self.getText()
        pos = self.w_text.edit_pos

        suffix = text[pos:]
        self.w_text.set_edit_text(text[:pos])
        return suffix

    def keypress(self, size, key):
        if key == 'backspace' and self.w_text.edit_pos == 0:
            return key
        if key == 'enter':
            return key

        key = super(Item, self).keypress(size, key)
        return key

class Items(urwid.ListBox):
    def __init__(self):
        super(Items, self).__init__(urwid.SimpleFocusListWalker([]))

    def refresh(self, items: List[gkeepapi.node.ListItem]):
        self.body[:] = [Item(item) for item in items]

    def keypress(self, size, key):
        def actual_key(unhandled):
            if unhandled:
                return key

        if self._command_map[key] == PREV_SELECTABLE:
            return actual_key(self._keypress_up(size))
        elif self._command_map[key] == NEXT_SELECTABLE:
            return actual_key(self._keypress_down(size))

        key = super(Items, self).keypress(size, key)
        if key == 'enter':
            pos = 0
            text = ''
            indented = None
            if self.focus is not None:
                text = self.focus.cutToEnd()
                pos = self.focus_position + 1

            if pos > 0:
                indented = self.body[pos - 1].indented
            item = gkeepapi.node.ListItem()
            item.text = text
            self.body.insert(pos, Item(item, indented))
            self.focus.setPos(0)
            self.focus_position = pos
            key = None
        elif key == 'backspace':
            pos = self.focus_position
            if pos > 0:
                text = self.body[pos].getText()
                last = pos == len(self.body) - 1
                del self.body[pos]
                if not last:
                    self.focus_position -= 1
                self.focus.appendText(text)
        elif key == 'meta [':
            pos = self.focus_position
            self.body[pos].dedent()
            key = None
        elif key == 'meta ]':
            pos = self.focus_position
            if pos > 0:
                self.body[pos].indent()
            key = None
        elif key == 'meta p':
            pos = self.focus_position
            if pos > 0:
                tmp = self.body[pos]
                self.body[pos] = self.body[pos - 1]
                self.body[pos - 1] = tmp
                if pos - 1 == 0:
                    self.body[pos - 1].dedent()
                self.focus_position = pos - 1
            key = None
        elif key == 'meta n':
            pos = self.focus_position
            if pos < len(self.body) - 1:
                tmp = self.body[pos]
                self.body[pos] = self.body[pos + 1]
                self.body[pos + 1] = tmp
                self.focus_position = pos + 1
            key = None
        elif key == 'meta x':
            pos = self.focus_position
            self.body[pos].toggleCheck()
            key = None

        return key

class Edit(urwid.AttrMap):
    def __init__(self, app: 'application.Application', note: gkeepapi.node.TopLevelNode):
        self.application = app
        self.note = note

        tmp = urwid.Text('')

        self.w_title = urwid_readline.ReadlineEdit(wrap=urwid.CLIP)
        self.w_text = urwid_readline.ReadlineEdit(multiline=True)
        self.w_list = Items()
        self.w_labels = labels.Labels()

        self.w_state = urwid.Text(u'', align=urwid.RIGHT)
        self.w_footer = urwid.Text(u'', align=urwid.RIGHT)
        self.w_content = urwid.Frame(
            tmp,
            header=tmp,
            footer=tmp
        )
        self.w_frame = urwid.Frame(
            urwid.Padding(
                self.w_content,
                align=urwid.CENTER,
                left=1,
                right=1
            ),
            header=self.w_state,
            footer=self.w_footer,
        )

        self.zen_mode = False

        super(Edit, self).__init__(
            self.w_frame,
            note.color.value
        )

        self._updateContent()
        self._updateLabels()
        self._updateState()

    def _updateContent(self):
        self.w_title.set_edit_text(self.note.title)
        self.w_content.contents['header'] = (
            urwid.AttrMap(self.w_title, 'b' + self.note.color.value),
            self.w_content.options()
        )

        w_body = None
        if isinstance(self.note, gkeepapi.node.List):
            self.w_list.refresh(self.note.items)
            w_body = (self.w_list, self.w_content.options())
        else:
            self.w_text.set_edit_text(self.note.text)
            w_body = (
                urwid.Filler(self.w_text, valign=urwid.TOP),
                self.w_content.options()
            )
        self.w_content.contents['body'] = w_body

    def _updateLabels(self):
        w_labels = (None, self.w_content.options())
        if len(self.note.labels):
            w_labels = (self.w_labels, self.w_content.options())
            self.w_labels.setLabels(self.note.labels.all(), self.note.color)

        self.w_content.contents['footer'] = w_labels

    def _updateState(self):
        parts = [
            '🔄' if self.note.dirty else '  ',
            '📦' if self.note.archived else '  ',
            '📍' if self.note.pinned else '  ',
        ]
        self.w_state.set_text(''.join(parts))

    def _updateMode(self):
        self.original_widget = self.w_content.contents['body'][0] \
            if self.zen_mode \
            else self.w_frame
        self._invalidate()

    def _save(self):
        title = self.w_title.get_edit_text()
        if self.note.title != title:
            self.note.title = title

        if not isinstance(self.note, gkeepapi.node.List):
            text = self.w_text.get_edit_text()
            if self.note.text != text:
                self.note.text = text
            return

        old_items = set((item.id for item in self.note.items))

        for i, w_item in enumerate(self.w_list.body):
            item = gkeepapi.node.ListItem(id_=w_item.id, parent_id=self.note.id)
            if w_item.id in old_items:
                item = self.note.get(w_item.id)
                old_items.remove(w_item.id)

            if item.checked != w_item.checked:
                item.checked = w_item.checked
            text = w_item.getText()
            if item.text != text:
                item.text = text

            if item.new:
                self.note.append(item)

            curr = None
            prev = item.super_list_item_id
            if i > 0 and w_item.indented:
                curr = self.w_list.body[i - 1].id

            if prev != curr:
                if prev is not None:
                    self.note.get(prev).dedent(item)

                if curr is not None:
                    self.note.get(curr).indent(item)

        for id_ in old_items:
            self.note.get(id_).delete()

    def keypress(self, size, key):
        key = super(Edit, self).keypress(size, key)
        if key == 'f':
            self.note.pinned = not self.note.pinned
            self._updateState()
            key = None
        elif key == 'e':
            self.note.archived = not self.note.archived
            self._updateState()
            key = None
        elif key == 'meta z':
            self.zen_mode = not self.zen_mode
            self._updateMode()
            key = None
        elif key == 'ctrl c':
            self.application.pop()
            key = None
        elif key == 'esc':
            self._save()
            self.application.pop()
            key = None
        return key

    def refresh(self, keep: gkeepapi.Keep):
        pass
