from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
import os
from pydub import AudioSegment
import elevenlabs
from io import BytesIO
import speech_recognition as sr

from process2 import process_text
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

from database import User, Appointment, Availability

# @app.before_request
# def before_first_request():
#      db.create_all()




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            session['user_type'] = user.user_type
            session['user_id'] = user.id
            return redirect(url_for(user.user_type, username=user.username))
        else:
            return 'Invalid username or password'

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['userType']
        
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return 'Username already exists'
        else:
            new_user = User(fullname=fullname, username=username, password=password, user_type=user_type)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/doctor/add_availability', methods=['GET', 'POST'])
def doctor():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    doctor_id = session.get('user_id')

    if request.method == 'POST':
        if 'remove' in request.form:  # Check if we're removing availability
            availability_id = request.form['remove']
            availability = Availability.query.get(availability_id)
            if availability and availability.doctor_id == doctor_id:
                db.session.delete(availability)
                db.session.commit()
                return 'Availability removed!'
        else:  # Adding a new availability
            day = request.form['day']
            start_time = request.form['start_time']
            end_time = request.form['end_time']

            if doctor_id:
                new_availability = Availability(doctor_id=doctor_id, day=day, start_time=start_time, end_time=end_time)
                db.session.add(new_availability)
                db.session.commit()
                return 'Availability added!'
            else:
                return 'Doctor not logged in', 403

    # Retrieve existing availabilities to display
    availabilities = Availability.query.filter_by(doctor_id=doctor_id).all()
    return render_template('doctor.html', username=username, availabilities=availabilities)



@app.route('/patient/<username>')
def patient(username):
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))
    return render_template('patient.html', username=username)

@app.route('/signout', methods=['POST'])
def signout():
    # Clear session data to sign out the user
    session.clear()
    return redirect(url_for('login'))


@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio part in the request'}), 400

    audio = request.files['audio']
    if audio.filename == '':
        return jsonify({'error': 'No selected file'}), 400


    user_id = session['user_id']
    audio_bytes = audio.read()

    # Convert the audio data into a BytesIO object
    audio_stream = BytesIO(audio_bytes)

    audio_stream.seek(0) 


    # Load the audio stream using pydub
    audio_file = AudioSegment.from_file(audio_stream)

    # Export the audio to WAV format (required by speech_recognition)
    wav_audio_stream = BytesIO()
    audio_file.export(wav_audio_stream, format="wav")

    # Reset the stream position to the beginning
    wav_audio_stream.seek(0)

    # Perform speech recognition on the WAV audio stream
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_audio_stream) as source:
        audio_data = recognizer.record(source)
    

    response_text = ""
    # Perform speech recognition
    try:
        text = recognizer.recognize_google(audio_data)
        print("Recognized text:", type(text), text)

        response_text = process_text(text, user_id)

        print(response_text,"result")
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


    # Convert response text to audio
    tts_bytes = elevenlabs.generate(api_key=os.getenv("ELEVEN_LABS_KEY"), text=response_text, voice="Alice")

    # Create a BytesIO object and write the audio data to it.
    audio_fp = BytesIO(tts_bytes)

    # Rewind the buffer to the beginning.
    audio_fp.seek(0)

    # Return the audio file in the response.
    return send_file(
        audio_fp,
        mimetype='audio/mp4',
        as_attachment=True,
        download_name='processed_audio.mp4'
    )


if __name__ == '__main__':
    app.run()
