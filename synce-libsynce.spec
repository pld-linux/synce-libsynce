#
# Conditional build:
%bcond_with	dbus	# build with dbus support
#
Summary:	Core SynCE library
Summary(pl.UTF-8):	Podstawowa biblioteka SynCE
Name:		synce-libsynce
Version:	0.10.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://dl.sourceforge.net/synce/%{name}-%{version}.tar.gz
# Source0-md5:	e46c72219bff559f4bb1615613671942
Patch0:		%{name}-nolibs.patch
URL:		http://www.synce.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.4
# not sure which was OK, but doesn't build with 0.61
%{?with_dbus:BuildRequires:	dbus-devel < 0.35}
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
	%{?with_dbus:--enable-dbus}

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
%doc README TODO
%attr(755,root,root) %{_libdir}/libsynce.so.*.*.*
%{_mandir}/man1/synce.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsynce.so
%{_libdir}/libsynce.la
%{_includedir}/synce*.h
%{_pkgconfigdir}/libsynce.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsynce.a
