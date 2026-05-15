$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "C:\worklist\DCMTK_WLM"
$watcher.Filter = "*.txt"
$watcher.EnableRaisingEvents = $true
 
Register-ObjectEvent $watcher Created -Action {
    $input = $Event.SourceEventArgs.FullPath
    $output = "C:\worklist\DCMTK_WLM\" + [System.IO.Path]::GetFileNameWithoutExtension($input) + ".wl"
 
    try {
        # Wait briefly to ensure file write is complete
        Start-Sleep -Milliseconds 500
 
        # Convert
        & "C:\Users\Administrator\Downloads\dcmtk-3.7.0-win64-dynamic\dcmtk-3.7.0-win64-dynamic\bin\dump2dcm.exe" +E $input $output
 
        # Only delete if conversion succeeded
        if (Test-Path $output) {
            Remove-Item $input
        }
    }
    catch {
        Write-Host "Error processing $input"
    }
}
 
while ($true) { Start-Sleep 5 }
