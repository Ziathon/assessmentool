from flask import Flask, request, render_template, send_file
import pandas as pd
import os
from logic import recommend_migration

app = Flask(__name__)
UPLOAD_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(file, sheet_name='All_Assessed_Machines')

            df.columns = df.columns.str.strip()
            df['CPU usage(%)'] = pd.to_numeric(df['CPU usage(%)'], errors='coerce')
            df['Memory usage(%)'] = pd.to_numeric(df['Memory usage(%)'], errors='coerce')
            df['Confidence Rating (% of utilization data collected)'] = pd.to_numeric(
                df['Confidence Rating (% of utilization data collected)'], errors='coerce')

            recommendations, notes = [], []
            for _, row in df.iterrows():
                rec, note = recommend_migration(row)
                recommendations.append(rec)
                notes.append(note)

            df['Recommended Migration Path'] = recommendations
            df['Notes'] = notes

            output_path = os.path.join(UPLOAD_FOLDER, 'Migration_Results.xlsx')
            csv_path = os.path.join(UPLOAD_FOLDER, 'Migration_Results.csv')
            df.to_excel(output_path, index=False)
            df.to_csv(csv_path, index=False)

            return render_template('index.html', tables=[df.to_html(classes='data')],
                                   download_link='Migration_Results.xlsx',
                                   csv_link='Migration_Results.csv')
        else:
            return 'Please upload a valid .xlsx file from Azure Migrate.'

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
