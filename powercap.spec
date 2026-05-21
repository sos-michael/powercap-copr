%global commit  REPLACED_AT_SRPM_TIME
%global cdate   REPLACED_AT_SRPM_TIME
%global shortc  %(c=%{commit}; echo ${c:0:7})

Name:           powercap
Version:        0.6.1
Release:        0.%{cdate}git%{shortc}%{?dist}
Summary:        C bindings to the Linux Power Capping Framework in sysfs
License:        BSD-3-Clause
URL:            https://github.com/powercap/powercap
Source0:        %{url}/archive/%{commit}/%{name}-%{shortc}.tar.gz

BuildRequires:  gcc
BuildRequires:  cmake >= 3.12
BuildRequires:  make

%description
A generic C interface to the Linux power capping framework (sysfs),
introduced in Linux 3.13. Ships libpowercap plus two utilities:
powercap-info (inspect control-type hierarchies and zone/constraint
state) and powercap-set (toggle zones, set power limits and time
windows). The library also exposes a powercap-rapl API for managing
Intel RAPL (Running Average Power Limit).

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

%files
%license LICENSE
%doc README.md AUTHORS RELEASES.md
%{_bindir}/powercap-info
%{_bindir}/powercap-set
%{_libdir}/libpowercap.so.0
%{_libdir}/libpowercap.so.%{version}
%{_mandir}/man1/powercap-info.1*
%{_mandir}/man1/powercap-set.1*
%{_mandir}/man3/*.3*

%files devel
%{_includedir}/%{name}/
%{_libdir}/libpowercap.so
%{_libdir}/pkgconfig/powercap.pc
%{_libdir}/cmake/powercap/

%changelog
* Wed May 20 2026 sos-michael <noreply@example.com> - 0.6.1-0
- Initial snapshot packaging of github.com/powercap/powercap master.
