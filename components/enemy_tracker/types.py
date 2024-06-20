class PID:
    def __init__(self, kp: float, ki: float, kd: float):
        self.__kp = kp
        self.__ki = ki
        self.__kd = kd
        self.__integral = 0
        self.__last_bias = 0

    def compute(self, bias: float, dt: float) -> float:
        self.__integral += bias * dt
        derivative = (bias - self.__last_bias) / dt
        output = self.__kp * bias + self.__ki * self.__integral + self.__kd * derivative
        self.__last_bias = bias
        return float(output)

    def reset(self) -> None:
        self.__integral = 0
        self.__last_bias = 0


