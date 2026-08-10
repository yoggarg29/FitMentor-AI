import time
import streamlit as st


class VoicePipeline:
    FORM_FEEDBACK_COOLDOWN = 15
    ISSUE_CONFIRMATION_TIME = 1.5

    def __init__(self, llm, tts):
        self.llm = llm
        self.tts = tts

        self.last_spoken_at = 0

        # Current issue waiting for confirmation
        self.candidate_issue = None
        self.candidate_since = None

        # Issue that has already been warned about
        self.active_issue = None

    def _create_issue(
        self,
        code,
        description,
        severity=2,
        confidence=None,
    ):
        return {
            "code": code,
            "description": description,
            "severity": severity,
            "confidence": confidence,
        }

    def _find_form_issue(self, exercise, metrics):

        if "issue" in metrics:
            return self._create_issue(
                "SYSTEM_ISSUE",
                metrics["issue"],
                severity=3,
            )

        if exercise == "Squats":

            depth = metrics.get("depth_status", "")
            back_angle = metrics.get("back_angle", 180)

            if depth == "SHALLOW DEPTH":
                return self._create_issue(
                    "SHALLOW_SQUAT",
                    "The squat is slightly shallow. Lower the hips a little more.",
                    severity=2,
                )

            if (
                isinstance(back_angle, (int, float))
                and back_angle < 130
            ):
                return self._create_issue(
                    "SQUAT_FORWARD_LEAN",
                    "The user is leaning too far forward during the squat.",
                    severity=2,
                )

        elif exercise == "Push-ups":

            alignment = metrics.get("body_alignment", "")
            hip_status = metrics.get("hip_status", "")

            if alignment == "Poor Form":
                return self._create_issue(
                    "PUSHUP_POOR_ALIGNMENT",
                    "The user's body is not straight during the push-up.",
                    severity=2,
                )

            if hip_status == "SAGGING":
                return self._create_issue(
                    "HIP_SAG",
                    "The user's hips are sagging down during the push-up.",
                    severity=3,
                )

            if hip_status == "PIKED UP":
                return self._create_issue(
                    "HIP_PIKE",
                    "The user's hips are too high. Lower them to form a straight line.",
                    severity=2,
                )

        elif exercise == "Biceps Curls (Dumbbell)":

            swing = metrics.get("swing_status", "")
            shoulder = metrics.get("shoulder_status", "")

            if swing == "SWINGING":
                return self._create_issue(
                    "TORSO_SWING",
                    "The user is swinging their torso during the curl. Keep the body still.",
                    severity=2,
                )

            if shoulder == "ELBOW DRIFTING":
                return self._create_issue(
                    "ELBOW_DRIFT",
                    "The user's elbow is drifting away from their side during the curl.",
                    severity=1,
                )

        elif exercise == "Shoulder Press":

            symmetry = metrics.get("symmetry_status", "")

            if symmetry == "UNEVEN PRESS":
                return self._create_issue(
                    "UNEVEN_PRESS",
                    "The user's arms are pressing unevenly. Keep both arms moving together.",
                    severity=2,
                )

        elif exercise == "Lunges":

            torso = metrics.get("torso_stability", "")

            if torso == "LATERAL LEAN":
                return self._create_issue(
                    "LUNGE_LATERAL_LEAN",
                    "The user is leaning sideways during the lunge. Keep the torso centered over the hips.",
                    severity=2,
                )

        return None

    def process_event(self, event, exercise, metrics):

        issue = self._find_form_issue(exercise, metrics)

        now = time.time()

        is_major_event = event in (
            "workout_started",
            "set_completed",
            "workout_completed",
        )

        if is_major_event:

            text = self.llm.give_feedback(event, None)

            if not text:
                return None

            voice = self.tts.speak(text)

            self.last_spoken_at = now

            return voice, text

        # -----------------------------
        # FORM COACHING
        # -----------------------------

        # No issue -> recovery
        if issue is None:

            self.candidate_issue = None
            self.candidate_since = None
            self.active_issue = None

            return None

        code = issue["code"]

        # Already warned about this issue.
        # Wait until user fixes it.
        if self.active_issue == code:
            return None

        # New candidate
        if self.candidate_issue != code:

            self.candidate_issue = code
            self.candidate_since = now

            return None

        # Still confirming
        if (
            now - self.candidate_since
            < self.ISSUE_CONFIRMATION_TIME
        ):
            return None

        # Global speech cooldown
        if (
            now - self.last_spoken_at
            < self.FORM_FEEDBACK_COOLDOWN
        ):
            return None

        text = self.llm.give_feedback(
            event,
            issue["description"],
        )

        if not text:
            return None

        voice = self.tts.speak(text)

        self.last_spoken_at = now

        self.active_issue = code

        self.candidate_issue = None
        self.candidate_since = None

        return voice, text


def autoplay_audio(audio_bytes):

    if not audio_bytes:
        return

    st.markdown(
        "<style>[data-testid='stAudio'] {display:none;}</style>",
        unsafe_allow_html=True,
    )

    st.audio(
        audio_bytes,
        format="audio/mp3",
        autoplay=True,
    )