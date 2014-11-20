# TODO:
# - runtime Requires if any
# - dir /usr/include/KF5 not packaged

%bcond_without	tests

%define		_state		stable
%define		orgname		kdbusaddons
%define		kdeframever	5.4
%define		qt_ver		5.3.2

Summary:	Convenience classes for DBus
Name:		kf5-%{orgname}
Version:	5.4.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/%{_state}/frameworks/%{kdeframever}/%{orgname}-%{version}.tar.xz
# Source0-md5:	33f64aeabee19b22a3d8cc3411342eca
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5DBus-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Test-devel >= %{qt_ver}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
BuildRequires:	Qt5X11Extras-devel >= %{qt_ver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	qt5-linguist >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

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
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%{__make}

%{?with_tests:%{__make} test}

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
%attr(755,root,root) %{_libdir}/libKF5DBusAddons.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KDBusAddons
%{_includedir}/KF5/kdbusaddons_version.h
%attr(755,root,root) %{_libdir}/libKF5DBusAddons.so
%{_libdir}/cmake/KF5DBusAddons
%{qt5dir}/mkspecs/modules/qt_KDBusAddons.pri
