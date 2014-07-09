# TODO:
# - proper place for *.pri,
# - set ECM_MKSPECS_INSTALL_DIR in kde5-extra-cmake-modules
# - runtime Requires if any
# - dir /usr/include/KF5 not packaged
%define         _state          stable
%define		orgname		kdbusaddons

Summary:	Convenience classes for DBus
Name:		kde5-%{orgname}
Version:	5.0.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/frameworks/%{version}/%{orgname}-%{version}.tar.xz
# Source0-md5:	da8585a074b204ab2bcd3e7bc8f4ddef
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.2.0
BuildRequires:	Qt5DBus-devel >= 5.2.0
BuildRequires:	Qt5Gui-devel >= 5.3.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Widgets-devel >= 5.2.0
BuildRequires:	Qt5X11Extras-devel >= 5.2.0
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kde5-extra-cmake-modules >= 1.0.0
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDBusAddons provides convenience classes on top of QtDBus, as well as
an API to create KDED modules.

%package devel
Summary:	Header files for %{orgname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{orgname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{orgname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{orgname}.

%prep
%setup -q -n %{orgname}-%{version}

%build
install -d build
cd build
%cmake \
	-DECM_MKSPECS_INSTALL_DIR=%{_libdir}/qt5/mkspecs/modules \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{orgname}5_qt --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{orgname}5_qt.lang
%defattr(644,root,root,755)
%doc MAINTAINER README.md
%attr(755,root,root) %{_bindir}/kquitapp5
%attr(755,root,root) %ghost %{_libdir}/libKF5DBusAddons.so.5
%attr(755,root,root) %{_libdir}/libKF5DBusAddons.so.5.0.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KDBusAddons
%{_includedir}/KF5/kdbusaddons_version.h
%attr(755,root,root) %{_libdir}/libKF5DBusAddons.so
%{_libdir}/cmake/KF5DBusAddons
%{_libdir}/qt5/mkspecs/modules/qt_KDBusAddons.pri
