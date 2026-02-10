# Smart Motion Detection Alert System – Trackster

A real-time smart surveillance system built using **Python**, **OpenCV**, and **Flask** that detects meaningful motion, automatically records video evidence, and sends instant alerts to a mobile phone while intelligently ignoring minor or irrelevant movements.

---

##  Features

###  Intelligent Motion Detection
- Uses background subtraction to detect real object/person movement  
- Ignores eye blinks, light flickers, camera noise, and small disturbances  
- Motion must persist across multiple frames before triggering alerts  

###  Automatic Video Recording
- Starts recording only when valid motion is detected  
- Stops recording automatically after motion ends  
- Saves timestamped evidence videos for later review  

###  Instant Alert System
- Captures a snapshot when motion is confirmed  
- Sends alert notifications to a mobile phone using **Twilio**  
- Cooldown mechanism prevents alert spam  

###  Web-Based Control Panel
- Start / Stop motion detection remotely  
- Simple and clean web interface built with Flask  

---

##  Tech Stack

- **Programming Language:** Python  
- **Computer Vision:** OpenCV  
- **Backend:** Flask  
- **Alerts & Messaging:** Twilio  
- **Image Hosting:** Cloudinary  
- **Frontend:** HTML, CSS  

---

##  Account Setup & Configuration

This project uses third-party services for alerts and image hosting.

---

###  Twilio Account (Alerts)

Twilio is used to send instant alert notifications when motion is detected.

**Steps:**
1. Create a free account at  https://www.twilio.com  
2. Verify your mobile number  
3. From the Twilio Console, collect:
   - Account SID  
   - Auth Token  
   - Twilio WhatsApp Sandbox number (or SMS-capable number)  
4. Enable WhatsApp Sandbox if you want WhatsApp alerts  

---

### 🖼️ Cloudinary Account (Image Hosting)

Cloudinary is used to host captured snapshot images sent in alerts.

**Steps:**
1. Create a free account at https://cloudinary.com  
2. Open the Cloudinary Dashboard  
3. Note down:
   - Cloud Name  
   - API Key  
   - API Secret  

---

##  Environment Configuration

Create a `.env` file in the project root and add:

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM=your_twilio_number
TWILIO_TO=your_verified_mobile_number

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```
## How to Run
```bash
pip install -r requirements.txt
python app.py
```
##  How It Works

- Camera continuously monitors the environment  
- Background subtraction identifies meaningful motion  
- Minor movements are filtered using contour area thresholds  

**When motion is confirmed:**
-  Video recording starts automatically  
-  A snapshot is captured  
-  Alert is sent to the registered mobile number  

Recording stops automatically once motion ends.

---
