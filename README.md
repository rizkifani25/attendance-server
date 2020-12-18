<h1 align="center"> Attendance Server </h1>
<h3 align="center"> Python Face Recognition API </h3>

### *Run on : 127.0.0.1*

### *Requirements*
```text
python 3.8
```

### *How to Run*
```text
pip install -r requirements.txt
py server.py
```

### *Config*
```json
{
    "port":15000,
    "firebaseConfig": "YOUR_FIREBASE_CREDENTIAL",
    "download_path": "YOUR_DOWNLOAD_PATH"
}
```

### *How to request*
- Method
```text
POST
```
- Endpoint
```text
- /validate
- /test
```

- Body
```json
{
    "room_id": "55-B101",
    "student_id": "1",
    "is_out": false
}
```
