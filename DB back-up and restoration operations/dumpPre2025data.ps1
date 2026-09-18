$mysql_bin = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe"
$mysql_dump = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqldump.exe"

$tables = @("report", "request", "request_detail")
$condition = "updated_at < '2025-01-01'"

$output = "E:\MYSQLBackup\pre2025Dumps.sql"
#Restore(stream) data from the backup DB to the active prod db; Table by table
foreach ($table in $tables) {
	$temp = "E:\MYSQLBackup\$table.sql"
	& $mysql_dump -u root -p --single-transaction --no-create-info --skip-triggers --skip-lock-tables --skip-add-locks --insert-ignore --quick --skip-add-drop-table --skip-disable-keys --where="$condition" prodBackupAug2026 $table >> $temp #| & $mysql_bin -u root -p prod

    if ($LASTEXITCODE -ne 0) {
        Write-Host "mysqldump failed for $table"
        exit 1
    }

    Get-Content $temp | Add-Content $output
    Remove-Item $temp
}

#--single-transaction — gives InnoDB tables a consistent snapshot without locking them for the dump.
#--quick — streams rows rather than loading entire tables into memory; important for large databases
#--no-create-info - tells mysqldump to dump only the INSERT statements, not CREATE TABLE statements.
#--insert-ignore - skip rows that already exist and only add new rows,prevents duplicate-key error.
#--skip-add-drop-table - don't include drop table statements
#--skip-disable-keys - don't include ALTER TABLE statements
#--skip-lock-tables - prevents lock table statements
#--