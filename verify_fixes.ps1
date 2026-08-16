# Verification script for AI Code Review Agent
# Run from the project root: .\verify_fixes.ps1
# Prints PASS/FAIL for every fix applied during this session.

$ErrorActionPreference = "SilentlyContinue"

function Check-File {
    param($Path, $Pattern, $Label)

    if (-not (Test-Path $Path)) {
        Write-Host "[MISSING FILE] $Label -> $Path does not exist" -ForegroundColor Red
        return
    }

    $found = Select-String -Path $Path -Pattern $Pattern -SimpleMatch

    if ($found) {
        Write-Host "[PASS] $Label" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $Label -> pattern not found in $Path" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Config-driven severity / no hardcoding ===" -ForegroundColor Cyan
Check-File "modules\severity.py" "def normalize_finding_fields" "severity.py has field normalization"
Check-File "modules\severity.py" "def get_severity_weights" "severity.py has shared weight loader"
Check-File "modules\severity.py" "def tag_owasp_category" "severity.py has OWASP tagging"
Check-File "modules\score_calculator.py" "from modules.severity import get_severity_weights" "score_calculator.py exists"
Check-File "database\repository.py" "from modules.score_calculator import calculate_score" "repository.py uses shared score calculator"
Check-File "ui\dashboard.py" "from modules.score_calculator import calculate_score" "dashboard.py uses shared score calculator"
Check-File "tools\pmd_runner.py" "_load_priority_map" "pmd_runner.py is config-driven"
Check-File "tools\spotbugs_runner.py" "_load_priority_map" "spotbugs_runner.py is config-driven"
Check-File "tools\pylint_runner.py" "_load_severity_map" "pylint_runner.py is config-driven"
Check-File "tools\radon_runner.py" "_load_severity_map" "radon_runner.py is config-driven"
Check-File "tools\java_quality_analyzer.py" "_load_severity_map" "java_quality_analyzer.py is config-driven"

Write-Host ""
Write-Host "=== Orchestrator ===" -ForegroundColor Cyan
Check-File "agents\orchestrator.py" "for finding in code_findings" "orchestrator.py tags default agent labels"
Check-File "agents\orchestrator.py" "logger.info" "orchestrator.py uses logging, not print()"

Write-Host ""
Write-Host "=== Database / Auth / Sessions ===" -ForegroundColor Cyan
Check-File "database\models.py" "CREATE TABLE IF NOT EXISTS sessions" "models.py has sessions table"
Check-File "database\models.py" "name          TEXT" "models.py has name column on users"
Check-File "database\auth.py" "def create_session" "auth.py has persistent session support"
Check-File "database\auth.py" "name: str = " "auth.py create_user accepts a name"
Check-File "ui\signup.py" "st.text_input(""Name"")" "signup.py collects a name"

Write-Host ""
Write-Host "=== Navigation / History restore ===" -ForegroundColor Cyan
Check-File "ui\sidebar.py" "nav_override" "sidebar.py supports forced navigation"
Check-File "ui\history.py" "force_page" "history.py forces navigation on restore"
Check-File "app.py" "force_page" "app.py applies forced navigation"

Write-Host ""
Write-Host "=== Chat embedded on review page (no separate AI Assistant page) ===" -ForegroundColor Cyan
Check-File "ui\review_page.py" "render_assistant_page" "review_page.py embeds the chat"
Check-File "ui\sidebar.py" "AI Assistant" "sidebar.py should NOT list AI Assistant (checking absence)"
if ((Select-String -Path "ui\sidebar.py" -Pattern "AI Assistant" -SimpleMatch)) {
    Write-Host "[FAIL] sidebar.py still lists a separate AI Assistant page" -ForegroundColor Red
} else {
    Write-Host "[PASS] sidebar.py has no separate AI Assistant page" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Dashboard redesign ===" -ForegroundColor Cyan
Check-File "ui\dashboard.py" "render_radar_chart" "dashboard.py has radar chart"
Check-File "ui\dashboard.py" "render_owasp_coverage" "dashboard.py has OWASP coverage widget"
if ((Select-String -Path "ui\dashboard.py" -Pattern "render_severity_pie" -SimpleMatch)) {
    Write-Host "[FAIL] dashboard.py still has the pie chart (should be removed)" -ForegroundColor Red
} else {
    Write-Host "[PASS] dashboard.py pie chart removed" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Reports page (PDF only) ===" -ForegroundColor Cyan
if ((Select-String -Path "ui\report_page.py" -Pattern "Download Findings \(JSON\)" -SimpleMatch)) {
    Write-Host "[FAIL] report_page.py still has JSON export (should be removed)" -ForegroundColor Red
} else {
    Write-Host "[PASS] report_page.py JSON export removed" -ForegroundColor Green
}
if ((Select-String -Path "ui\report_page.py" -Pattern "Download Findings \(CSV\)" -SimpleMatch)) {
    Write-Host "[FAIL] report_page.py still has CSV export (should be removed)" -ForegroundColor Red
} else {
    Write-Host "[PASS] report_page.py CSV export removed" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Conversational assistant signature ===" -ForegroundColor Cyan
Check-File "agents\conversational_assistant.py" "chat_history: list" "conversational_assistant.py has correct ask() signature"

Write-Host ""
Write-Host "=== Python security rules (severity standard + new rules) ===" -ForegroundColor Cyan
Check-File "knowledge_base\python_security_rules.json" "PY-AUTH-001" "python_security_rules.json has Insecure Authentication rule"
Check-File "knowledge_base\python_security_rules.json" "PY-ACCESS-001" "python_security_rules.json has Broken Access Control rule"
$sqlCritical = Select-String -Path "knowledge_base\python_security_rules.json" -Pattern '"id": "PY-SQL-001"' -Context 0,3
if ($sqlCritical -match "CRITICAL") {
    Write-Host "[PASS] SQL Injection severity is CRITICAL" -ForegroundColor Green
} else {
    Write-Host "[FAIL] SQL Injection severity is not CRITICAL" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Config files exist ===" -ForegroundColor Cyan
$configFiles = @(
    "severity_map.json", "severity_weights.json", "owasp_map.json",
    "pmd_priority_map.json", "spotbugs_priority_map.json",
    "pylint_severity_map.json", "radon_severity_map.json",
    "java_quality_severity.json", "risk_thresholds.json"
)
foreach ($f in $configFiles) {
    if (Test-Path "config\$f") {
        Write-Host "[PASS] config\$f exists" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] config\$f is MISSING" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Done. Review any [FAIL] or [MISSING FILE] lines above. ===" -ForegroundColor Cyan
Write-Host ""