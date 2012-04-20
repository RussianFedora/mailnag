Name: mailnag
Version: 0.4
Release: 0.1.bdd7d5826f%{?dist}
Summary: A mail notification daemon for GNOME 3

Group: User Interface/X
License: GPLv2
URL: https://github.com/pulb/mailnag
Source0: %{name}-%{version}-bdd7d5826f.tar.bz2
Source1: mailnag.svg
Source2: mailnag_config.desktop

BuildArch: noarch

Requires: pyxdg
Requires: pygobject3
Requires: pygobject2
Requires: gnome-python2-gnomekeyring
Requires: python-httplib2
Requires: libnotify
Requires: gstreamer


%description
Mailnag is a fork of the Popper mail notifier (http://launchpad.net/popper).
What Popper is to Ubuntu's Unity, Mailnag is to GNOME-Shell.

%prep
%setup -q -n %{name}-%{version}-bdd7d5826f

%build
./gen_locales

%install
install -dD -m 755 %{buildroot}%{_datadir}/%{name}
install -dD -m 755 %{buildroot}%{_datadir}/applications
install -dD -m 755 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -dD -m 755 %{buildroot}%{_bindir}

sed -i 's!./Mailnag!/usr/share/mailnag/Mailnag!g' mailnag mailnag_config
sed -i 's!./data!/usr/share/mailnag/data!g' Mailnag/common/utils.py
sed -i 's!./locale!/usr/share/locale!g' Mailnag/common/i18n.py

cp -r locale %{buildroot}%{_datadir}
cp -r Mailnag data %{buildroot}%{_datadir}/%{name}


install -m 755 mailnag mailnag_config %{buildroot}%{_bindir}
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/applications

find %{buildroot}%{_datadir}/%{name} -name "*.py" -exec chmod 755 {} \;

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS LICENSE README.md
%{_bindir}/%{name}*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/*
%{_datadir}/applications/*


%changelog
* Fri Apr 20 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 0.4-0.1.bdd7d5826f.R
- initial build
