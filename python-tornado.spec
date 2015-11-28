#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python3 # CPython 3.x module

%define		module	tornado
Summary:	Web framework and asynchronous networking library
Name:		python-%{module}
Version:	3.1.1
Release:	4
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/t/tornado/%{module}-%{version}.tar.gz
# Source0-md5:	901e4f24b9e840860f6095451aa75828
URL:		http://www.tornadoweb.org/
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
Requires:	ca-certificates
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tornado is a Python web framework and asynchronous networking library,
originally developed at FriendFeed. By using non-blocking network I/O,
Tornado can scale to tens of thousands of open connections, making it
ideal for long polling, WebSockets, and other applications that
require a long-lived connection to each user.

%package -n python3-tornado
Summary:	Web framework and asynchronous networking library
Group:		Libraries/Python
Requires:	ca-certificates
Requires:	python3-modules

%description -n python3-tornado
Tornado is a Python web framework and asynchronous networking library,
originally developed at FriendFeed. By using non-blocking network I/O,
Tornado can scale to tens of thousands of open connections, making it
ideal for long polling, WebSockets, and other applications that
require a long-lived connection to each user.

%prep
%setup -q -n %{module}-%{version}

# fix #!/usr/bin/env python -> #!/usr/bin/python:
#%{__sed} -i -e '1s,^#!.*python,#!%{__python},' %{name}.py

%build
%py_build

%if %{with tests}
cd build-2/lib
%{__python} -m tornado.test.runtests
cd ../..
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%if %{with tests}
cd build-3/lib
%{__python3} -m tornado.test.runtests
cd ../..
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/ca-certificates.crt
ln -sf /etc/certs/ca-certificates.crt $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/ca-certificates.crt

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/ca-certificates.crt
ln -sf /etc/certs/ca-certificates.crt $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/ca-certificates.crt
%endif

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/%{module}/ca-certificates.crt
%{py_sitescriptdir}/%{module}/platform
%{py_sitescriptdir}/%{module}/test
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/ca-certificates.crt
%{py3_sitescriptdir}/%{module}/platform
%{py3_sitescriptdir}/%{module}/test
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
