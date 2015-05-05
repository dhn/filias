filias - Fetch ILIAS
======

FIlias fetch content from ILIAS System with the SOAP API.
The old version of FIlias was fetched the content via WebDAV.

## Requirements ##

- Python 3.*
- Suds (install with pip3)
- SQLite

## Install

    pip3 install suds-jurko
    git clone https://github.com/dhn/filias.git
    
## Usage
	usage: main.py [options]
	   -f, --fetch           Fetch content from ILIAS Server.
	   -u, --username=USER   Set ilias username to USER.
	   -p, --password=PASS   Set ilias password to PASS.
	   -P, --proxy [PROTOCOL://]HOST[:PORT] Use proxy on given port
	   -h, --help            Show this help and exit.
	   -v, --version         Show version info and exit.
