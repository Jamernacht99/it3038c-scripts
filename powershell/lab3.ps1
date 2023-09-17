$CurrentDate = Get-Date -Format "dddd, MMMM d yyyy"
$PSVERSION = $PSVersionTable.PSVersion
$USER = $env:USERNAME
$HOSTNAME = $env:COMPUTERNAME
$IPADDRESS = (Get-NetIPAddress | Where-Object { $_.AddressFamily -eq 'IPv4' }).IPAddress
$Recipients = @("lamjs@mail.uc.edu", "leonardf@ucmail.uc.edu")


$BODY = "This machine's IP is $IPADDRESS. User is $USER. Hostname is $HOSTNAME. PowerShell Version $PSVERSION. Today's Date is $CURRENTDATE"

Write-Output "Recipients = "
Write-Output $Recipients
Write-Output "`n"

#
#Send-MailMessage -To "$Recipients" -From "jlam8931@gmail.com" -Subject "IT3038C Windows SysInfo" -Body $BODY -SmtpServer smtp.gmail.com -port 587 -UseSSL -Credential (Get-Credential) 

$BODY | Set-content -Path "C:it3038c-scripts\powershell\bodyOuput.txt"