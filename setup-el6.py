#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# This file is part of PYAP.
# Copyright 2016 fccagou <fccagou@gmail.com>
#
# PYAP is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PYAP is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyap. If not, see <http://www.gnu.org/licenses/>.

from distutils.core  import setup
setup(name='pyap',
        version='0.4.4-rc1',
        description='PYthon Alert Processor',
        url='http://github.com/fccagou/pyap',
        author='fccagou',
        author_email='fccagou@gmail.com',
        license='GPLv3+',
        long_description="PYthon Alert Processor (or P..... Y'A Personne) is a little tool used to process alert sent by differents ways.",
        scripts=[
            'bin/pyap'
            ],
        packages=[
            'pyap',
            'blink1',
            'usb',
            'db9'
            ],
        package_data= {
            'usb': [
                'backend/__init__.py',
                'backend/libusb0.py',
                'backend/libusb1.py',
                'backend/openusb.py',
                ]
            },
        data_files=[
            ('share/doc/pyap',[
                'doc/README.md',
                'doc/LICENSE.md',
                'doc/LICENSE-EXTERNAL.md',
                'data/nagios2json.php',
                'data/pyap.sysconfig',
                'data/51-blink1.rules',
                'tests/test.conf'
                ]
            ),
            ('share/doc/pyap/samples/status',[
                'tests/status/n1',
                'tests/status/n2',
                ]
            ),
            ('/etc/pyap', ['']),
            ('/etc/init.d',['data/etc/init.d/pyap']),
            ],
    )
