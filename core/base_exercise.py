from abc import ABC,abstractmethod
from collections import deque
import math
class BaseExercise(ABC):
    ANGLE_DELTA_THRESHOLD = 3
    MIN_CONFIRM_FRAMES = 3

    def __init__(self):
        self.reps=0
        self.stage=None
         # Motion tracking
        self.angle_history = deque(maxlen=5)
        self.previous_angle = None
        self.movement = "STABLE"
         # Frame confirmation
        self.down_frames = 0
        self.up_frames = 0
    
    def calculate_angle(self, a, b, c) -> float:
        ax,ay=a[0]-b[0],a[1]-b[1]
        cx,cy=c[0]-b[0],c[1]-b[1]

        dot=ax*cx + ay*cy

        mag_a=math.sqrt(ax**2 + ay**2)
        mag_c=math.sqrt(cx**2 + cy**2)

        if mag_a==0 or mag_c==0:
            return 0

        cos_angle=max(-1,min(1,dot/(mag_a*mag_c)))

        return math.degrees(math.acos(cos_angle))

    def smooth_angle(self, angle: float) -> float:
        """Return a temporally smoothed joint angle."""

        self.angle_history.append(angle)
        return sum(self.angle_history) / len(self.angle_history)
    
    def update_movement(self, angle: float) -> str:
        """Update movement direction based on angle change."""

        if self.previous_angle is not None:
            delta = angle - self.previous_angle

            if delta < -self.ANGLE_DELTA_THRESHOLD:
                self.movement = "DESCENDING"

            elif delta > self.ANGLE_DELTA_THRESHOLD:
                self.movement = "ASCENDING"

            else:
                self.movement = "STABLE"

        self.previous_angle = angle

        return self.movement
    
    def reset_tracking(self):
        self.reps = 0
        self.stage = None

        self.angle_history.clear()
        self.previous_angle = None
        self.movement = "STABLE"

        self.down_frames = 0
        self.up_frames = 0

    

    def get_point(self,landmarks,idx):
        p=landmarks[idx]
        return (p.x,p.y) 
    
    @abstractmethod
    def process(self,landmarks):
        pass

    @abstractmethod
    def reset(self):
        pass