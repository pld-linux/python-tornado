#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# tornado tests [use network]
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	tornado
Summary:	Web framework and asynchronous networking library
Summary(pl.UTF-8):	Szkielet WWW i asynchroniczna biblioteka sieciowa
Name:		python-%{module}
Version:	5.1.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/tornado/
Source0:	https://files.pythonhosted.org/packages/source/t/tornado/%{module}-%{version}.tar.gz
# Source0-md5:	a1ce4f392d30ff0ebcb255150d89b826
#Source0:	https://github.com/tornadoweb/tornado/archive/v%{version}.tar.gz
URL:		http://www.tornadoweb.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7.9
BuildRequires:	python-modules >= 1:2.7.9
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-backports-ssl_match_hostname
BuildRequires:	python-backports_abc >= 0.4
BuildRequires:	python-certifi
BuildRequires:	python-futures
BuildRequires:	python-singledispatch
# SO_REUSEPORT option
BuildRequires:	uname(release) >= 3.9
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
%if "%{py3_ver}" < "3.5"
BuildRequires:	python3-backports_abc >= 0.4
%endif
%if "%{py3_ver}" < "3.4"
BuildRequires:	python3-singledispatch
%endif
# SO_REUSEPORT option
BuildRequires:	uname(release) >= 3.9
%endif
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tornado is a Python web framework and asynchronous networking library,
originally developed at FriendFeed. By using non-blocking network I/O,
Tornado can scale to tens of thousands of open connections, making it
ideal for long polling, WebSockets, and other applications that
require a long-lived connection to each user.

%description -l pl.UTF-8
Tornado to szkielet WWW oraz asynchroniczna biblioteka sieciowa dla
Pythona, oryginalnie powstałe w FriendFeed. Dzięki użyciu
nieblokującego sieciowego we/wy, Tornado może się skalować do
dziesiątek tysięcy otwartych połączeń, co czyni go idealnym do
zastosowań z długim pobieraniem, WebSockets i innych wymagających
długotrwałego połączenia z każdym użytkownikiem.

%package -n python3-tornado
Summary:	Web framework and asynchronous networking library
Summary(pl.UTF-8):	Szkielet WWW i asynchroniczna biblioteka sieciowa
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-tornado
Tornado is a Python web framework and asynchronous networking library,
originally developed at FriendFeed. By using non-blocking network I/O,
Tornado can scale to tens of thousands of open connections, making it
ideal for long polling, WebSockets, and other applications that
require a long-lived connection to each user.

%description -n python3-tornado -l pl.UTF-8
Tornado to szkielet WWW oraz asynchroniczna biblioteka sieciowa dla
Pythona, oryginalnie powstałe w FriendFeed. Dzięki użyciu
nieblokującego sieciowego we/wy, Tornado może się skalować do
dziesiątek tysięcy otwartych połączeń, co czyni go idealnym do
zastosowań z długim pobieraniem, WebSockets i innych wymagających
długotrwałego połączenia z każdym użytkownikiem.

%package apidocs
Summary:	API documentation for Python tornado module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona tornado
Group:		Documentation

%description apidocs
API documentation for Python tornado module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona tornado.

%prep
%setup -q -n %{module}-%{version}

# non-Linux
%{__rm} tornado/platform/{kqueue,windows}.py

%build
%if %{with python2}
TORNADO_EXTENSION=1 \
%py_build

%if %{with tests}
cd build-2/lib*
%{__python} -m tornado.test.runtests
cd ../..
%endif
%endif

%if %{with python3}
TORNADO_EXTENSION=1 \
%py3_build

%if %{with tests}
cd build-3/lib*
%{__python3} -m tornado.test.runtests
cd ../..
%endif
%endif

%if %{with doc}
# drop -W from sphinx options to allow build without optional imports (e.g. twisted)
%{__make} -C docs sphinx \
	SPHINXOPTS="-n -d build/doctrees ."
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
# just tornado tests with their data
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/tornado/test
%endif

%if %{with python3}
%py3_install
# just tornado tests with their data
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/tornado/test
%endif

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py_sitedir}/tornado
%attr(755,root,root) %{py_sitedir}/tornado/speedups.so
%{py_sitedir}/tornado/*.py[co]
%{py_sitedir}/tornado/platform
%{py_sitedir}/tornado-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitedir}/tornado
%attr(755,root,root) %{py3_sitedir}/tornado/speedups.cpython-*.so
%{py3_sitedir}/tornado/*.py
%{py3_sitedir}/tornado/platform
%{py3_sitedir}/tornado/__pycache__
%{py3_sitedir}/tornado-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/*
%endif
