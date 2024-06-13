Hello!

**Format of CSV-Source file:**
ID,NAME,COUNTRY

Delimiter must be ","
Each e.g. ID oder NAME will be a node in XML

**TargetFormat**
<dataroot>
	<Address>
		<ADDRNUMBER>1</ADDRNUMBER>
		<ID>0123231</ID>
		<Country>DE</Country>
	</Address>
 <dataroot>

Features
 * Provides a feature to clean up names (e.g. special characters)
 * Code automatically adds ADDRNUMBER
 * Split - Files to a given number
 * Filepicker instead of providing path via command line
 * If NAME is longer than 40 (SAP limit) -> NAME2 till NAME4 is automatically added

 
RUN via Commandline or create Executable (pyinstaller -F csvconvert.py)
