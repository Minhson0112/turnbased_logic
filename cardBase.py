class Card:
    def __init__(self, name, health, armor, base_damage, crit_rate, speed, chakra, position, element, tier):
        self.name = name
        self.health = health
        self.max_health = health
        self.armor = armor
        self.base_damage = base_damage
        self.crit_rate = crit_rate
        self.speed = speed
        self.chakra = chakra
        self.position = position
        self.element = element
        self.tier = tier
        self.target = None
        self.team = None
        self.enemyTeam = None

    def is_alive(self):
        return self.health > 0

    def health_bar(self, bar_length=20):
        ratio = self.health / self.max_health if self.max_health else 0
        filled = int(ratio * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        return f"HP: [{bar}] {self.health}/{self.max_health}"

    def __str__(self):
        return (f"Card(name={self.name}, {self.health_bar()}, armor={self.armor}, "
                f"base_damage={self.base_damage}, crit_rate={self.crit_rate}, speed={self.speed}, "
                f"chakra={self.chakra}, position={self.position}, element={self.element})")
