%global commit  REPLACED_AT_SRPM_TIME
%global cdate   REPLACED_AT_SRPM_TIME
%global shortc  REPLACED_AT_SRPM_TIME
%global upstream_version REPLACED_AT_SRPM_TIME

Name:           powercap
Version:        %{upstream_version}^%{cdate}git%{shortc}
Release:        1%{?dist}
Summary:        C bindings to the Linux Power Capping Framework in sysfs
License:        BSD-3-Clause
URL:            https://github.com/powercap/powercap
Source0:        %{name}-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  cmake >= 3.12
BuildRequires:  make

%description
A generic C interface to the Linux power capping framework (sysfs),
introduced in Linux 3.13. Ships libpowercap and the utilities
powercap-info (inspect control-type hierarchies and zone/constraint
state) and powercap-set (toggle zones, set power limits and time
windows), plus rapl-info and rapl-set for Intel RAPL (Running Average
Power Limit). The library also exposes a powercap-rapl API.

Snapshot of upstream master at %{shortc} (%{cdate}).

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Headers, pkg-config metadata, and CMake package config files for
building against libpowercap.

%prep
%autosetup -n %{name}-%{commit}

%build
%cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%ldconfig_scriptlets

%check
%ctest

%files
%license LICENSE
%doc README.md AUTHORS RELEASES.md
%{_bindir}/powercap-info
%{_bindir}/powercap-set
%{_bindir}/rapl-info
%{_bindir}/rapl-set
%{_libdir}/libpowercap.so.*
%{_mandir}/man1/powercap-info.1*
%{_mandir}/man1/powercap-set.1*
%{_mandir}/man1/rapl-info.1*
%{_mandir}/man1/rapl-set.1*

%files devel
%{_includedir}/%{name}/
%{_libdir}/libpowercap.so
%{_libdir}/pkgconfig/powercap.pc
%{_libdir}/cmake/powercap/
