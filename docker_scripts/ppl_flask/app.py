# app.py
from flask import Flask, render_template, request, jsonify
from utils import get_coordinates_from_address,get_petrol_pump_locations,nearest_pp_distance

app = Flask(__name__)

# Render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Handle form submission
@app.route('/get_coordinates', methods=['POST'])
def get_coordinates_route():
    # Get the address from the form
    address = request.form['address']
    
    # Get latitude and longitude using the Python function
    location,osmid = get_coordinates_from_address(address)
    
    data = {}
    data['latitude'] = location[0]
    data['longitude'] = location[1]    
    data['osmid'] = osmid
    data['address'] = address
    
    df,connection_status = nearest_pp_distance(address)
    data['connection_status'] = connection_status
    #data['pump_locations'] = df.to_json(orient="records")
    data['pump_locations'] = df.to_html()
    
    # Return the latitude and longitude
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
