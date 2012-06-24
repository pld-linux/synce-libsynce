#
# Conditional build:
%bcond_with	dbus	# build with dbus support
#
Summary:	Core SynCE library
Summary(pl):	Podstawowa biblioteka SynCE
Name:		synce-libsynce
Version:	0.9.3
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://dl.sourceforge.net/synce/%{name}-%{version}.tar.gz
# Source0-md5:	9b793d1ef241fa7fca6ca7832b3b4811
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

%description -l pl
Biblioteka libsynce to cz�� projektu SynCE. Jest wymagana dla (co
najmniej) nast�puj�cych cz�ci projektu: librapi2, dccmd.

%package devel
Summary:	Header files for libsynce library
Summary(pl):	Pliki nag��wkowe biblioteki libsynce
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_dbus:Requires:	dbus-devel}

%description devel
Header files for libsynce library.

%description devel -l pl
Pliki nag��wkowe biblioteki libsynce.

%package static
Summary:	Static libsynce library
Summary(pl):	Statyczna biblioteka libsynce
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libsynce library.

%description static -l pl
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
