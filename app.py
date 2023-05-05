from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

parking_data = {}  # in-memory database

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entry', methods=['POST'])
def entry():
    plate = request.form['plate']
    parking_lot = request.form['parkingLot']
    ticket_id = len(parking_data) + 1  # generate unique ticket id
    parking_data[ticket_id] = {
        'plate': plate,
        'parking_lot': parking_lot,
        'entry_time': datetime.datetime.now(),
        'exit_time': None,
        'charge': None
    }
    return jsonify({'ticketId': ticket_id})

@app.route('/exit', methods=['POST'])
def exit():
    ticket_id = int(request.form['ticketId'])
    if ticket_id not in parking_data:
        return jsonify({'error': 'Ticket not found'}), 404
    ticket = parking_data[ticket_id]
    if ticket['exit_time'] is not None:
        return jsonify({'error': 'Ticket already used'}), 400
    ticket['exit_time'] = datetime.datetime.now()
    parked_time = (ticket['exit_time'] - ticket['entry_time']).total_seconds() / 60  # minutes
    charge = int(parked_time / 15) * 2  # 2 dollars per 15 minutes
    ticket['charge'] = charge
    return jsonify({
        'plate': ticket['plate'],
        'parked_time': parked_time,
        'parking_lot': ticket['parking_lot'],
        'charge': charge
    })

if __name__ == '__main__':
    app.run()
