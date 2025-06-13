## Azure Migrate Analyzer (Azure Web App Version)

### 🚀 Features
- Upload Azure Migrate assessment Excel file
- Automatically analyze and recommend migration paths
- Export as Excel and CSV for Power BI

### 🧱 Run Locally
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

### ☁️ Azure Web App Deployment (No Docker)

1. Go to Azure Portal > App Services > Create a new **Web App**
   - Runtime: Python 3.11
   - Region: Your preferred region
   - Linux recommended

2. **Deployment Method**:
   - Use **Deployment Center** to connect GitHub repo or upload ZIP
   - Or use **VS Code Azure Tools** for direct deploy

3. **App Configuration**:
   - Flask will run on `0.0.0.0:8000` by default

4. **Access your site and upload assessments**
