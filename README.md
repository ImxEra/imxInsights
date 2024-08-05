# imxInsights

![imxInsights logo](https://raw.githubusercontent.com/ImxEra/imxInsights/main/docs/assets/logo.svg#only-dark#gh-dark-mode-only)
![imxInsights logo](https://raw.githubusercontent.com/ImxEra/imxInsights/main/docs/assets/logo-light.svg#only-light#gh-light-mode-only)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/imxInsights)
[![PyPI - Status](https://img.shields.io/pypi/status/imxInsights)](https://pypi.org/project/imxInsights/)

[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com)
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](http://ansicolortags.readthedocs.io/?badge=latest)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
![PyPI - License](https://img.shields.io/pypi/l/imxInsights)

**Documentation**: <a href="https://ImxEra.github.io/imxInsights/" target="_blank">https://ImxEra.github.io/imxInsights/</a>

**Source Code**: <a href="https://github.com/ImxEra/imxInsights" target="_blank">https://github.com/ImxEra/imxInsights</a>

***THIS LIBRARY IS NOT AFFILIATED WITH PRORAIL***, this is a personal project and is not owned or endorsed by ProRail. 
Therefore, ProRail assumes no responsibility for the functionality, accuracy, or usage of this library. 
***THE PUBLIC retains full ownership and responsibility for the codebase.*** 

!!! danger "Warning!"  

    - The goal of `imxInsights` is to extract information from imx files. **Please note that modifying, 
    adding, deleting, or altering data is beyond the scope of this module**.
    - `imxInsights` explicit supports imx versions 1.2.4, 5.0.0 and all major versions up to and including version 12.0.0.
    
!!! info "Audience"

    The intended audience for `imxInsights` consists of end users with basic Python knowledge. Therefore, the module offers a minimalistic API that is thoroughly documented. 
    We leverage the remarkable `makedocs` plugins to effortlessly generate a polished website from documentations and markdown files.


## This repository host the imx 12.0 implementation     

Transitioning from version 1.2.4 / 5.0.0 to 12.0.0 of this library necessitates extensive changes and significant code 
rewriting due to fundamental shifts in how imx files are utilized. Below, we outline a comprehensive roadmap that will 
be continually updated until we reach the first stable version.


!!! danger "New concept, breaking changes!"  
    ***This project is currently under active development and is not yet in its final form.***
    ***As such, there may be frequent changes, incomplete features, or potential instability.***

    ***-   We recommend using the stable and feature richer 0.1.0 release on for imx versions "1.2.4" and "5.0.0".***

### Roadmap

#### Q3-1 2024 - init public release on github
![](https://progress-bar.dev/98?title=progresses)

- [X] Imx Container POC to init project
- [X] Imx 1.2.4 5.0.0 and 12.0.0 file import
- [X] Imx Config Class
- [X] ImxExtension objects
- [X] Imx single file 
- [X] Imx zip container
- [X] ImxCustomException and handler
- [X] GML shapley geometry
- [X] RailConnection shapley geometry
- [X] Known parent and children
- [X] Imx data as Pandas dataframe


####  Q3-2 2024 - MVP library release on PyPI
- [X] Imx Compair imx version ignore
- [X] Imx Compair Object
- [ ] Compair object metadata overview
- [ ] Compair object type between 2 versions 
- [ ] Compair object type as timeline
- [ ] Compair as pandas dataframe
- [ ] Excel output
- [ ] Imx container metadata
- [ ] Imx single file metadata
- [ ] Imx data as Geojson
- [ ] Compair as geojson
- [ ] Documentation update
- [ ] min tests coverage 95%
- [ ] clean git by fresh upload 🎉
- [ ] GitHub actions release on pypi


####  Q4-1 2024 
- [ ] (Imx) Area's and area classifier
- [ ] Excel diff color dataframe and excel
- [ ] Ref as objects
- [ ] nice ref display
- [ ] parent path display
- [ ] km by linear referencing
- [ ] RailConnectionInfos class
- [ ] TrackFragments support
- [ ] implement puic as a concept instead of passing keys to make clear what we use as a key.


#### Backlog current features implementation
- [ ] Situation changes support (read and check)
- [ ] graph implementation
- [ ] generate graph geometry
- [ ] graph end user api
- [ ] advanced geometry view
- [ ] 3d Measure calculator
- [ ] Imx 1.0-RC release on pypi


## Supported Python Versions
This library is compatible with ***Python 3.10*** and above. 

!!! warning  
    ***Python Typehints are awesome therefor 3.9 and below will NOT be supported***.


## Features
todo


## Quick Start
todo

## Distribution and installation
todo

## Code samples and snippets
todo

## Contributing
Contributions welcome! For more information on the design of the library, see [contribution guidelines for this project](CONTRIBUTING.md).

