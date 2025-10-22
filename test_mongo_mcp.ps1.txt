# test_mongo_mcp.ps1

# 1. List first 5 students
Write-Host "`nListing first 5 students:"
$students = Invoke-RestMethod -Uri "http://localhost:8000/students?limit=5"
$students | Format-Table student_id, first_name, last_name, age, active

# 2. Insert a new student
Write-Host "`nInserting a new student..."
$newStudent = @{
    student_id = "S999"
    first_name = "Test"
    last_name  = "User"
    age        = 21
    scores     = @{ math=90; cs=88; db=93 }
    active     = $true
}
$response = Invoke-RestMethod -Uri "http://localhost:8000/students" `
    -Method POST `
    -Headers @{'Content-Type'='application/json'} `
    -Body ($newStudent | ConvertTo-Json -Compress)
Write-Host "Inserted ID:" $response.inserted_id

# 3. Get the inserted student
Write-Host "`nFetching the inserted student..."
$student = Invoke-RestMethod -Uri "http://localhost:8000/students/$($response.inserted_id)"
$student | Format-Table student_id, first_name, last_name, age

# 4. Update the student age
Write-Host "`nUpdating the student's age to 22..."
$update = @{ age = 22 }
Invoke-RestMethod -Uri "http://localhost:8000/students/$($response.inserted_id)" `
    -Method PATCH `
    -Headers @{'Content-Type'='application/json'} `
    -Body ($update | ConvertTo-Json -Compress)

# 5. Fetch again to verify update
$student = Invoke-RestMethod -Uri "http://localhost:8000/students/$($response.inserted_id)"
Write-Host "`nUpdated student:"
$student | Format-Table student_id, first_name, last_name, age

# 6. Delete the student
Write-Host "`nDeleting the student..."
Invoke-RestMethod -Uri "http://localhost:8000/students/$($response.inserted_id)" `
    -Method DELETE

Write-Host "`nStudent deleted."

# 7. Fetch MCP metadata
Write-Host "`nFetching MCP metadata..."
$mcp = Invoke-RestMethod -Uri "http://localhost:8000/mcp"
$mcp | ConvertTo-Json | Write-Host
