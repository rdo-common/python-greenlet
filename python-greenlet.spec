%global         modname greenlet
%global         with_python3 1

Name:           python-%{modname}
Version:        0.4.11
Release:        3%{?dist}
Summary:        Lightweight in-process concurrent programming
Group:          Development/Libraries
License:        MIT
URL:            http://pypi.python.org/pypi/%{modname}
Source0:        https://github.com/python-greenlet/greenlet/archive/%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python-tools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

%description
The greenlet package is a spin-off of Stackless, a version of CPython
that supports micro-threads called "tasklets". Tasklets run
pseudo-concurrently (typically in a single or a few OS-level threads)
and are synchronized with data exchanges on "channels".

%package -n     python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
Group:          Development/Libraries

%description -n python2-%{modname}
The greenlet package is a spin-off of Stackless, a version of CPython
that supports micro-threads called "tasklets". Tasklets run
pseudo-concurrently (typically in a single or a few OS-level threads)
and are synchronized with data exchanges on "channels".

This is the Python 2 version of greenlet.

%package -n     python2-%{modname}-devel
Summary:        C development headers for python2-greenlet
%{?python_provide:%python_provide python2-%{modname}-devel}
Group:          Development/Libraries
Requires:       python2-%{modname} = %{version}-%{release}

%description -n python2-%{modname}-devel
This package contains header files required for C modules development.

%if 0%{?with_python3}
%package -n     python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
Group:          Development/Libraries

%description -n python3-%{modname}
The greenlet package is a spin-off of Stackless, a version of CPython
that supports micro-threads called "tasklets". Tasklets run
pseudo-concurrently (typically in a single or a few OS-level threads)
and are synchronized with data exchanges on "channels".

This is the Python 3 version of greenlet.

%package -n     python3-greenlet-devel
Summary:        C development headers for python3-greenlet
%{?python_provide:%python_provide python3-%{modname}-devel}
Group:          Development/Libraries
Requires:       python3-%{modname} = %{version}-%{release}

%description -n python3-%{modname}-devel
This package contains header files required for C modules development.

%endif # if with_python3

%prep
%setup -q -n greenlet-%{version}
chmod 644 benchmarks/*.py
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # if with_python3

%build
%py2_build

%if 0%{?with_python3}
pushd %{py3dir}
  %py3_build
popd
%endif # if with_python3

%install
# Install python 3 first, so that python 2 gets precedence:
%if 0%{?with_python3}
pushd %{py3dir}
  %py3_install
popd
%endif # if with_python3
%py2_install
 
%check
# Run the upstream test suite and benchmarking suite to further exercise the code
%{__python2} setup.py test
PYTHONPATH=$(pwd) %{__python2} benchmarks/chain.py
%if 0%{?with_python3}
PYTHONPATH=
pushd %{py3dir}
%{__python3} setup.py test || :
2to3 -w --no-diffs -n  benchmarks/chain.py
PYTHONPATH=$(pwd) %{__python3} benchmarks/chain.py
%endif # if with_python3

%files -n python2-%{modname}
%license LICENSE LICENSE.PSF
%doc AUTHORS NEWS README.rst
%doc doc/greenlet.txt benchmarks
%{python_sitearch}/greenlet.so
%{python_sitearch}/greenlet*.egg-info

%files -n python2-%{modname}-devel
%license LICENSE LICENSE.PSF
%doc AUTHORS NEWS README.rst
%{_includedir}/python2*/greenlet

%if 0%{?with_python3}
%files -n python3-greenlet
%license LICENSE LICENSE.PSF
%doc AUTHORS NEWS README.rst
%doc doc/greenlet.txt benchmarks
%{python3_sitearch}/greenlet.cpython-*.so
%{python3_sitearch}/greenlet*.egg-info

%files -n python3-greenlet-devel
%license LICENSE LICENSE.PSF
%doc AUTHORS NEWS README.rst
%{_includedir}/python3*/greenlet
%endif # if with_python3

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.11-2
- Rebuild for Python 3.6

* Sun Dec 11 2016 Kevin Fenzi <kevin@scrye.com> - 0.4.11-1
- Update to 0.4.11. Fixes bug #1403514

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Oct 25 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.9-1
- Update to 0.4.9
- Use %license macro
- Follow new RPM Packaging guidelines
- Cleanups in spec

* Fri Aug 21 2015 Kevin Fenzi <kevin@scrye.com> 0.4.7-2
- Re-enable tests on secondary arches. Fixes #1252899
- Applied patch to build on ppc64le. Fixes #1252900

* Fri Jun 26 2015 Kevin Fenzi <kevin@scrye.com> 0.4.7-1
- Update to 0.4.7. Fixes bug #1235896

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 29 2015 Terje Røsten <terje.rosten@ntnu.no> - 0.4.5-1
- 0.4.5
- Add python3 subpackage
- Ship license files
- Some spec clean ups
- Update fixes FTBFS issue (bz#1106779)
- Add comment about issues on ppc64, s390 & s390x

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Orion Poplawski <orion@cora.nwra.com> 0.4.2-1
- Update to 0.4.2

* Mon Aug 05 2013 Kevin Fenzi <kevin@scrye.com> 0.4.1-1
- Update to 0.4.1
- Fix FTBFS bug #993134

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Pádraig Brady <P@draigBrady.com> - 0.4.0-1
- Update to 0.4.0

* Thu Oct 11 2012 Pádraig Brady <P@draigBrady.com> - 0.3.1-11
- Add support for ppc64

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Dan Horák <dan[at]danny.cz> - 0.3.1-8
- disable tests also for s390(x)

* Thu Nov 17 2011 Pádraig Brady <P@draigBrady.com> - 0.3.1-7
- Fix %%check quoting in the previous comment which when
  left with a single percent sign, pulled in "unset DISPLAY\n"
  into the changelog

* Mon Oct 24 2011 Pádraig Brady <P@draigBrady.com> - 0.3.1-6
- cherrypick 25bf29f4d3b7 from upstream (rhbz#746771)
- exclude the %%check from ppc where the tests segfault

* Wed Oct 19 2011 David Malcolm <dmalcolm@redhat.com> - 0.3.1-5
- add a %%check section
- cherrypick 2d5b17472757 from upstream (rhbz#746771)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr 14 2010 Lev Shamardin <shamardin@gmail.com> - 0.3.1-2
- Splitted headers into a -devel package.

* Fri Apr 09 2010 Lev Shamardin <shamardin@gmail.com> - 0.3.1-1
- Initial package version.
