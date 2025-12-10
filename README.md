# SARIF Test Repo (CS 5599 Project 2)

This repository demonstrates generating and uploading SARIF results from Safety dependency scans. It uses intentionally vulnerable Python dependencies in `vulnerable-app` so the scan produces findings you can inspect in GitHub code scanning.

## Repository Layout

- `vulnerable-app/app.py`: Tiny demo that prints versions of intentionally outdated libs.
- `vulnerable-app/requirements.txt`: The vulnerable dependency list used for scanning.
- `.github/workflows/security-scan.yml`: GitHub Actions workflow that runs Safety, converts results to SARIF via an action, and uploads to code scanning.
- `safety.json` and `safety-results.sarif`: Sample outputs from the latest scan (JSON and SARIF artifacts you can inspect or re-upload).
- `screenshots/placeholder.png`: Placeholder for screenshots showing the integration working (e.g., GitHub code scanning alerts).

## Intentional Vulnerabilities (educational only)

The demo app pins old versions to guarantee findings:

- `flask==1.0.2` (multiple CVEs fixed in later 2.x/3.x releases)
- `django==1.11.0` (end-of-life; dozens of auth/XSS/CSRF fixes in later versions)
- `pyyaml==5.1` (unsafe load issues fixed in >=5.4/6.x)
- `requests==2.19.1` (redirect header handling, auth leaks; fixed in 2.32.x)
- `cryptography==2.3` (multiple crypto/ASN.1 parsing fixes; fixed in 3.x+ and 4.x+)

These are deliberately unpatched so Safety produces warnings for demo purposes.

## Prerequisites

- Python 3.11  
- Optional virtual environment:  
  ```sh
  python -m venv .venv
  source .venv/bin/activate     # Linux/macOS
  .\.venv\Scripts\activate      # Windows
  ```
- Safety CLI (`pip install safety==3.7.0`)
- GitHub secret `SAFETY_API_KEY` for CI workflow authentication

## Setup & Usage

### 1) Install vulnerable app dependencies (optional)
```sh
pip install -r vulnerable-app/requirements.txt
```

### 2) Install Safety
```sh
pip install safety==3.7.0
```

### 3) Run the demo script (prints vulnerable versions)
```sh
python vulnerable-app/app.py
```

### 4) Run Safety locally and capture JSON output
```sh
safety scan --full-report --file vulnerable-app/requirements.txt --output json > safety.json
```

### 5) Convert to SARIF locally (optional)
You may use the same SARIF converter tool invoked by CI or rely on CI-generated `safety-results.sarif`.

---

## CI Workflow (GitHub Actions)

**Triggers:**  
- `push`  
- `pull_request`

**Workflow steps:**  
1. Checkout repository  
2. Set up Python 3.11  
3. Install Safety (`safety==3.7.0` recommended)  
4. Run Safety:  
   ```sh
   safety scan --output json > safety.json
   ```  
   (authenticated with `SAFETY_API_KEY`)
5. Convert JSON → SARIF using `kramandr/safety-sarif-action`
6. Upload SARIF to GitHub code scanning via `github/codeql-action/upload-sarif@v3`

**Required secret:**  
- `SAFETY_API_KEY`

**Actions used:**  
- Safety CLI  
- SARIF conversion (`kramandr/safety-sarif-action`)  
- SARIF upload (`github/codeql-action/upload-sarif`)

---

## Viewing Results

After CI completes:

- Navigate to **Security → Code scanning alerts** to view Safety findings.
- You can also open `safety-results.sarif` locally in:
  - VS Code (SARIF Viewer extension)
  - Any SARIF-compatible viewer

---

## Updating / Remediating

Vulnerabilities are intentionally present for demonstration.  
To reduce findings:

1. Update versions in `vulnerable-app/requirements.txt` to recommended secure versions.
2. Re-run Safety or push a commit to trigger CI.

---

## Screenshots

The `screenshots/` directory contains example images demonstrating how the SARIF workflow integrates with GitHub. These include:  
- Screenshots of the **workflow execution** in GitHub Actions, showing Safety running and the SARIF upload step.  
- The resulting **Code Scanning alerts** displayed in GitHub’s Security tab.  
- An **alert detail view**, illustrating how GitHub presents file/line information, metadata, and remediation guidance extracted from the SARIF file.
