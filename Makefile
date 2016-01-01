# The Qubes OS Project, http://www.qubes-os.org
#
# Copyright (C) 2015 Jason Mehring <nrgaway@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

all:
	@true

install:
	install -D -m 0644 files/canadapop-internal-r3.repo $(DESTDIR)/etc/yum.repos.d/canadapop-internal-r3.repo
	install -D -m 0644 files/canadapop-r3.repo $(DESTDIR)/etc/yum.repos.d/canadapop-r3.repo
	install -d -m 755 $(DESTDIR)/etc/pki/rpm-gpg
	install -m 644 files/RPM-GPG-KEY-canadapop* $(DESTDIR)/etc/pki/rpm-gpg/
