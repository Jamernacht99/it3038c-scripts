Get-service | format-list displayname, status  
get-service | format-table displayname, status  
get-service | format-table *  
get-service | sort-object –property Status –descending | format-table displayname, status  
 get-service | sort-object –property Status –descending | format-table displayname, status | out-file C:\services.txt   
 notepad C:\services.txt  
 Remove-Item C:\services.txt  
 get-service | out-gridview  
 get-service | select-object displayname, status | out-gridview  
 get-service | select-object * | out-gridview  
$Hello = "Hello, PowerShell" 
Write-Host($Hello) 
Set-ExecutionPolicy -ExecutionPolicy Unrestricted 
function getIP{ 

    (get-netipaddress).ipv4address | Select-String "192*" 

} 
write-host(getIP) 
$IP = getIP 

Write-Host(“This machine’s IP is $IP”) 

Write-Host(“This machine’s IP is {0}” -f $IP) 