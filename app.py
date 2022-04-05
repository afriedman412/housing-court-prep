from flask import Flask, request, render_template, send_file
import zipfile
import pandas as pd
from helpers import q, format_queries

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('form.html')

@app.route('/search', methods=["GET"])
def search_endpoint():
    case_name = request.args.get('case_name')
    house_number = request.args.get('house_number')
    street_name = request.args.get('street_name')
    boro = request.args.get('boro')

    full_address = f"{house_number} {street_name}, {boro}"

    jsons, params =format_queries(house_number, street_name, boro)

    with zipfile.ZipFile(f'{case_name}.zip', 'w') as case_zip:

        page_data = {}

        for k in jsons.keys():
            try:
                json_ = jsons[k]
                params_ = params[k]

            except KeyError:
                continue

            r = q(json_, params_)
            if r.status_code == 200:
                print(k, len(r.json()))

                if k == 'acris':
                    documents = []
                    doc_ids = [d['document_id'] for d in r.json()]
                    for d in set(doc_ids):
                        params_ = {'document_id':d}
                        r = q(json_, params_)
                        if r.status_code == 200:
                            documents += r.json()
                    # page_data['documents'] = documents
                    # pd.DataFrame(documents).to_csv(f"{case_name}_documents.csv")
                    print("acris docs:", len(documents))
                    if documents:
                        case_zip.writestr(
                            f"{case_name}_documents.csv", 
                            pd.DataFrame(documents).to_csv())

                # page_data[k] = r.json()
                # pd.DataFrame(r.json()).to_csv(f"{case_name}_{k}.csv")
                if r.content:
                    case_zip.writestr(
                        f"{case_name}_{k}.csv", 
                        pd.DataFrame(r.json()).to_csv())


    return send_file(f'{case_name}.zip',
                 mimetype='zip',
                 attachment_filename=f'{case_name}.zip',
                 as_attachment=True)

if __name__ == "__main__":
    app.run()
 
