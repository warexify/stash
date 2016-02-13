# coding: utf-8
"""
Centralize handlers for various user actions.
"""
class ShNullResponder(object):

    def handle(self, *args, **kwargs):
        pass

    def __getattribute__(self, item):
        return object.__getattribute__(self, 'handle')

    def __getitem__(self, item):
        return object.__getattribute__(self, 'handle')


# noinspection PyAttributeOutsideInit,PyDocstring
class ShUserActionProxy(object):
    """
    The purpose of this object is to be a centralized place to respond
    to any user actions trigger from the UI including typing, touching,
    tap, etc. A centralized object makes it easier to be substituted by
    other user-defined object for command script, e.g. ssh.

    :param StaSh stash:
    """

    def __init__(self, stash):
        self.stash = stash
        self.null_responder = ShNullResponder()
        self.reset()

        # TextView delegate
        class _TVDelegate(object):
            @staticmethod
            def textview_did_begin_editing(sender):
                self.tv_responder.textview_did_begin_editing(sender)

            @staticmethod
            def textview_did_end_editing(sender):
                self.tv_responder.textview_did_end_editing(sender)

            @staticmethod
            def textview_should_change(sender, rng, replacement):
                return self.tv_responder.textview_should_change(sender, rng, replacement)

            @staticmethod
            def textview_did_change(sender):
                self.tv_responder.textview_did_change(sender)

            @staticmethod
            def textview_did_change_selection(sender):
                self.tv_responder.textview_did_change_selection(sender)

        # Virtual key row swipe gesture
        class _SVDelegate(object):
            @staticmethod
            def scrollview_did_scroll(sender):
                if self.sv_responder:
                    self.sv_responder.scrollview_did_scroll(sender)
                else:
                    sender.superview.scrollview_did_scroll(sender)

        self.tv_delegate = _TVDelegate()
        self.sv_delegate = _SVDelegate()

    # The properties are used for late binding as the various components
    # may not be ready when this class is initialized
    @property
    def vk_responder(self):
        return self._vk_responder or self.stash.ui

    @vk_responder.setter
    def vk_responder(self, value):
        self._vk_responder = value

    @property
    def tv_responder(self):
        return self._vk_responder or self.stash.terminal.tv_delegate

    @tv_responder.setter
    def tv_responder(self, value):
        self._tv_responder = value

    @property
    def kc_responder(self):
        return self._kc_responder or self.stash.terminal.kc_handlers

    @kc_responder.setter
    def kc_responder(self, value):
        self._kc_responder = value

    def reset(self):
        self._vk_responder = None
        self._tv_responder = None
        self.sv_responder = None
        self._kc_responder = None  # for keyCommands

    # --------------------- Proxy ---------------------
    # Buttons
    def vk_tapped(self, sender):
        self.vk_responder.vk_tapped(sender)

    # Keyboard shortcuts
    def kc_pressed(self, key, modifierFlags):
        self.kc_responder[(key, modifierFlags)]()
