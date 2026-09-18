#Command line arguments will be used to gather the data to be restored
#We start by asking for the table(report, request or request_detail)
#We then collect the condition, we first collect the column name, then collect the specifying parameter

param (
    [Parameter(Mandatory=$true)] [string]$Table,
	[Parameter(Mandatory=$true)] [string]$Column,
	[Parameter(Mandatory=$true)] [string]$Range_Start,
	[Parameter(Mandatory=$true)] [string]$Range_End
)
#For the range start and end, if using dates to specify the range, use the format 'YYYY-MM-DD'

$mysql_bin = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe"
$mysql_dump = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqldump.exe"

$target_condition = "$Column >= '$Range_Start' AND $Column <= '$Range_End'"

& $mysql_dump -u root -p --no-create-info --quick --skip-add-drop-table --skip-disable-keys --skip-lock-tables --where="$target_condition" backUpDB $Table | & $mysql_bin -u root -p prodDB 2> "C:\restorations.log"
