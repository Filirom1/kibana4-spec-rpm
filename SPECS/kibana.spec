Name:     kibana
Version:  4.3.1
Release:  1%{?dist}
Summary:  Explore & Visualize Your Data
Group:    Applications/Internet
License:  ASL 2.0
URL:      https://www.elastic.co/products/%{name}
Source0:  https://download.elasticsearch.org/%{name}/%{name}/%{name}-%{version}-linux-x64.tar.gz
Source1:  kibana-sysconfig
Source2:  kibana-logrotate
Source3:  kibana.service

%define debug_package %{nil}

%description
Explore & Visualize Your Data

%prep
%setup -q -n %{name}-%{version}-linux-x64
ln -s `pwd`/src src/server

%build
true

%install
rm -rf $RPM_BUILD_ROOT

# config
%{__mkdir} -p %{buildroot}%{_sysconfdir}/kibana
%{__install} -m 644 config/kibana.yml %{buildroot}%{_sysconfdir}/%{name}

# sysconfig
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/kibana

# logs
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/kibana

# systemd
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/kibana.service

# sources
%{__mkdir} -p %{buildroot}%{_datadir}/%{name}
%{__cp} -r {LICENSE.txt,README.txt,bin,installedPlugins,node,node_modules,optimize,package.json,src,webpackShims} %{buildroot}%{_datadir}/%{name}/

%files
%defattr(-,root,root,-)
%dir %config(noreplace) "/etc/sysconfig"
%config(noreplace) "/etc/sysconfig/kibana"

%dir %config(noreplace) "/etc/kibana"
%config(noreplace) "/etc/kibana/kibana.yml"

%config(noreplace) "/etc/logrotate.d/kibana"

%{_unitdir}/kibana.service

%dir %attr(0755, kibana, kibana) "/var/log/kibana"

%ghost "/var/run/kibana.pid"

%doc "/usr/share/kibana/LICENSE.txt"
%doc "/usr/share/kibana/README.txt"

"/usr/share/kibana/src"
"/usr/share/kibana/bin"
"/usr/share/kibana/installedPlugins"
"/usr/share/kibana/node"
"/usr/share/kibana/node_modules"
"/usr/share/kibana/optimize"
"/usr/share/kibana/package.json"
"/usr/share/kibana/webpackShims"

%attr(775,-,kibana) "/usr/share/kibana/optimize"


%pre -p /bin/sh
getent group kibana >/dev/null || groupadd -r kibana
getent passwd kibana >/dev/null || \
    useradd -r -g kibana -d /usr/share/kibana -s /sbin/nologin \
    -c "kibana user" kibana

%post -p /bin/sh

[ -f /etc/sysconfig/kibana ] && . /etc/sysconfig/kibana
/bin/systemctl start kibana.service


%postun -p /bin/sh
# only execute in case of package removal, not on upgrade
if [ $1 -eq 0 ] ; then

    getent passwd kibana > /dev/null
    if [ "$?" == "0" ] ; then
        userdel kibana
    fi

    getent group kibana >/dev/null
    if [ "$?" == "0" ] ; then
        groupdel kibana
    fi
fi

exit


%changelog
* Mon Nov 16 2015 Romain Philibert <romain.philibert@worldline.com> 4.2.0-1
- Update Kibana to version 4.2.0
* Thu Apr 14 2015 Romain Philibert <romain.philibert@worldline.com> 4.1.0-1
- bump version
* Thu Apr 14 2015 Romain Philibert <romain.philibert@worldline.com> 4.0.2-1
- bump version
* Thu Mar 26 2015 Romain Philibert <romain.philibert@worldline.com> 4.0.1-1
- new package for kibana4
