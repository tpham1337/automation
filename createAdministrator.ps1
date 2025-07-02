Connect-MgGraph -TenantId "YOUR TENANT ID" -Scopes "user.readwrite.all","RoleManagement.readwrite.directory"

# User Object -----------------
$displayName = "Juan Speedy"
$givenName = "Juan"
$surName = "Speedy"
$domain = "M365x59378762.onmicrosoft.com"
$mailNickName = "$givenName.$surName"
$userPrincipalName = "$givenName.$surName@$domain"
$temporaryPassword = "h4ck3rM4n!"

$passwordProfile = @{
    Password = $temporaryPassword
}

# Administrator role(s) -------
$adminRoles = "User Administrator","Intune Administrator" # Example for multiple roles: $adminRoles = "User Administrator","Intune Administrator","Exchange Administrator"
#------------------------------

$user = New-MgUser -DisplayName $displayName -GivenName $givenName -Surname $surName -UserPrincipalName $userPrincipalName -PasswordProfile $passwordProfile -AccountEnabled -MailNickname $mailNickName

foreach($adminRole in $adminRoles){
    $roles = Get-MgDirectoryRole
    $role = $roles | Where-Object { $_.DisplayName -eq "$adminRole" }
    if (-not $role) {
        $template = Get-MgDirectoryRoleTemplate | Where-Object { $_.DisplayName -eq "$adminRoles" }
        $role = New-MgDirectoryRole -RoleTemplateId $template.Id
    }
    New-MgDirectoryRoleMemberByRef -DirectoryRoleId $role.Id -BodyParameter @{
    "@odata.id" = "https://graph.microsoft.com/v1.0/directoryObjects/$($user.Id)"
    }
}
Write-host "$($user.UserPrincipalName) has been created with following roles: $adminRoles"
