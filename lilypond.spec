Summary:	Music typesetter
Summary(pl):	Program do sk³adania nut
Name:		lilypond
Version:	1.2.6
Release:	1
License:	GPL
Group:		Applications/Sound
Group(de):	Applikationen/Laut
Group(pl):	Aplikacje/D¼wiêk
Source0:	ftp://ftp.gnu.org/gnu/lilypond/%{name}-%{version}.tar.gz
URL:		http://www.cs.uu.nl/people/hanwen/lilypond/index.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LilyPond is a music typesetter. It produces beautiful sheet music
using a high level description file as input. It excels at typesetting
classical music, but you can also print pop-songs. With LilyPond we
hope to make music publication software available to anyone on the
internet.

%description -l pl
LilyPond jest programem do sk³adu muzycznego. Produkuje piêkne
partytury u¿ywaj±c jêzyka wysokiego poziomu jako wej¶cie. S³u¿y przede
wszystkim do sk³adania nut muzyki klasycznej, ale mo¿na drukowaæ tak¿e
piosenki pop. Autorzy udostêpniaj± LilyPond z nadziej± dostarczenia
wszystkim oprogramowania do publikacji muzycznych.

%prep
%setup -q

%build
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,root,root,755)
