Hello!

**Format of CSV-Source file:**
ID,NAME,COUNTRY

**TargetFormat**
<dataroot>
	<Address>
		<ADDRNUMBER>1</ADDRNUMBER>
		<ID>0123231</ID>
		<Country>DE</Country>
	</Address>
 <dataroot>

Features
 * Code automatically adds ADDRNUMBER
 * Split - Files to a given number
 * Filepicker instead of providing path via command line
 * If NAME is longer than 40 (SAP limit) -> NAME2 till NAME4 is automatically added
 
