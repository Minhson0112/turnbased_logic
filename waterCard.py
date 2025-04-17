from cardBase import Card

class WaterCard(Card):
    def special_skills(self):
        print(f"{self.name} kích hoạt kỹ năng đặc biệt hệ Thủy! 💧")

        alive_allies = [c for c in self.team if c.is_alive()]
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        # Tính sẵn các giá trị buff
        heal = int(self.base_damage * 3)
        armor_buff = int(self.base_damage * 2)
        damage_buff = int(self.base_damage * 0.3)

        if self.tier == "Genin":
            target = min(alive_allies, key=lambda c: c.health, default=None)
            if target:
                target.health = min(target.health + heal, target.max_health)
                print(f"👉 {target.name} được hồi {heal} máu!")

        elif self.tier == "Chunin":
            targets = sorted(alive_allies, key=lambda c: c.health)[:2]
            for target in targets:
                target.health = min(target.health + heal, target.max_health)
                print(f"👉 {target.name} được hồi {heal} máu!")

        elif self.tier == "Jounin":
            targets = sorted(alive_allies, key=lambda c: c.health)[:2]
            for target in targets:
                target.health = min(target.health + heal, target.max_health)
                target.armor += armor_buff
                print(f"👉 {target.name} được hồi {heal} máu và buff {armor_buff} giáp!")

        elif self.tier == "Kage":
            for target in alive_allies:
                target.health = min(target.health + heal, target.max_health)
                target.armor += armor_buff
                print(f"⚔️ {target.name} được hồi {heal} máu, buff {armor_buff} giáp!")

        elif self.tier == "Legendary":
            for target in alive_allies:
                target.health = min(target.health + heal, target.max_health)
                target.armor += armor_buff
                target.base_damage += damage_buff
                print(f"🌟 {target.name} được hồi {heal} máu, buff {armor_buff} giáp và tăng {damage_buff} damage!")

        else:
            print(f"{self.name} không có kỹ năng đặc biệt phù hợp.")
