# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

Name:           qc-usb-kmod
Version:        0.6.6
Release:        42%{?dist}.1
Summary:        qc-usb kernel modules

Group:          System Environment/Kernel
License:        GPLv2+
URL:            http://qce-ga.sourceforge.net/
Source0:        http://downloads.sourceforge.net/qce-ga/qc-usb-%{version}.tar.gz
Patch0:         qc-usb-0.6.6-2.6.24.patch
# from http://patch-tracking.debian.net/patch/series/view/qc-usb/0.6.6-6/kcompat-2.6.26.patch
Patch1:         qc-usb-0.6.6-2.6.26.patch
# this comes from mandriva package
Patch2:         qc-usb-0.6.6-2.6.27.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64
# ppc and ppc64 disabled by knurd on 20081003 as it is known to fail on 2.6.27: 
# https://bugzilla.redhat.com/show_bug.cgi?id=465486

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Logitech QuickCam video driver with V4L support


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

# go
%setup -q -c -T -a 0
%patch0 -p0 -b .2.6.24
%patch1 -p0 -b .2.6.26
%patch2 -p0 -b .2.6.27
for kernel_version in %{?kernel_versions}; do
    cp -a  qc-usb-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make -C "_kmod_build_${kernel_version%%___*}" LINUX_DIR="${kernel_version##*___}" %{?_smp_mflags} quickcam.ko
done


%install
rm -rf $RPM_BUILD_ROOT
for kernel_version in %{?kernel_versions}; do
    install -D -m 755 _kmod_build_${kernel_version%%___*}/quickcam.ko $RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/quickcam.ko
done

%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.6.6-42.1
- rebuild for latest rawhide kernel

* Wed Oct 15 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.6.6-42
- Add 2.6.27 patch

* Fri Oct 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.6.6-41.1
- rebuild for rpm fusion

* Wed Oct 01 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.6.6-40.1
- rebuild for new kernels

* Mon Sep 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.6.6-39.1
- add qc-usb-0.6.6-2.6.26.patch
- temporary disable ppc

* Sat Aug 16 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.6.6-37
- rebuild for new kernels

* Thu Jul 24 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-36
- rebuild for new Fedora kernels

* Tue Jul 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-35
- rebuild for new Fedora kernels

* Wed Jul 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-34
- rebuild for new Fedora kernels

* Fri Jun 13 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-33
- rebuild for new Fedora kernels

* Fri Jun 06 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-32
- rebuild for new Fedora kernels

* Thu May 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-31
- rebuild for new Fedora kernels

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-30
- build for f9

* Sat Feb 16 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-23
- fix typo

* Sun Feb 10 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.6.6-22
- Patch for 2.6.24

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-21
- rebuild for new kmodtools, akmod adjustments

* Sun Jan 20 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-20
- build akmods package

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-5
- rebuilt for 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Tue Dec 04 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.6.6-4
- Convert to kmod2

* Tue Dec 04 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.6.6-3
- Add ExclusiveArch and description

* Sun Dec 02 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.6.6-2
- Rename from kmod-qc-usb to qc-usb-kmod

* Sat Dec 01 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.6.6-1
- Version bump
- Enable non-x86 builds

* Mon Sep 17 2007 Lubomir Kundrak <lkundrak@redhat.com> 0.6.5-1
- Initial package
