DB QUERY optimsation by removal of rows from selected tables
The tables in question here are: request, request_detail and report tables, They are the cause of most latency issues reported by users.

The order of the procedure of the operation is as follows:
1. Create a back-up database alongside the production database; grant necessary users necessary privileges if neeed be

2. Run db_backup.bat via command prompt to create a copy of the data that we are going to remove from the production database in the created backup database

3.Once all the data has been backed up, we can reduce the size of the production database. Through powershell run delete_rows.ps1 to delete all data  dated before 2024

Contigencies
Data may be needed back to the production database so there are 2 scripts to return the data back to the production db.

1. First measure is to return just select rows back to the production db tables - the pre-requisite will be that to use it you'll need to know the name of the table and the condition that specifies/narrows down the exact row to return to the production database table ie the column name and the value of teh column in that row. The script will fetch the row from the backup db and write it to the prod db. Just run restore_specified_data.ps1, it will prompt you the table in which the data is needed, the column to use and the value to look for in that column.

2. Second measure is to return a range of data(if you need to return chunks of data at once without returning all removed data, you can specify use a range, eg using a date frame or id-range.) For this run restore_datarange.ps1
You'll be prompted the table, then the specifying column and the values where the range should start and end. The script will repopulate the data from the backup db to the prod db

3. Third measure is to retrieve all removed data back into the production db.
First create an SQL dump of the data to be retuned.(Done by running dumpPre2024data.ps1 via powershell). Then run restorepre2024dataFromdump.bat via command prompt, This will restore all data back to the prod db. 