# Copyright 2009-2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# GNU Radio Companion is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# GNU Radio Companion is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

from __future__ import absolute_import
import os
import warnings


GR_IMPORT_ERROR_MESSAGE = """\
Cannot import gnuradio.

Is the model path environment variable set correctly?
    All OS: PYTHONPATH

Is the library path environment variable set correctly?
    Linux: LD_LIBRARY_PATH
    Windows: PATH
    MacOSX: DYLD_LIBRARY_PATH
"""


def die(error, message):
    msg = "{0}\n\n({1})".format(message, error)
    try:
        import gtk
        d = gtk.MessageDialog(
            type=gtk.MESSAGE_ERROR,
            buttons=gtk.BUTTONS_CLOSE,
            message_format=msg,
        )
        d.set_title(type(error).__name__)
        d.run()
        exit(1)
    except ImportError:
        exit(type(error).__name__ + '\n\n' + msg)


def check_gtk():
    try:
        warnings.filterwarnings("error")
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('PangoCairo', '1.0')

        from gi.repository import Gtk
        Gtk.init_check()
        warnings.filterwarnings("always")
    except Exception as err:
        die(err, "Failed to initialize GTK. If you are running over ssh, "
                 "did you enable X forwarding and start ssh with -X?")


def check_gnuradio_import():
    try:
        from gnuradio import gr
    except ImportError as err:
        die(err, GR_IMPORT_ERROR_MESSAGE)


def check_blocks_path():
    if 'GR_DONT_LOAD_PREFS' in os.environ and not os.environ.get('GRC_BLOCKS_PATH', ''):
        die(EnvironmentError("No block definitions available"),
            "Can't find block definitions. Use config.conf or GRC_BLOCKS_PATH.")


def do_all():
    check_gnuradio_import()
    check_gtk()
    check_blocks_path()
