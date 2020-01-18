%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global svnrev  625
%global revdate 20130827

Name:           pywbem 
Version:        0.7.0
Release:        16.%{revdate}svn%{svnrev}%{?dist}
Summary:        Python WBEM Client and Provider Interface
Group:          Development/Libraries
License:        LGPLv2
URL:            http://pywbem.sourceforge.net
# The source for this package was pulled from upstream svn repository.
# Use the following commands to get the archive:
#  svn export -r 613 svn://svn.code.sf.net/p/pywbem/code/pywbem/trunk pywbem-20130128
#  tar -cJvf pywbem-20130128.tar.xz pywbem-20130128
Source0:        %{name}-%{revdate}.tar.xz
BuildRequires:  python-setuptools-devel 
BuildArch:      noarch

# fix module imports in /usr/bin/mofcomp
Patch0:         pywbem-20130411-mof_compiler-import.patch
# Remove python-twisted module, we don't want twisted in RHEL
Patch1:         pywbem-remove-twisted.patch
# Use system python, in case someone has enabled software collection
# See bug #987039
Patch2:         pywbem-20130723-shebang.patch

%description
A Python library for making CIM (Common Information Model) operations over HTTP 
using the WBEM CIM-XML protocol. It is based on the idea that a good WBEM 
client should be easy to use and not necessarily require a large amount of 
programming knowledge. It is suitable for a large range of tasks from simply 
poking around to writing web and GUI applications. 

WBEM, or Web Based Enterprise Management is a manageability protocol, like 
SNMP, standardised by the Distributed Management Task Force (DMTF) available 
at http://www.dmtf.org/standards/wbem.

It also provides a Python provider interface, and is the fastest and 
easiest way to write providers on the planet.

%prep
%setup -q -n %{name}-%{revdate}
%patch0 -p1 -b .mofcomp-imports
%patch1 -p1
%patch2 -p1 -b .shebang

%build
# dirty workaround to fix the mof_compiler.py module path
ln -s . pywbem
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p -m755 %{buildroot}%{_bindir}
mv %{buildroot}/%{python_sitelib}/%{name}/wbemcli.py %{buildroot}/%{_bindir}/pywbemcli
mv %{buildroot}/%{python_sitelib}/%{name}/mof_compiler.py %{buildroot}/%{_bindir}/mofcomp
rm %{buildroot}/%{python_sitelib}/%{name}/wbemcli.py[co]
rm %{buildroot}/%{python_sitelib}/%{name}/mof_compiler.py[co]

%clean 
rm -rf %{buildroot}

%files
%{python_sitelib}/*
%attr(755,root,root) %{_bindir}/mofcomp
%attr(755,root,root) %{_bindir}/pywbemcli
%doc README

%changelog
* Tue Aug 27 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-16.20130827svn625
- Fixed parsing of ipv6 addresses.

* Thu Aug 15 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-15.20130723svn623
- Fixed /usr/bin/mofcomp shebang to use system python (rhbz#987039).

* Tue Aug 13 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-14.20130723svn623
- Fixed certificate verification issue.

* Tue Jul 23 2013  <jsafrane@redhat.com> 0.7.0-13.20130723svn623
- Fixed checking of CIMVERSION in CIM-XML.

* Tue Jul 16 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-12.20130702svn622
- Removed dependency on python-twisted.

* Tue Jul  2 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-11.20130702svn622
- New upstream version.
- Method parameters are now case-insensitive.

* Fri May 24 2013 Tomas Bzatek <tbzatek@redhat.com> 0.7.0-10.20130411svn619
- Fix module imports in /usr/bin/mofcomp

* Thu Apr 11 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-9.20130411svn619
- New upstream version.
- Removed debug 'print' statements.

* Mon Jan 28 2013 Michal Minar <miminar@redhat.com> 0.7.0-8.20130128svn613
- New upstream version.
- Added post-release snapshot version info.
- Removed obsoleted BuildRoot,

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jan 01 2010 David Nalley <david@gnsa.us> 0.7.0-3
- refined requires for epel compat
* Sun Jun 28 2009 David Nalley <david@gnsa.us> 0.7.0-2
- Added some verbiage regarding what WBEM is and expanding WBEM and CIM acronyms
- Added python-twisted as a dependency
* Thu Jun 25 2009 David Nalley <david@gnsa.us> 0.7.0-1
- Initial packaging

