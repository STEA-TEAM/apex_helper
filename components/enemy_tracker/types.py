class PID:
    def __init__(self, kp, ki, kd):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.integral = 0
        self.previous_error = 0

    def compute(self, bias: float, dt: float) -> float:
        self.integral += bias * dt
        derivative = (bias - self.previous_error) / dt
        output = self.Kp * bias + self.Ki * self.integral + self.Kd * derivative
        self.previous_error = bias
        return float(output)



