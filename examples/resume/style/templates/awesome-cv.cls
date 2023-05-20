%% Start of file `awesome-cv.cls'.
% Awesome CV Class File
%
% This class has been downloaded from:
% https://github.com/posquit0/Awesome-CV
%
% Author:
% Claud D. Park <posquit0.bj@gmail.com>
% http://www.posquit0.com
%
% Notes:
% 1) This class file defines the structure and layout of the template file (cv.tex, resume.tex).
% 2) It has been written in such a way that under most circumstances you
% should not need to edit it.
%
% Class license:
% LPPL v1.3c (http://www.latex-project.org/lppl)
%


%-------------------------------------------------------------------------------
%                Identification
%-------------------------------------------------------------------------------
\ProvidesClass{awesome-cv}[2017/02/05 v1.6.1 Awesome Curriculum Vitae Class]
\NeedsTeXFormat{LaTeX2e}


%-------------------------------------------------------------------------------
%                Class options
%
% (need to be done before the external package loading, for example because
% we need \paperwidth, \paperheight and \@ptsize to be defined before loading
% geometry and fancyhdr)
%-------------------------------------------------------------------------------
% Options for draft or final
\DeclareOption{draft}{\setlength\overfullrule{5pt}}
\DeclareOption{final}{\setlength\overfullrule{0pt}}
% Inherit options of article
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}


%-------------------------------------------------------------------------------
%                3rd party packages
%-------------------------------------------------------------------------------
% Needed to make fixed length table
\RequirePackage{array}
% Needed to handle list environment
\RequirePackage{enumitem}
% Needed to handle text alignment
\RequirePackage{ragged2e}
% Needed to configure page layout
\RequirePackage{geometry}
% Needed to make header & footer effeciently
\RequirePackage{fancyhdr}
% Needed to manage colors
\RequirePackage{xcolor}
% Needed to use \ifxetex-\else-\fi statement
\RequirePackage{ifxetex}
% Needed to use \if-\then-\else statement
\RequirePackage{xifthen}
% Needed to use a toolbox of programming tools
\RequirePackage{etoolbox}
% Needed to change line spacing in specific environment
\RequirePackage{setspace}
% Needed to manage fonts
\RequirePackage[quiet]{fontspec}
% To support LaTeX quoting style
\defaultfontfeatures{Ligatures=TeX}
% Needed to manage math fonts
\RequirePackage{unicode-math}
% Needed to use icons from font-awesome
% (https://github.com/posquit0/latex-fontawesome)
\RequirePackage{fontawesome5}
\RequirePackage[default,opentype]{sourcesanspro}
% Needed for the photo ID
\RequirePackage[skins]{tcolorbox}
% Needed to deal a paragraphs
\RequirePackage{parskip}
% Needed to deal hyperlink
\RequirePackage[hidelinks,unicode]{hyperref}
\hypersetup{%
  pdftitle={},
  pdfauthor={},
  pdfsubject={},
  pdfkeywords={}
}


%-------------------------------------------------------------------------------
%                Configuration for directory locations
%-------------------------------------------------------------------------------
% Configure a directory location for fonts(default: 'fonts/')
\newcommand*{\fontdir}[1][fonts/]{\def\@fontdir{#1}}
\fontdir


%-------------------------------------------------------------------------------
%                Configuration for layout
%-------------------------------------------------------------------------------
%% Page Layout
% Configure page margins with geometry
\geometry{left=2.0cm, top=1.5cm, right=2.0cm, bottom=2.0cm, footskip=.5cm}

%% Header & Footer
% Set offset to each header and footer
\fancyhfoffset{0em}
% Remove head rule
\renewcommand{\headrulewidth}{0pt}
% Clear all header & footer fields
\fancyhf{}
% Enable if you want to make header or footer using fancyhdr
\pagestyle{fancy}


%-------------------------------------------------------------------------------
%                Configuration for colors
%-------------------------------------------------------------------------------
% Gray-scale colors
\definecolor{white}{HTML}{FFFFFF}
\definecolor{black}{HTML}{000000}
\definecolor{darkgray}{HTML}{333333}
\definecolor{gray}{HTML}{5D5D5D}
\definecolor{lightgray}{HTML}{777777}
% Basic colors
\definecolor{green}{HTML}{C2E15F}
\definecolor{orange}{HTML}{FDA333}
\definecolor{purple}{HTML}{D3A4F9}
\definecolor{red}{HTML}{FB4485}
\definecolor{blue}{HTML}{6CE0F1}
% Text colors
\definecolor{darktext}{HTML}{414141}
\colorlet{text}{darkgray}
\colorlet{graytext}{gray}
\colorlet{lighttext}{lightgray}
% Awesome colors
\definecolor{awesome-emerald}{HTML}{00A388}   %%%%
\definecolor{awesome-skyblue}{HTML}{0395DE}   %%%%+
\definecolor{awesome-red}{HTML}{DC3522}       %%%%
\definecolor{awesome-pink}{HTML}{EF4089}      %%%
\definecolor{awesome-orange}{HTML}{FF6138}    %%%%%
\definecolor{awesome-nephritis}{HTML}{27AE60} %%%
\definecolor{awesome-concrete}{HTML}{95A5A6}  %% Apple
\definecolor{awesome-darknight}{HTML}{131A28} %%%%
% Google colors
\definecolor{googleBlue}{HTML}{4285f4}   % %%%% Google
\definecolor{googleRed}{HTML}{ea4335}    % %%%%
\definecolor{googleYellow}{HTML}{fbbc05} % %%
\definecolor{googleGreen}{HTML}{34a853}  % %%%%
\definecolor{googleBlack}{HTML}{000000}  % %%%%
% Nubank
\definecolor{nubank}{HTML}{820ad1} % %%%%% Nubank
\definecolor{nubank-light}{HTML}{a964d6}
% Microsoft colors
\definecolor{msBlue}{HTML}{05a6f0}   % %%%% Microsoft
\definecolor{msRed}{HTML}{f35325}    % %%%%
\definecolor{msYellow}{HTML}{ffba08} % %%
\definecolor{msGreen}{HTML}{81bc06}  % %%%

\colorlet{awesome}{|= meta.general.color =|}

\newbool{useGoogleColors}
\setbool{useGoogleColors}{false}

\newcounter{GoogleColorIndexA}
\setcounter{GoogleColorIndexA}{1}

\newcounter{GoogleColorIndexB}
\setcounter{GoogleColorIndexB}{1}

% Counter1 for google color (headers)
\newcommand*{\incColorA}{%
  \stepcounter{GoogleColorIndexA}%
  \ifthenelse{\equal{\theGoogleColorIndexA}{7}}{\setcounter{GoogleColorIndexA}{1}}{}%
}
\newcommand*{\decColorA}{%
  \addtocounter{GoogleColorIndexA}{-1}%
  \ifthenelse{\equal{\theGoogleColorIndexA}{0}}{\setcounter{GoogleColorIndexA}{6}}{}%
}

% Counter2 for google colors (dates, locations, and stuff)
\newcommand*{\incColorB}{%
  \stepcounter{GoogleColorIndexB}%
  \ifthenelse{\equal{\theGoogleColorIndexB}{7}}{\setcounter{GoogleColorIndexB}{1}}{}%
}
\newcommand*{\decColorB}{%
  \addtocounter{GoogleColorIndexB}{-1}%
  \ifthenelse{\equal{\theGoogleColorIndexB}{0}}{\setcounter{GoogleColorIndexB}{6}}{}%
}

% Color text using google colors
\newcommand*{\colorizeA}{%
  \ifbool{useGoogleColors}{%
    \ifthenelse{\equal{\theGoogleColorIndexA}{1}}{\color{googleBlue}}{}%
    \ifthenelse{\equal{\theGoogleColorIndexA}{2}}{\color{googleRed}}{}%
    \ifthenelse{\equal{\theGoogleColorIndexA}{3}}{\color{googleYellow}}{}%
    \ifthenelse{\equal{\theGoogleColorIndexA}{4}}{\color{googleBlue}}{}%
    \ifthenelse{\equal{\theGoogleColorIndexA}{5}}{\color{googleGreen}}{}%
    \ifthenelse{\equal{\theGoogleColorIndexA}{6}}{\color{googleRed}}{}%
  }{%
    \color{awesome}%
  }%
}

\newcommand*{\colorizeB}{%
  \ifbool{useGoogleColors}{%
    \ifthenelse{\equal{\theGoogleColorIndexB}{1}}{\color{googleBlue}}{}%
    \ifthenelse{\equal{\theGoogleColorIndexB}{2}}{\color{googleRed}}{}%
    \ifthenelse{\equal{\theGoogleColorIndexB}{3}}{\color{googleYellow}}{}%
    \ifthenelse{\equal{\theGoogleColorIndexB}{4}}{\color{googleBlue}}{}%
    \ifthenelse{\equal{\theGoogleColorIndexB}{5}}{\color{googleGreen}}{}%
    \ifthenelse{\equal{\theGoogleColorIndexB}{6}}{\color{googleRed}}{}%
  }{%
    \color{awesome}%
  }%
}

% Boolean value to switch section color highlighting
\newbool{acvSectionColorHighlight}
\setbool{acvSectionColorHighlight}{true}

% Awesome section color
\newcommand*{\@sectioncolor}[3]{%
  \ifbool{acvSectionColorHighlight}%
    {{\colorizeA\incColorA#1#2#3}}%
    {\colorizeA\incColorA#1#2#3}%
}


%-------------------------------------------------------------------------------
%                Configuration for fonts
%-------------------------------------------------------------------------------
% Set the FontAwesome font to be up-to-date.
% \newfontfamily\FA[Path=\@fontdir]{FontAwesome}
% Set font for header (default is Roboto)

% Header
\newfontfamily\headerfont[
  Path=\@fontdir,
  UprightFont=*-Regular,
  ItalicFont=*-Italic,
  BoldFont=*-Bold,
  BoldItalicFont=*-BoldItalic,
]{Roboto}

% \newfontfamily\headerfont[
%   Path=\@fontdir,
%   UprightFont=*-Regular,
%   ItalicFont=*-Light,
%   BoldFont=*-Bold,
%   % BoldItalicFont=*-Medium,
% ]{Calibri}

% Header light
\newfontfamily\headerfontlight[
  Path=\@fontdir,
  UprightFont=*-Thin,
  ItalicFont=*-ThinItalic,
  BoldFont=*-Medium,
  BoldItalicFont=*-MediumItalic,
]{Roboto}

% \newfontfamily\headerfontlight[
%   Path=\@fontdir,
%   UprightFont=*-Regular,
%   ItalicFont=*-Light,
%   BoldFont=*-Bold,
%   BoldItalicFont=*-Medium,
% ]{Comfortaa}

% Footer
\newcommand*{\footerfont}{\sourcesanspro}

% Body
% \newcommand*{\bodyfont}{\sourcesanspro}
\newfontfamily\bodyfont[
  Path=\@fontdir,
  UprightFont=*-Regular,
  ItalicFont=*-Italic,
  BoldFont=*-Bold,
  BoldItalicFont=*-BoldItalic,
]{Calibri}

% Body light
% \newcommand*{\bodyfontlight}{\sourcesansprolight}
\newfontfamily\bodyfontlight[
  Path=\@fontdir,
  UprightFont=*-Regular,
  ItalicFont=*-Italic,
  BoldFont=*-Bold,
  BoldItalicFont=*-BoldItalic,
]{CalibriLight}


% Source
\newfontfamily\sourcefont[
  Path=\@fontdir,
  UprightFont=*-Regular,
  % ItalicFont=*-Light,
  BoldFont=*-Medium,
  % BoldItalicFont=*-MediumItalic,
]{FiraCode}

%-------------------------------------------------------------------------------
%                Configuration for styles
%-------------------------------------------------------------------------------

\ifthenelse{\isempty{}}{
  \newcommand*{\link}[2]{\href{#1}{\emph{#2}}}
  \let\emphdate\empty
}{
  \newcommand*{\link}[2]{\href{#1}{#2}}
  \let\emphdate\slshape
}


% Configure styles for each CV elements
% For fundamental structures
\newcommand*{\headerfirstnamestyle}[1]{{\fontsize{32pt}{1em}\headerfontlight\color{graytext} #1}}
\newcommand*{\headerlastnamestyle}[1]{{\fontsize{32pt}{1em}\headerfont\bfseries\color{text} #1}}
\newcommand*{\headerpositionstyle}[1]{{\fontsize{7.6pt}{1em}\bodyfont\scshape\colorizeB #1}}
\newcommand*{\headeraddressstyle}[1]{{\fontsize{8pt}{1em}\headerfont\emphdate\color{lighttext} #1}}
\newcommand*{\headersocialstyle}[1]{{\fontsize{6.8pt}{1em}\headerfont\color{text} #1}}
\newcommand*{\headerquotestyle}[1]{{\fontsize{9pt}{1em}\bodyfont\itshape\color{darktext} #1}}
\newcommand*{\footerstyle}[1]{{\fontsize{8pt}{1em}\footerfont\scshape\color{lighttext} #1}}
\newcommand*{\sectionstyle}[1]{{\fontsize{16pt}{1em}\bodyfont\bfseries\color{text}\@sectioncolor #1}}
\newcommand*{\subsectionstyle}[1]{{\fontsize{12pt}{1em}\bodyfont\scshape\textcolor{text}{#1}}}
\newcommand*{\paragraphstyle}{\fontsize{9pt}{1em}\bodyfontlight\upshape\color{lighttext}}

% For elements of entry
\newcommand*{\entrytitlestyle}[1]{{\fontsize{10pt}{1em}\bodyfont\bfseries\color{darktext} #1}}
\newcommand*{\entrypositionstyle}[1]{{\fontsize{8pt}{1em}\bodyfont\scshape\color{graytext} #1}}
\newcommand*{\entrydatestyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\colorizeB\textbf{ #1}}}
\newcommand*{\entrylocationstyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\colorizeB\textbf{ #1}}}
\newcommand*{\descriptionstyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\upshape\color{text} #1}}

% For elements of subentry
\newcommand*{\subentrytitlestyle}[1]{{\fontsize{8pt}{1em}\bodyfont\mdseries\color{graytext} #1}}
\newcommand*{\subentrypositionstyle}[1]{{\fontsize{7pt}{1em}\bodyfont\scshape\color{graytext} #1}}
\newcommand*{\subentrydatestyle}[1]{{\fontsize{7pt}{1em}\bodyfontlight\emphdate\color{graytext} #1}}
\newcommand*{\subentrylocationstyle}[1]{{\fontsize{7pt}{1em}\bodyfontlight\emphdate\colorizeB #1}}
\newcommand*{\subdescriptionstyle}[1]{{\fontsize{8pt}{1em}\bodyfontlight\upshape\color{text} #1}}

% For elements of honor
\newcommand*{\honortitlestyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\color{lighttext} #1}}
\newcommand*{\honorpositionstyle}[1]{{\fontsize{9pt}{1em}\bodyfont\bfseries\color{darktext} #1}}
\newcommand*{\honordatestyle}[1]{{\fontsize{9pt}{1em}\bodyfont\colorizeB\textbf{ #1}}}
\newcommand*{\honorlocationstyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\colorizeB\textbf{ #1}}}

% For elements of project
\newcommand*{\projecttitlestyle}[1]{{\fontsize{9pt}{1em}\bodyfont\bfseries\color{darktext} #1}}
\newcommand*{\projectdatestyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\colorizeB\textbf{ #1}}}
\newcommand*{\projectdescriptionstyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\color{text} #1}}
\newcommand*{\projectitemsstyle}[1]{\color{lighttext} #1}

% For elements of skill
\newcommand*{\skilltypestyle}[1]{{\fontsize{10pt}{1em}\bodyfont\bfseries\color{darktext} #1}}
\newcommand*{\skillsetstyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\color{text} #1}}

% For elements of the cover letter
\newcommand*{\lettersectionstyle}[1]{{\fontsize{14pt}{1em}\bodyfont\bfseries\color{text}\@sectioncolor #1}}
\newcommand*{\recipientaddressstyle}[1]{{\fontsize{9pt}{1em}\bodyfont\scshape\color{graytext} #1}}
\newcommand*{\recipienttitlestyle}[1]{{\fontsize{11pt}{1em}\bodyfont\bfseries\color{darktext} #1}}
\newcommand*{\lettertitlestyle}[1]{{\fontsize{10pt}{1em}\bodyfontlight\bfseries\color{darktext} \underline{#1}}}
\newcommand*{\letterdatestyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\colorizeB\textbf{ #1}}}
\newcommand*{\lettertextstyle}{\fontsize{10pt}{1.4em}\bodyfont\upshape\color{gray}}
\newcommand*{\letternamestyle}[1]{{\fontsize{10pt}{1em}\bodyfont\bfseries\color{darktext} #1}}
\newcommand*{\letterenclosurestyle}[1]{{\fontsize{10pt}{1em}\bodyfontlight\emphdate\color{lighttext} #1}}


%-------------------------------------------------------------------------------
%                Commands for personal information
%-------------------------------------------------------------------------------
% Define photo ID
% Usage: \photo[circle|rectangle,edge|noedge,left|right]{<path-to-image>}
\newcommand{\photo}[2][circle,edge,left]{%
  \def\@photo{#2}
  \@for\tmp:=#1\do{%
    \ifthenelse{\equal{\tmp}{circle} \or \equal{\tmp}{rectangle}}%
      {\let\@photoshape\tmp}{}%
    \ifthenelse{\equal{\tmp}{edge} \or \equal{\tmp}{noedge}}%
      {\let\@photoedge\tmp}{}%
    \ifthenelse{\equal{\tmp}{left} \or \equal{\tmp}{right}}%
      {\let\@photoalign\tmp}{}%
  }%
}
\def\@photoshape{circle}
\def\@photoedge{edge}
\def\@photoalign{left}

% Define writer's name
% Usage: \name{<firstname>}{<lastname>}
% Usage: \firstname{<firstname>}
% Usage: \lastname{<lastname>}
% Usage: \familyname{<familyname>}
\newcommand*{\name}[2]{\def\@firstname{#1}\def\@lastname{#2}}
\newcommand*{\nameTo}[2]{\def\@firstname{#1,}\def\@lastname{|= meta.formats.to =| #2}}
\newcommand*{\firstname}[1]{\def\@firstname{#1}}
\newcommand*{\lastname}[1]{\def\@lastname{#1}}
\newcommand*{\familyname}[1]{\def\@lastname{#1}}
\newcommand*{\companyname}[1]{\def\@companyname{#1}}
\def\@familyname{\@lastname}



% Configure \lang to set the document language command
% \def\@languageName{en}
% \newcommand*{\lang}[1]{%
%   \def\@languageName{#1}%
%   \ifthenelse{\equal{#1}{pt}}{\usepackage[portuguese]{babel}}{}%
% }
% Configure \tr to accept texts for english(en) and portuguese(pt)
% \newcommand*{\tr}[2]{{\ifthenelse{\equal{en}{\@languageName}}{#1}{#2}}}




% Define writer's address
% Usage: \address{<address>}
\newcommand*{\address}[1]{\def\@address{#1}}

% Define writer's position
% Usage: \position{<position>}
\newcommand*{\position}[1]{\def\@position{#1}}

% Defines writer's mobile (optional)
% Usage: \mobile{<mobile number>}
\newcommand*{\mobile}[1]{\def\@mobile{#1}}

% Defines writer's email (optional)
% Usage: \email{<email address>}
\newcommand*{\email}[1]{\def\@email{#1}}

% Defines writer's homepage (optional)
% Usage: \homepage{<url>}
\newcommand*{\homepage}[1]{\def\@homepage{#1}}

% Defines writer's portfolio page (optional)
% Usage: \portfolio{<url without https://>}
\newcommand*{\portfolio}[1]{\def\@portfolio{#1}}

% Defines writer's github (optional)
% Usage: \github{<github-nick>}
\newcommand*{\github}[1]{\def\@github{#1}}

% Defines writer's gitlab (optional)
% Usage: \gitlab{<gitlab-nick>}
\newcommand*{\gitlab}[1]{\def\@gitlab{#1}}

% Defines writer's stackoverflow profile (optional)
% Usage: \stackoverflow{<so userid>}{<so username>}
%   e.g.https://stackoverflow.com/users/123456/sam-smith
%       would be \stackoverflow{123456}{sam-smith}
\newcommand*{\stackoverflow}[2]{\def\@stackoverflowid{#1}\def\@stackoverflowname{#2}}

% Defines writer's linked-in (optional)
% Usage: \linkedin{<linked-in-nick>}
\newcommand*{\linkedin}[1]{\def\@linkedin{#1}}

% Defines writer's dockerhub (optional)
% Usage: \dockerhub{<dockerhub-in-nick>}
\newcommand*{\dockerhub}[1]{\def\@dockerhub{#1}}

% Defines writer's twitter (optional)
% Usage: \twitter{<twitter handle>}
\newcommand*{\twitter}[1]{\def\@twitter{#1}}

% Defines writer's skype (optional)
% Usage: \skype{<skype account>}
\newcommand*{\skype}[1]{\def\@skype{#1}}

% Defines writer's reddit (optional)
% Usage: \reddit{<reddit account>}
\newcommand*{\reddit}[1]{\def\@reddit{#1}}

% Defines writer's xing (optional)
% Usage: \xing{<xing name>}
\newcommand*{\xing}[1]{\def\@xing{#1}}

% Defines writer's medium profile (optional)
% Usage: \medium{<medium account>}
\newcommand*{\medium}[1]{\def\@medium{#1}}

% Defines writer's google scholar profile (optional)
% Usage: \googlescholar{<googlescholar userid>}{<googlescholar username>}
% e.g.https://scholar.google.co.uk/citations?user=wpZDx1cAAAAJ
% would be \googlescholar{wpZDx1cAAAAJ}{Name-to-display-next-icon}
% If 'googlescholar-name' is not provided than it defaults to
% '\firstname \lastname'
\newcommand*{\googlescholar}[2]{%
  \def\@googlescholarid{#1}%
  \ifthenelse{\equal{#2}{}}{%
    \def\@googlescholarname{\@firstname~\@lastname}%
  }{%
    \def\@googlescholarname{#2}%
  }%
}

% Defines writer's extra informations (optional)
% Usage: \extrainfo{<extra informations>}
\newcommand*{\extrainfo}[1]{\def\@extrainfo{#1}}

% Defines writer's quote (optional)
% Usage: \quote{<quote>}
\renewcommand*{\quote}[1]{\def\@quote{#1}}

% Defines recipient's information (cover letter only)
% Usage: \recipient{<recipient name>}{<recipient address>}
% Usage: \recipientname{<recipient name>}
% Usage: \recipientaddress{<recipient address>}
\newcommand*{\recipient}[2]{\def\@recipientname{#1}\def\@recipientaddress{#2}}
\newcommand*{\recipientname}[1]{\def\@recipientname{#1}}
\newcommand*{\recipientaddress}[1]{\def\@recipientaddress{#1}}

% Defines the title for letter (cover letter only, optional)
% Usage: \lettertitle{<title>}
\newcommand*{\lettertitle}[1]{\def\@lettertitletext{#1}}

% Defines the date for letter (cover letter only)
% Usage: \letterdate{<date>}
\newcommand*{\letterdate}[1]{\def\@letterdate{#1}}

% Defines a message of opening for letter (cover letter only)
% Usage: \letteropening{<message>}
% \newcommand*{\letteropening}[1]{\def\@letteropening{#1}}

% Defines a message of closing for letter (cover letter only)
% Usage: \letterclosing{<message>}
% \newcommand*{\letterclosing}[1]{\def\@letterclosing{#1}}

% Defines an enclosure for letter (cover letter only, optional)
% Usage: \letterenclosure[<enclosure name>]{<enclosure>}
\newcommand*{\letterenclname}[1][Enclosure]{\def\@letterenclname{#1}}
\newcommand*{\letterenclosure}[2][]{%
  % if an optional argument is provided, use it to redefine \enclname
  \ifthenelse{\equal{#1}{}}{}{\def\@letterenclname{#1}}
  \def\@letterenclosure{#2}
}


%-------------------------------------------------------------------------------
%                Commands for extra
%-------------------------------------------------------------------------------
%% Define helper macros a user can change easily
% Header
\newcommand{\hquad}{\hskip0.5em\relax}
\newcommand{\acvHeaderNameDelim}{\space}
\newcommand{\acvHeaderAfterNameSkip}{.4mm}
\newcommand{\acvHeaderAfterPositionSkip}{.4mm}
\newcommand{\acvHeaderAfterAddressSkip}{-.5mm}
\newcommand{\acvHeaderIconSep}{\space}
\newcommand{\acvHeaderSocialSep}{\quad\textbar\quad}
\newcommand{\acvHeaderAfterSocialSkip}{6mm}
\newcommand{\acvHeaderAfterQuoteSkip}{5mm}


% Others
\newcommand{\acvPositionSep}{\hquad\textbar\hquad}
\newcommand{\acvSectionTopSkip}{10mm}
\newcommand{\acvSectionContentTopSkip}{2.5mm}


%-------------------------------------------------------------------------------
%                Commands for utilities
%-------------------------------------------------------------------------------
% Use to align an element of tabular table
\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}

% Use to draw horizontal line with specific thickness
\def\vhrulefill#1{\leavevmode\leaders\hrule\@height#1\hfill \kern\z@}

% Use to execute conditional statements by checking empty string
\newcommand*{\ifempty}[3]{\ifthenelse{\isempty{#1}}{#2}{#3}}


%-------------------------------------------------------------------------------
%                Commands for elements of CV structure
%-------------------------------------------------------------------------------
% Define a header for CV
% Usage: \makecvheader
\newcommand*{\makecvheader}[1][C]{%
  \let\drawphoto\undefined%
  \let\headertextwidth\undefined%
  \let\headerphotowidth\undefined%
  \newcommand*{\drawphoto}{%
    \ifthenelse{\isundefined{\@photo}}{}{%
      \newlength{\photodim}
      \ifthenelse{\equal{\@photoshape}{circle}}%
        {\setlength{\photodim}{1.3cm}}%
        {\setlength{\photodim}{1.8cm}}%
      \ifthenelse{\equal{\@photoedge}{edge}}%
        {\def\@photoborder{darkgray}}%
        {\def\@photoborder{none}}%
      \begin{tikzpicture}%
        \node[\@photoshape, draw=\@photoborder, line width=0.3mm, inner sep=\photodim, fill overzoom image=\@photo] () {};
      \end{tikzpicture}
    }%
  }
  \newlength{\headertextwidth}
  \newlength{\headerphotowidth}
  \ifthenelse{\isundefined{\@photo}}{
    \setlength{\headertextwidth}{\textwidth}
    \setlength{\headerphotowidth}{0cm}
  }{%
    \setlength{\headertextwidth}{0.76\textwidth}
    \setlength{\headerphotowidth}{0.24\textwidth}
  }%
  \begin{minipage}[c]{\headerphotowidth}%
    \ifthenelse{\equal{\@photoalign}{left}}{\raggedright\drawphoto}{}
  \end{minipage}
  \begin{minipage}[c]{\headertextwidth}
    \ifthenelse{\equal{#1}{L}}{\raggedright}{\ifthenelse{\equal{#1}{R}}{\raggedleft}{\centering}}
    \headerfirstnamestyle{\@firstname}\headerlastnamestyle{{}\acvHeaderNameDelim\@lastname}%
    \\[\acvHeaderAfterNameSkip]%
    \ifthenelse{\isundefined{\@position}}{}{\headerpositionstyle{\@position\\[\acvHeaderAfterPositionSkip]}}%
    \ifthenelse{\isundefined{\@address}}{}{\headeraddressstyle{\@address\\[\acvHeaderAfterAddressSkip]}}%
    \headersocialstyle{%
      \newbool{isstart}%
      \setbool{isstart}{true}%
      \ifthenelse{\isundefined{\@mobile}}%
        {}%
        {%
          \faMobile\acvHeaderIconSep\@mobile%
          \setbool{isstart}{false}%
        }%
      \ifthenelse{\isundefined{\@email}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{mailto:\@email}{\faEnvelope\acvHeaderIconSep\@email}%
        }%
      \ifthenelse{\isundefined{\@homepage}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://\@homepage}{\faHome\acvHeaderIconSep Homepage}%
        }%
      \ifthenelse{\isundefined{\@portfolio}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://\@portfolio}{\faFolder\acvHeaderIconSep |= meta.formats.portfolio =|}%
        }%
      \ifthenelse{\isundefined{\@github}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://github.com/\@github}{\faGithubSquare\acvHeaderIconSep Github}%
        }%
      \ifthenelse{\isundefined{\@gitlab}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://gitlab.com/\@gitlab}{\faGitlab\acvHeaderIconSep\@gitlab}%
        }%
      \ifthenelse{\isundefined{\@stackoverflowid}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://stackoverflow.com/users/\@stackoverflowid}{\faStackOverflow\acvHeaderIconSep\@stackoverflowname}%
        }%
      \ifthenelse{\isundefined{\@linkedin}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://www.linkedin.com/in/\@linkedin}{\faLinkedin\acvHeaderIconSep Linkedin}%
        }%
      \ifthenelse{\isundefined{\@twitter}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://twitter.com/\@twitter}{\faTwitter\acvHeaderIconSep\@twitter}%
        }%
      \ifthenelse{\isundefined{\@dockerhub}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://hub.docker.com/u/\@dockerhub}{\faDocker\acvHeaderIconSep Dockerhub}%
        }%
      \ifthenelse{\isundefined{\@skype}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \faSkype\acvHeaderIconSep\@skype%
        }%
      \ifthenelse{\isundefined{\@reddit}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://www.reddit.com/user/\@reddit}{\faReddit\acvHeaderIconSep\@reddit}%
        }%
      \ifthenelse{\isundefined{\@xing}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://www.xing.com/profile/\@xing}{\faXingSquare\acvHeaderIconSep\@xing}
        }%
      \ifthenelse{\isundefined{\@medium}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://medium.com/@\@medium}{\faMedium\acvHeaderIconSep\@medium}%
        }%
      \ifthenelse{\isundefined{\@googlescholarid}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \link{https://scholar.google.com/citations?user=\@googlescholarid}{\faGraduationCap\acvHeaderIconSep\@googlescholarname}%
        }%
      \ifthenelse{\isundefined{\@extrainfo}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \@extrainfo%
        }%
    } \\[\acvHeaderAfterSocialSkip]%
    \ifthenelse{\isundefined{\@quote}}%
      {}%
      {\headerquotestyle{\@quote\\}\vspace{\acvHeaderAfterQuoteSkip}}%
  \end{minipage}%
  \begin{minipage}[c]{\headerphotowidth}%
    \ifthenelse{\equal{\@photoalign}{right}}{\raggedleft\drawphoto}{}
  \end{minipage}
}

% Define a footer for CV
% Usage: \makecvfooter{<left>}{<center>}{<right>}
\newcommand*{\makecvfooter}[3]{%
  \fancyfoot{}
  \fancyfoot[L]{\footerstyle{#1}}
  \fancyfoot[C]{\footerstyle{#2}}
  \fancyfoot[R]{\footerstyle{#3}}
}

% Define a section for CV
% Usage: \cvsection{<section-title>}
\newcommand{\cvsection}[1]{%
  \vspace{\acvSectionTopSkip}
  \sectionstyle{#1}
  \phantomsection
  \color{gray}\vhrulefill{0.9pt}
}

% Define a subsection for CV
% Usage: \cvsubsection{<subsection-title>}
\newcommand{\cvsubsection}[1]{%
  \vspace{\acvSectionContentTopSkip}
  \vspace{-3mm}
  \subsectionstyle{#1}
  \phantomsection
}

% Define a paragraph for CV
\newenvironment{cvparagraph}{%
  \vspace{\acvSectionContentTopSkip}
  \vspace{-3mm}
  \paragraphstyle
}{%
  \par
  \vspace{2mm}
}

% Define a paragraph for missing references
\newenvironment{cvreferences}{%
  \vspace{\acvSectionContentTopSkip}
  \vspace{-3mm}
  \paragraphstyle
}{%
  \par
  \vspace{2mm}
}

% Define an environment for cventry
\newenvironment{cventries}{%
  \vspace{\acvSectionContentTopSkip}
  \begin{center}
}{%
  \end{center}
}
% Define an entry of cv information
% Usage: \cventry{<position>}{<title>}{<location>}{<date>}{<description>}
\newcommand*{\cventry}[5]{%
  \vspace{-2mm}
  \setlength\tabcolsep{0.0mm}
  % \setlength{\extrarowheight}{0pt}
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} L{\textwidth - 7.5cm} R{7.5cm}}
    \entrytitlestyle{#2}\ifempty{#1}{}{\entrypositionstyle{\enskip\cdotp\enskip #1}} & \entrydatestyle{\ifempty{#3}{#4}{#3\enskip\cdotp\enskip #4}}
  \end{tabular*}\\
  \vspace{-1mm}
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} L{\textwidth}}
    \begin{justify}\vspace{-4mm}\descriptionstyle{#5}\end{justify}\vspace{-4mm}
  \end{tabular*}\incColorB\\
}

% Define an environment for cvsubentry
\newenvironment{cvsubentries}{%
  \begin{center}
}{%
  \end{center}
}
% Define a subentry of cv information
% Usage: \cvsubentry{<position>}{<title>}{<date>}{<description>}
\newcommand*{\cvsubentry}[4]{%
  \setlength\tabcolsep{0pt}
  \setlength{\extrarowheight}{0pt}
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} L{\textwidth - 4.5cm} R{4.5cm}}
    \setlength\leftskip{0.2cm}
    \subentrytitlestyle{#2} & \ifthenelse{\equal{#1}{}}
      {\subentrydatestyle{#3}}{}
    \ifthenelse{\equal{#1}{}}
      {}
      {\subentrypositionstyle{#1} & \subentrydatestyle{#3} \\}
    \ifthenelse{\equal{#4}{}}
      {}
      {\multicolumn{2}{L{17.0cm}}{\subdescriptionstyle{#4}} \\}
  \end{tabular*}
}

% Define an environment for cvhonor
\newenvironment{cvhonors}{%
  \vspace{\acvSectionContentTopSkip}
  \vspace{-2mm}
  \begin{center}
    \setlength\tabcolsep{1ex}
    \setlength{\extrarowheight}{0pt}
    \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} R{2.0cm} L{\textwidth - 5.7cm} R{3cm}}
}{%
    \end{tabular*}
  \end{center}
}
% Define a line of cv information(honor, award or something else)
% Usage: \cvhonor{<position>}{<title>}{<location>}{<date>}
\newcommand*{\cvhonor}[4]{%
  \honordatestyle{#4} & 
  \ifthenelse{\isempty{#1}}
  {%
    \ifthenelse{\isempty{#2}}
      {}
      {\honorpositionstyle{#2}}
  }
  {%
    \honorpositionstyle{#1}%
    \ifthenelse{\isempty{#2}}
      {}
      {, \honortitlestyle{#2}}
  } &
  % \honorpositionstyle{#1}\ifthenelse{\isempty{#2}}{}{, \honortitlestyle{#2}} & 
  \honorlocationstyle{#3} \incColorB\\
}

% Define two lines of cv information for a publication
% Usage: \publish{<link>}{<title>}{<authors>}{<date>}
\newcommand*{\cvpublish}[4]{%
   & \honorpositionstyle{\link{#1}{#2}}\newline \honortitlestyle{#3} & \honorlocationstyle{#4} \incColorB\\
}

% Define an environment for cvskill
\newenvironment{cvskills}{%
  \vspace{\acvSectionContentTopSkip}
  \vspace{-2.0mm}
  \begin{center}
    \setlength\tabcolsep{1.0ex}
    \setlength{\extrarowheight}{0pt}
    \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} R{2.0cm} L{\textwidth - 2.0cm}}
}{%
    \end{tabular*}
  \end{center}
}
% Define a line of cv information(skill)
% Usage: \cvskill{<type>}{<skillset>}
\newcommand*{\cvskill}[2]{%
	\skilltypestyle{#1} & \skillsetstyle{#2} \\
}

% Define an environment for cvitems(for cventry)
\newenvironment{cvitems}{%
  \vspace{-4.0mm}
  \begin{justify}
  \begin{itemize}[leftmargin=2.3ex, nosep, noitemsep]
    \setlength{\parskip}{0pt}
    \renewcommand{\labelitemi}{\bullet}
}{%
  \end{itemize}
  \end{justify}
  \vspace{-4.0mm}
}


%-------------------------------------------------------------------------------
%                Commands for elements of Cover Letter
%-------------------------------------------------------------------------------
% Define an environment for cvletter
\newenvironment{cvletter}{%
  \lettertextstyle
}{%
}

% Define a section for the cover letter
% Usage: \lettersection{<section-title>}
\newcommand{\lettersection}[1]{%
  \par\addvspace{2.5ex}
  \phantomsection{}
  \lettersectionstyle{#1}
  \color{gray}\vhrulefill{0.9pt}
  \par\nobreak\addvspace{0.4ex}
}

% Define a title of the cover letter
% Usage: \makelettertitle
\newcommand*{\makelettertitle}{%
  % \vspace{5.0mm}
  \setlength\tabcolsep{0pt}
  \setlength{\extrarowheight}{0pt}
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} L{\textwidth - 4.5cm} R{4.5cm}}
    \recipienttitlestyle{\@recipientname} & \letterdatestyle{\@letterdate}
  \end{tabular*}
  \begin{singlespace}
    \recipientaddressstyle{\@recipientaddress}\newline\vspace{6.0mm}
  \end{singlespace}
  \incColorB
  % \ifthenelse{\isundefined{\@lettertitletext}}
  %   {}
  %   {\lettersection{\@lettertitletext}}
  % \lettertextstyle{\@letteropening}
}

% Define a closing of the cover letter
% Usage: \makelettersignature
\newcommand*{\makelettersignature}[2]{%
  \vspace{6.8mm}
  \begin{flushright}
    \lettertextstyle{#1} \\[6.0mm]
    \letternamestyle{#2}
  \end{flushright}
  \ifthenelse{\isundefined{\@letterenclosure}}
    {}
    {%
      \\[8.0mm]
      \letterenclosurestyle{\@letterenclname: \@letterenclosure}
    }
}

\newcommand*{\makelettersubject}[1]{%
  \lettersection{#1}
  \vspace{8.0mm}
}

\newcommand*{\makeletteropening}[1]{
  \lettertextstyle{#1} \\[4.0mm]
}

\newcommand*{\makelettertopic}[1]{
  \textbf{\colorizeB{\large #1 - }}
}

% Coding
\newcommand*{\code}[1]{\textbf{\colorizeB\sourcefont\scriptsize #1}\lettertextstyle}
\newcommand*{\n}{\textbackslash n}

% Projects
% \begin{cvprojects}...\end{cvprojects}
\newenvironment{cvprojects}{%
  \vspace{\acvSectionContentTopSkip}
  \vspace{-2mm}
  \incColorB
  % \setlength{\extrarowheight}{0pt}
  \setlength\tabcolsep{0.0mm}
  \begin{center}
    % \setlength\tabcolsep{0.0mm}
}{%
  \end{center}
  \decColorB
  % \vspace{-4mm}
}

% \cvproject
% #1 Company link
% #2 Company name
% #3 Position name
% #4 Location
% #5 Date
% #6 Company description
% #7 My participation
\newcommand*{\cvproject}[7]{
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} C{0.5cm} L{\textwidth - 5.5cm} R{5.0cm}}
    & \projecttitlestyle{\ifempty{#1}{#2}{\link{#1}{#2}}}\ifempty{#3}{}{\entrypositionstyle{\enskip\cdotp\enskip #3}}%
    & \projectdatestyle{#4\ifempty{#5}{}{\enskip\cdotp\enskip#5}} \\
  \end{tabular*}\\
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} C{0.5cm} L{\textwidth - 0.5cm}}
    & \begin{justify}\vspace{-4mm}\projectdescriptionstyle{#6}\vspace{-3mm}\end{justify} \\
    & \hspace*{0.5cm}\projectitemsstyle{\begin{cvitems}\item{#7}\end{cvitems}} \\
  \end{tabular*}\vspace{1mm}
  \incColorB
}
