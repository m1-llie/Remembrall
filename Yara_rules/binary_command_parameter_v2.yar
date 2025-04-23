rule binary_command_parameter_monitor_v2
{
    meta:
        description = "help detect the use of native living-off-the-land binaries to prevent rollback v2"
        last_modified = "2024-06-23"
    strings:
        $binaries = "vssadmin|wmic|wbadmin|bcdedit|powershell|diskshadow|fsutil" nocase
        $commands = "delete|resize|catalog|backup|systemstatebackup|recoveryenabled|ignoreallfailures|win32_shadowcopy|-version|/version|-e|/e|usn deletejournal" nocase
        $parent_checks = "ParentName=\"Termius.exe\"|ParentExecutablePath=\"C:\\Program Files\\WindowsApps\\" nocase
    condition:
        for any $b in ($binaries) : ( 
            $b and any of ($commands)
        ) and not any of ($parent_checks)
}