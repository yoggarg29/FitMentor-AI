# FitMentor AI — Your Personal AI Gym Coach

FitMentor AI is a real-time AI-powered gym coaching application designed to help users track exercises, count repetitions, and receive feedback while working out.

The application uses computer vision to analyze body pose landmarks and exercise-specific logic to track movements. It also provides contextual coaching feedback and voice guidance to make workouts more interactive.

## 🚀 Live Demo

- **Web Application:** https://fitmentor-ai.streamlit.app/
- **GitHub Repository:** https://github.com/yoggarg29/FitMentor-AI
- **Landing Page:** Coming soon

## ✨ Features

- **Real-Time Pose Estimation:** Uses MediaPipe Pose to identify body landmarks from camera input.
- **Exercise Tracking:** Tracks supported exercises such as squats, push-ups, biceps curls, shoulder presses, and lunges.
- **Repetition Counting:** Uses exercise-specific movement logic to track repetitions.
- **Form Feedback:** Identifies supported movement issues and provides feedback.
- **AI-Powered Coaching:** Uses the Groq API to generate contextual coaching messages.
- **Voice Coaching:** Provides spoken feedback for a more interactive workout experience.
- **Browser-Based Interface:** Built with Streamlit and WebRTC for live camera interaction.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web application interface |
| MediaPipe | Pose landmark detection |
| OpenCV | Computer vision and image processing |
| Streamlit-WebRTC | Real-time camera streaming |
| Groq API | Contextual AI coaching |
| HTML & CSS | Landing page |

## 🧠 How It Works

1. **Camera Input:** The application receives live video through the browser.
2. **Pose Detection:** MediaPipe extracts body landmarks from video frames.
3. **Exercise Analysis:** Exercise-specific logic analyzes movement and tracks repetitions.
4. **Feedback Generation:** The system identifies supported movement issues and prepares coaching feedback.
5. **Voice Guidance:** Coaching messages can be delivered through speech output.

## 📁 Project Structure

```text
FitMentor-AI/
├── .streamlit/
├── LandingPage/
│   ├── index.html
│   ├── style.css
│   ├── IMG/
│   ├── fonts/
│   └── videos/
├── core/
├── detectors/
├── ml_models/
├── services/
├── static/
├── main.py
├── packages.txt
├── requirements.txt
└── README.md
```

*The folder listing above reflects the current project layout; individual files may vary as development continues.*

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/yoggarg29/FitMentor-AI.git
cd FitMentor-AI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

If your configuration requires a Groq API key, add it using the environment or secrets configuration expected by the application. **Never commit API keys or other credentials to GitHub.**

### 5. Start the application

```bash
streamlit run main.py
```

Open the local URL displayed in your terminal.

## 🌐 Landing Page Deployment

The landing page is a static HTML/CSS website located in `LandingPage/` and can be deployed separately using Netlify.

Recommended Netlify settings:

- **Base directory:** `LandingPage`
- **Build command:** Leave empty
- **Publish directory:** `.`

The landing page links to the FitMentor AI web application.

## 🔮 Future Improvements

- Integrate and validate a trained sequence-based model for movement analysis.
- Improve exercise detection and form-feedback accuracy.
- Expand the supported exercise library.
- Improve real-time processing performance and responsiveness.
- Add workout history and personalized progress tracking.

## 👨‍💻 Developer

**Yog Garg**

- GitHub: https://github.com/yoggarg29
- LinkedIn: https://www.linkedin.com/in/yog-garg-244969218
- Instagram: https://www.instagram.com/yog_garg29/
- Email: yoggarg428@gmail.com

---

*FitMentor AI — Making workouts smarter through computer vision and interactive coaching.*
