

#DB replication script

#msql backup binary
$mysql_bin = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe"
$mysql_dump = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqldump.exe"

#Create new DB 
& $mysql_bin -u root -e "CREATE DATABASE BackupDB"

#Do the backup; Stream the data directly from one db into the the newly created one
#backup the entire db
#& $mysql_dump -u root --single-transaction --quick c_root > "C:\c_rootDBDumpAug2026"
#[System.IO.File]::OpenRead("C:\c_rootDBDumpAug2026") | & $mysql_bin -u root c_rootBackup -nop

#--single-transaction — gives InnoDB tables a consistent snapshot without locking them for the dump.
#--quick — streams rows rather than loading entire tables into memory; important for large databases


#"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe" -u root c_rootBackup < "E:\MYSQLBackup\c_rootDBDumpAug2026"

#backup_dump_is_in__E:\MYSQLBackup\c_rootDBDumpAug2026.sql
"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqldump.exe" -u root -p --single-transaction --quick prod | "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe" -u root -p BackupDB
