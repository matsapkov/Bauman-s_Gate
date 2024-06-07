class Obstacle:
    def __init__(self, sign, foot_penalty, cavalry_penalty, shooting_penalty):
        self.symbol = sign
        self.unit_on_foot_penalty = foot_penalty
        self.unit_cavalry_penalty = cavalry_penalty
        self.unit_shooting_penalty = shooting_penalty