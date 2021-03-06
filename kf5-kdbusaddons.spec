#
# Conditional build:
%bcond_with	tests		# build without tests

# TODO:
# - runtime Requires if any
# - make test not hanging and switch it back on

%define		kdeframever	5.79
%define		qtver		5.9.0
%define		kfname		kdbusaddons
Summary:	Convenience classes for DBus
Name:		kf5-%{kfname}
Version:	5.79.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	94f13ec26cc751662ed00a2184a3a3f7
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KDBusAddons provides convenience classes on top of QtDBus, as well as
an API to create KDED modules.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5DBus-devel >= %{qtver}
Requires:	cmake >= 2.6.0

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%{?with_tests:%ninja_build test}

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc MAINTAINER README.md
%attr(755,root,root) %{_bindir}/kquitapp5
%attr(755,root,root) %{_libdir}/libKF5DBusAddons.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5DBusAddons.so.5
%{_datadir}/qlogging-categories5/kdbusaddons.categories
%{_datadir}/qlogging-categories5/kdbusaddons.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KDBusAddons
%{_includedir}/KF5/kdbusaddons_version.h
%attr(755,root,root) %{_libdir}/libKF5DBusAddons.so
%{_libdir}/cmake/KF5DBusAddons
%{qt5dir}/mkspecs/modules/qt_KDBusAddons.pri
