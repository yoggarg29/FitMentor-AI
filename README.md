# FitMentor AI — Your Personal AI Gym Coach

FitMentor AI is a real-time AI-powered gym coaching application designed to help users track exercises, count repetitions, and receive feedback while working out.

The application uses computer vision to analyze body pose landmarks and exercise-specific logic to track movements. It also provides contextual coaching feedback and voice guidance to make workouts more interactive.

## 🚀 Live Demo

- **Landing Page:** https://fit-mentor-ai.netlify.app/
- **Web Application:** https://fitmentor-ai.streamlit.app/
- **GitHub Repository:** https://github.com/yoggarg29/FitMentor-AI

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

*This is a high-level overview of the repository structure.*

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

### 4. Configure secrets

If the application requires a Groq API key, configure it through the environment or Streamlit secrets mechanism expected by the code.

**Never commit API keys, passwords, or other credentials to GitHub.**

### 5. Start the application

```bash
streamlit run main.py
```

Open the local URL displayed in your terminal.

## 🌐 Deployment

### Landing Page — Netlify

The static landing page is deployed separately on Netlify.

- **Live URL:** https://fit-mentor-ai.netlify.app/
- **Source directory:** `LandingPage/`
- **Build command:** None required for the static HTML/CSS site.
- **Publish directory:** `.` relative to the configured base directory.

### Web Application — Streamlit

The interactive gym coaching application is hosted separately on Streamlit Community Cloud.

- **Live URL:** https://fitmentor-ai.streamlit.app/

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
