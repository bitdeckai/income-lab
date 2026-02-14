param(
  [Parameter(Mandatory=$true)]
  [string]$LogPath
)

if (-not (Test-Path $LogPath)) {
  Write-Error "Log file not found: $LogPath"
  exit 1
}

$log = Get-Content $LogPath -Raw
$checks = @(
  @{ Name = 'BLE advertising started'; Pattern = 'BLE|advertis' },
  @{ Name = 'Commissioning completed'; Pattern = 'commission|pairing complete|fabric' },
  @{ Name = 'IP assigned'; Pattern = 'IP|DHCP|network up' }
)

Write-Host "Matter commissioning quick diagnostics"
$failed = 0

foreach ($c in $checks) {
  if ($log -match $c.Pattern) {
    Write-Host "[PASS] $($c.Name)"
  } else {
    Write-Host "[FAIL] $($c.Name)"
    $failed++
  }
}

if ($failed -gt 0) {
  Write-Host "Result: NEEDS INVESTIGATION ($failed checks failed)"
  exit 2
}

Write-Host "Result: BASIC CHECKS PASSED"
exit 0
