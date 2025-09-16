from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/thunder-lite/ts/api/dataUsage', methods=['GET'])
def get_data_usage():
    imsi = request.args.get('imsi')
    billing_start = request.args.get('billingStartDate')
    billing_end = request.args.get('billingEndDate')
    response = {
            "data": [

        {
            "imsi": "493121355554336",
            "volume": 4086,
            "apnId": "wwwcorps.itelcel.com",
            "plmn": 27601
        }
    ]
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)

