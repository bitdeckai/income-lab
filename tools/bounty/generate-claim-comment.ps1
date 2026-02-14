param(
  [Parameter(Mandatory=$true)] [string]$IssueUrl,
  [Parameter(Mandatory=$true)] [string]$Plan,
  [string]$Eta = "24-48h"
)

@"
Hi, I'd like to claim this task: $IssueUrl

Plan:
$Plan

ETA: $Eta

I will submit a focused PR with tests and verification notes.
"@
