#Command line arguments will be used to gather the data to be restored
#We start by asking for the table(report, request or request_detail)
#We then collect the condition, we first collect the column name, then collect the specifying parameter

param (
    [Parameter(Mandatory=$true)] [string]$Table,
	[Parameter(Mandatory=$true)] [string]$Column,
	[Parameter(Mandatory=$true)] [string]$Condition
)

$mysql_bin = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe"
$mysql_dump = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqldump.exe"

$target_condition = "$Column=$Condition"

& $mysql_dump -u root -p --no-create-info --quick --skip-add-drop-table --skip-disable-keys --skip-lock-tables --where="$target_condition" BackupDB $Table #| & $mysql_bin -u root -p prod 2> "C\restorations.log"
