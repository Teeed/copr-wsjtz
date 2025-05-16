#global rctag rc8

Name:		wsjtz
Version:	2.7.0_1.48
Release:	1%{?dist}
Summary:	Weak Signal communication by K1JT (WSJTZ version)

License:	GPL-3.0-or-later

URL:		https://sourceforge.net/projects/wsjt-z/
Source0:    https://sourceforge.net/projects/wsjt-z/files/Source/wsjtz-2.7.0-rc7-1.48.zip

ExcludeArch:    i686

BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	tar
BuildRequires:	gcc-c++
BuildRequires:	gcc-gfortran

BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-linguist
BuildRequires:	qt5-qtserialport-devel
BuildRequires:	qt5-qtmultimedia-devel
BuildRequires:	desktop-file-utils
BuildRequires:	hamlib-devel
BuildRequires:	fftw-devel
BuildRequires:	libusbx-devel
BuildRequires:	systemd-devel
BuildRequires:	boost-devel
BuildRequires:	portaudio-devel

BuildRequires:	asciidoc
BuildRequires:	rubygem-asciidoctor
BuildRequires:	libappstream-glib

Conflicts: wsjtx

%description
WSJT-X is a computer program designed to facilitate basic amateur radio
communication using very weak signals. It implements communication protocols
or "modes" called JT4, JT9, JT65, QRA64, ISCAT, MSK144, and WSPR, as well as
one called Echo for detecting and measuring your own radio signals reflected
from the Moon.


%prep
%setup -n wsjtx
#{?rctag:-%{rctag}}


# Extract wsjtx source and clean up
find ./ -type f -exec chmod -x {} \;

ls -al


# convert CR + LF to LF
dos2unix *.ui *.iss *.txt


%build
# The fortran code in this package is not type safe and will thus not work
# with LTO.  Additionally there are numerous bogus strncat calls that also
# need to be fixed for this package to work with LTO
%define _lto_cflags %{nil}

# Workaround for build with gcc-10, problem reported upstream
export CFLAGS="%{optflags} -fcommon"
export LDFLAGS="%{?__global_ldflags}"
# workaround for hamlib check, i.e. for hamlib_LIBRARY_DIRS not to be empty
export PKG_CONFIG_ALLOW_SYSTEM_LIBS=1

%cmake -Dhamlib_STATIC=FALSE \
       -DBoost_NO_SYSTEM_PATHS=FALSE

%cmake_build


%install
%cmake_install

dos2unix %{buildroot}%{_datadir}/applications/message_aggregator.desktop

# Make sure the right style is used.
desktop-file-edit --set-key=Exec --set-value="wsjtx --style=fusion" \
    %{buildroot}/%{_datadir}/applications/wsjtx.desktop
# desktop files
desktop-file-validate %{buildroot}%{_datadir}/applications/wsjtx.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/message_aggregator.desktop
# 

# fix docs
install -p -m 0644 -t %{buildroot}%{_datadir}/doc/wsjtx GUIcontrols.txt jt9.txt \
  v1.7_Features.txt wsjtx_changelog.txt

# drop wsjtx hamlib bins
rm -f %{buildroot}%{_bindir}/rigctl*-wsjtx


%files
%license COPYING
%doc %{_datadir}/doc/wsjtx
%{_bindir}/cablog
%{_bindir}/echosim
%{_bindir}/fcal
%{_bindir}/fmeasure
%{_bindir}/fmtave
%{_bindir}/fst4sim
%{_bindir}/hash22calc
%{_bindir}/jt4code
%{_bindir}/jt65code
%{_bindir}/jt9
%{_bindir}/jt9code
%{_bindir}/ft8code
%{_bindir}/message_aggregator
%{_bindir}/msk144code
%{_bindir}/q65sim
%{_bindir}/q65code
%{_bindir}/udp_daemon
%{_bindir}/wsjtx
%{_bindir}/wsjtx_app_version
%{_bindir}/wsprd
%{?fedora:%{_mandir}/man1/*.1.gz}
%{_datadir}/applications/wsjtx.desktop
%{_datadir}/applications/message_aggregator.desktop
%{_datadir}/pixmaps/wsjtx_icon.png
%{_datadir}/wsjtx


%changelog
* Fri May 16 2025 Tadeusz Magura-Witkowski <tadeuszmw@gmail.com> 2.7.0_1.48-1
- new package built with tito

* Fri May 16 2025 Tadeusz Magura-Witkowski <tadeuszmw@gmail.com> - 2.7.0_1.48-1
- Initial version, based on https://src.fedoraproject.org/rpms/wsjtx (a506bea2c1012741e27d171e7400387930b98469)


