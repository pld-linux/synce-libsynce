# TODO:
#	- descriptions and names for -connector-*
#	- check connector-dccm requirement
#
# Conditional build:
%bcond_without	dbus	# build without dbus support
%bcond_without	dccm	# build without dccm file support
%bcond_with	hal	# build without hal support
%bcond_without	odccm	# build without odccm support

%if %{without dbus}
%undefine with_odccm
%undefine with_hal
%endif
Summary:	Core SynCE library
Summary(pl.UTF-8):	Podstawowa biblioteka SynCE
Name:		synce-libsynce
Version:	0.15.1
Release:	2
License:	MIT
Group:		Libraries
Source0:	http://dl.sourceforge.net/synce/libsynce-%{version}.tar.gz
# Source0-md5:	eaddc88c5f0027e89c6f0fffec34def2
Patch0:		%{name}-nolibs.patch
URL:		http://www.synce.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.4
%{?with_dbus:BuildRequires:	dbus-glib-devel >= 0.60}
%{?with_hal:BuildRequires:	hal-devel >= 0.5.8}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libsynce is part of the SynCE project. It's required for (at least)
the following parts of the SynCE project: librapi2, dccmd.

%description -l pl.UTF-8
Biblioteka libsynce to część projektu SynCE. Jest wymagana dla (co
najmniej) następujących części projektu: librapi2, dccmd.

%package devel
Summary:	Header files for libsynce library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsynce
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_dbus:Requires:	dbus-devel}
%{?with_dbus:Requires:	dbus-glib-devel}

%description devel
Header files for libsynce library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libsynce.

%package static
Summary:	Static libsynce library
Summary(pl.UTF-8):	Statyczna biblioteka libsynce
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libsynce library.

%description static -l pl.UTF-8
Statyczna biblioteka libsynce.

%package -n synce-connector-hal
Summary:	Virtual package which provides connection to a WinCE device
Group:		Applications/System
Provides:	synce-connector
Requires:	%{name} = %{version}-%{release}
Requires:	synce-hal

%description -n synce-connector-hal
Virtual package which provides connection to a WinCE device.

%package -n synce-connector-odccm
Summary:	Virtual package which provides connection to a WinCE device
Group:		Applications/System
Provides:	synce-connector
Requires:	%{name} = %{version}-%{release}
Requires:	synce-odccm

%description -n synce-connector-odccm
Virtual package which provides connection to a WinCE device.

%package -n synce-connector-dccm
Summary:	Virtual package which provides connection to a WinCE device
Group:		Applications/System
Provides:	synce-connector
Requires:	%{name} = %{version}-%{release}
# check what is actually required
Requires:	synce-vdccm

%description -n synce-connector-dccm
Virtual package which provides connection to a WinCE device.

%prep
%setup -q -n libsynce-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_dccm: --disable-dccm-file-support} \
	%{!?with_hal: --disable-hal-support} \
	%{!?with_odccm: --disable-odccm-support}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README TODO
%attr(755,root,root) %{_libdir}/libsynce.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsynce.so.0
%{_mandir}/man7/synce.7*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsynce.so
%{_libdir}/libsynce.la
%{_includedir}/synce*.h
%{_pkgconfigdir}/libsynce.pc
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libsynce.a

%if %{with hal}
%files -n synce-connector-hal
%defattr(644,root,root,755)
%endif

%if %{with odccm}
%files -n synce-connector-odccm
%defattr(644,root,root,755)
%endif

%if %{with dccm}
%files -n synce-connector-dccm
%defattr(644,root,root,755)
%endif
