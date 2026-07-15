from services.config.workout_config import PROMPT

from groq import RateLimitError, APIError


class LLMCoach:
    def __init__(self, groq_client):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT

    def give_feedback(self, event, issue):
        prompt = f"Event: {event}"

        if issue:
            prompt += f" Form Issue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-4:],
            {"role": "user", "content": prompt},
        ]

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.4,
            )

            text = response.choices[0].message.content.strip()

            self.history.append({
                "role": "assistant",
                "content": text,
            })

            return text

        except RateLimitError:
            return self._fallback_feedback(event, issue)

        except APIError:
            return self._fallback_feedback(event, issue)

        except Exception:
            return self._fallback_feedback(event, issue)

    def _fallback_feedback(self, event, issue):
        if event == "workout_started":
            return "Workout started. Stay controlled and focus on proper form."

        if event == "set_completed":
            return "Set complete. Take a breath and prepare for the next set."

        if event == "workout_completed":
            return "Workout complete. Great work today."

        if event == "no_pose_detected":
            return "Step into the camera frame so I can track your movement."

        if event == "ongoing_form_check" and issue:
            return f"Check your form. {issue}"

        return "Stay controlled and keep going."