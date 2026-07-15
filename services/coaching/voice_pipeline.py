import time
import streamlit as st


class VoicePipeline:
    FORM_FEEDBACK_COOLDOWN = 15
    REPEAT_ISSUE_COOLDOWN = 30

    def __init__(self, llm, tts):
        self.llm = llm
        self.tts = tts

        self.last_spoken_at = 0
        self.last_issue = None
        self.last_issue_spoken_at = 0

    def _find_form_issue(self, exercise, metrics):
        if "issue" in metrics:
            return metrics["issue"]

        if exercise == "Squats":
            depth = metrics.get("depth_status", "")
            back_angle = metrics.get("back_angle", 180)

            if depth == "SHALLOW DEPTH":
                return (
                    "The squat is slightly shallow. "
                    "Lower the hips a little more."
                )

            if isinstance(back_angle, (int, float)) and back_angle < 130:
                return (
                    "The user is leaning too far forward "
                    "during the squat."
                )

        elif exercise == "Push-ups":
            alignment = metrics.get("body_alignment", "")
            hip_status = metrics.get("hip_status", "")

            if alignment == "Poor Form":
                return (
                    "The user's body is not straight "
                    "during the push-up."
                )

            if hip_status == "SAGGING":
                return (
                    "The user's hips are sagging down "
                    "during the push-up."
                )

            if hip_status == "PIKED UP":
                return (
                    "The user's hips are too high. "
                    "Lower them to form a straight line."
                )

        elif exercise == "Biceps Curls (Dumbbell)":
            swing = metrics.get("swing_status", "")
            shoulder = metrics.get("shoulder_status", "")

            if swing == "SWINGING":
                return (
                    "The user is swinging their torso during "
                    "the curl. Keep the body still."
                )

            if shoulder == "ELBOW DRIFTING":
                return (
                    "The user's elbow is drifting away from "
                    "their side during the curl."
                )

        elif exercise == "Shoulder Press":
            symmetry = metrics.get("symmetry_status", "")
            extension = metrics.get("extension_status", "")

            if symmetry == "UNEVEN PRESS":
                return (
                    "The user's arms are pressing unevenly. "
                    "Keep both arms moving together."
                )

            

        elif exercise == "Lunges":
            torso_stability = metrics.get(
                "torso_stability",
                "",
            )

            if torso_stability == "LATERAL LEAN":
                return (
                    "The user is leaning sideways during the lunge — "
                    "keep the torso centered over the hips."
                )

        return None

    def process_event(self, event, exercise, metrics):
        issue = self._find_form_issue(exercise, metrics)

        now = time.time()

        is_major_event = event in [
            "workout_started",
            "set_completed",
            "workout_completed",
        ]

        is_form_event = event == "ongoing_form_check"

        if not is_major_event:
            if not issue:
                self.last_issue = None
                return None

            if now - self.last_spoken_at < self.FORM_FEEDBACK_COOLDOWN:
                return None

            if (
                issue == self.last_issue
                and now - self.last_issue_spoken_at
                < self.REPEAT_ISSUE_COOLDOWN
            ):
                return None

        text = self.llm.give_feedback(event, issue)

        if not text:
            return None

        voice = self.tts.speak(text)

        self.last_spoken_at = now

        if issue:
            self.last_issue = issue
            self.last_issue_spoken_at = now

        return voice, text


def autoplay_audio(audio_bytes):
    if not audio_bytes:
        return

    st.markdown(
        "<style>[data-testid='stAudio'] {display: none;}</style>",
        unsafe_allow_html=True,
    )

    st.audio(
        audio_bytes,
        format="audio/mp3",
        autoplay=True,
    )