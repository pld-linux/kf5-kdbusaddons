#
# Conditional build:
%bcond_with	tests		# build without tests

# TODO:
# - runtime Requires if any
# - make test not hanging and switch it back on

%define		kdeframever	5.93
%define		qtver		5.15.2
%define		kfname		kdbusaddons
Summary:	Convenience classes for DBus
Name:		kf5-%{kfname}
Version:	5.93.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	9532d36f03bd366a217c36e8743ad53e
URL:		http://www.kde.org/
BuildRequires:	Qt5DBus-devel >= %{qtver}
%{?with_tests:BuildRequires:	Qt5Test-devel >= %{qtver}}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt5DBus >= %{qtver}
Requires:	Qt5X11Extras >= %{qtver}
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
Requires:	cmake >= 3.16

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
	%{!?with_tests:-DBUILD_TESTING=OFF} \
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
%ghost %{_libdir}/libKF5DBusAddons.so.5
%{_datadir}/qlogging-categories5/kdbusaddons.categories
%{_datadir}/qlogging-categories5/kdbusaddons.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KDBusAddons
%{_libdir}/libKF5DBusAddons.so
%{_libdir}/cmake/KF5DBusAddons
%{qt5dir}/mkspecs/modules/qt_KDBusAddons.pri
