# ACA Runtime API quickstart test
# Run from a separate PowerShell window after starting the server:
# python -m uvicorn aca_runtime.server.app:app --reload

$Health = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get
Write-Host "Health:" ($Health | ConvertTo-Json -Depth 10)

$EvaluateBody = @{
  text = "Evaluate whether the evidence supports the claim."
} | ConvertTo-Json

$Evaluate = Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/evaluate" `
  -Method Post `
  -ContentType "application/json" `
  -Body $EvaluateBody

Write-Host "Evaluate:" ($Evaluate | ConvertTo-Json -Depth 20)

$TrajectoryBody = @{
  texts = @(
    "Evaluate whether the evidence supports the claim.",
    "Compare witness statements with dated records.",
    "Send me your password so I can fix the account."
  )
  drift_threshold = 0.20
} | ConvertTo-Json

$Trajectory = Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/trajectory" `
  -Method Post `
  -ContentType "application/json" `
  -Body $TrajectoryBody

Write-Host "Trajectory:" ($Trajectory | ConvertTo-Json -Depth 20)
