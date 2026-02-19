# Fix Healthcare Knowledge Base Filename
# Run this in HAWCC/Windows if you have healthcare.kb.yaml instead of healthcare-kb.yaml

Write-Host "Checking for incorrectly named file..." -ForegroundColor Yellow

if (Test-Path "knowledge/healthcare.kb.yaml") {
    Write-Host "Found: knowledge/healthcare.kb.yaml (INCORRECT - has dot instead of dash)" -ForegroundColor Red
    Write-Host "Renaming to: knowledge/healthcare-kb.yaml" -ForegroundColor Yellow
    Move-Item "knowledge/healthcare.kb.yaml" "knowledge/healthcare-kb.yaml"
    Write-Host "✅ Fixed!" -ForegroundColor Green
} else {
    Write-Host "File not found: knowledge/healthcare.kb.yaml" -ForegroundColor Gray
}

if (Test-Path "knowledge/healthcare-kb.yaml") {
    Write-Host "✅ Correct file exists: knowledge/healthcare-kb.yaml" -ForegroundColor Green
} else {
    Write-Host "❌ Missing: knowledge/healthcare-kb.yaml" -ForegroundColor Red
    Write-Host "Please ensure this file exists" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Listing all knowledge base files:" -ForegroundColor Cyan
Get-ChildItem knowledge/
