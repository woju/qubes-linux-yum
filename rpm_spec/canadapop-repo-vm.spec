#
# The Qubes OS Project, http://www.qubes-os.org
#
# Copyright (C) 2015  Jason Mehring <nrgaway@gmail.com>
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

%{!?version: %define version %(cat version)}

Name:      qubes-canadapop-repo-vm
Version:   %{version}
Release:   1%{?dist}
Summary:   Qubes Canadapop repo for VM
License:   GPL 2.0
URL:       http://www.canadapop.com/

Vendor:	   Canadapop.com
Group:	   Qubes
BuildArch: noarch

%define _builddir %(pwd)

%description
Qubes Canadapop repo installation for VM.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build

%install
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
/etc/pki/rpm-gpg/RPM-GPG-KEY-canadapop*
%config(noreplace) /etc/yum.repos.d/canadapop-r3.repo
%config(noreplace) /etc/yum.repos.d/canadapop-internal-r3.repo
