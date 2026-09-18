$mysql_bin = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe"

$queries = @("DELETE FROM request WHERE updated_at < '2025-01-01'",
			 "DELETE FROM request_detail WHERE updated_at < '2025-01-01'")
			# "DELETE FROM report WHERE updated_at < '2024-01-01'")

#delete old data
foreach ($query in $queries) {
	& $mysql_bin -u root -p prod -e $query
}