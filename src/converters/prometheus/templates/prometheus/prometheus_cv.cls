\LoadClass{article}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{PrometheusCV}[2020/10/14 Here to make editing your CV not an eternal torment]

\RequirePackage{titlesec}

% We customise the \section command 
\titleformat{\section}         
  {\large\scshape\raggedright} % Make the \section headers large, small caps and left aligned
  {}{0em}                      % No label (prefix) and no horizontal separation between label and title body
  {}                           		% Code preceeding the title body
  [\titlerule]                 % Code following the title body. Here a horizontal line.
 
 % We also slightly update \subsection command
 \titleformat{\subsection}
 {\normalsize\scshape\raggedright}
 {}{0em}
 {}
 
 %%% define the \datedsubsection command %%%
\newcommand{\datedsubsection}[5]{%	
	\cvsubsection[#3]{\textbf{#4}  \hfill \small{\textlf{\scshape{#1}}} \\}%
	\small{\textlf{\scshape{#3}}}
	\raggedright
	#5
}

\newcommand{\datedsubsectionwithoutenterprise}[5]{%	
	\cvsubsection[#3]{\textbf{#4}  \hfill \small{\textlf{\scshape{#1}}} \\}%
	% \small{\textlf{\scshape{#3}}}
	\raggedright
	#5
}

\newcommand{\undatedsubsection}[3]{%	
	\cvsubsection[#2]{\textbf{#1}}%
	\raggedright
	\begin{small}
		#3
	\end{small}
}

 %%% define the \datedsubsectionnarrow command %%%
\newcommand{\datedsubsectionnarrow}[4]{%	
	\cvsubsectionnarrow[#2]{#3 \hfill \small{\textlf{\scshape{#2}}}}%
	\begin{minipage}{5cm}
		\vspace*{-.7ex}\hspace*{-3cm}\footnotesize #1
	\end{minipage}
	\raggedright
	
	\begin{small}
		#4
	\end{small}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% DEFINE OUR OWN SUBSECTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcounter{cvsubsection}
\titleclass{\cvsubsection}{straight}[\part]
\titleformat{\cvsubsection}         
	{\raggedright} 
	{}{0em}                      
	{}                           
\titlespacing*{\cvsubsection}{0pt}{3.5ex plus 1ex minus .2ex}{-2.5ex}

% The same but in narrow 
\newcounter{cvsubsectionnarrow}
\titleclass{\cvsubsectionnarrow}{straight}[\part]
\titleformat{\cvsubsectionnarrow}         
	{\raggedright} 
	{}{0em}                      
	{}                           
\titlespacing*{\cvsubsectionnarrow}{0pt}{0pt}{-2.5ex}

