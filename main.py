import time
import random
from fireCard import FireCard
from windCard import WindCard
from waterCard import WaterCard
from taijutsuCard import TaijutsuCard
from lightningCard import LightningCard
from earthCard import EarthCard
from cardBase import Card


ELEMENT_CLASS_MAP = {
    "Hỏa": FireCard,
    "Thủy": WaterCard,
    "Thổ": EarthCard,
    "Phong": WindCard,
    "Lôi": LightningCard,
    "Thể": TaijutsuCard
}

def create_card(name, health, armor, base_damage, crit_rate, speed, chakra, position, element, tier):
    card_class = ELEMENT_CLASS_MAP.get(element, Card)
    return card_class(name, health, armor, base_damage, crit_rate, speed, chakra, position, element, tier)

def get_default_target(enemy_team):
    for idx in range(3):  # hàng đầu -> giữa -> sau
        if enemy_team[idx].is_alive():
            return enemy_team[idx]
    return None

def battle_turn(attacker_team, enemy_team):
    for attacker in attacker_team:
        if not attacker.is_alive():
            continue

        if attacker.chakra >= 100:
            attacker.special_skills()
            attacker.chakra = 0
            continue

        target = attacker.target if attacker.target and attacker.target.is_alive() else get_default_target(enemy_team)
        if target:
            print(f"{attacker.name} tấn công {target.name}!")

            # Dodge check (speed là tỷ lệ thập phân)
            if random.random() < target.speed:
                print(f"  => {target.name} đã né tránh tấn công! (Tỷ lệ: {target.speed*100:.1f}%)")
                continue

            is_crit = random.random() < attacker.crit_rate
            multiplier = 2 if is_crit else 1
            damage = max(attacker.base_damage * multiplier - target.armor, 0)
            target.health = max(target.health - damage, 0)

            if is_crit:
                print(f"  => Chí mạng! Gây {damage} sát thương; {target.name} còn {target.health} máu.")
            else:
                print(f"  => Gây {damage} sát thương; {target.name} còn {target.health} máu.")
        else:
            print(f"Không có mục tiêu hợp lệ cho {attacker.name}.")
        time.sleep(2)

def is_team_alive(team):
    return any(card.is_alive() for card in team)

def increase_chakra(team):
    for card in team:
        if card.is_alive():
            card.chakra += 20

def get_team_total_speed(team):
    return sum(card.speed for card in team if card.is_alive())

def print_team_health(team, team_name):
    print(f"\nTeam {team_name} Health Status:")
    for card in team:
        print(f"{card.name}: {card.health_bar()}")

def simulate_battle(team1, team2):
    initial_speed_team1 = get_team_total_speed(team1)
    initial_speed_team2 = get_team_total_speed(team2)

    first_team, second_team = (team1, team2) if initial_speed_team1 >= initial_speed_team2 else (team2, team1)
    print(f"Team {'1' if first_team == team1 else '2'} sẽ tấn công trước trong toàn bộ trận battle.")

    turn = 1
    while is_team_alive(team1) and is_team_alive(team2):
        print(f"\n--- Turn {turn} ---")
        battle_turn(first_team, second_team)
        if not is_team_alive(second_team):
            print("Team bị tấn công đã bị tiêu diệt!")
            break

        print()
        battle_turn(second_team, first_team)
        if not is_team_alive(first_team):
            print("Team bị tấn công đã bị tiêu diệt!")
            break

        print_team_health(team1, "1")
        print_team_health(team2, "2")
        increase_chakra(team1)
        increase_chakra(team2)

        turn += 1

# === Khởi tạo cards với speed là phần trăm né tránh (dạng float từ 0.0 → 1.0) ===

card1 = create_card("Warrior", 2000, 30, 70, 0.2, 0.05, 20, "đầu", "Thủy", "Kage")     # 5% né tránh
card2 = create_card("Mage", 900, 10, 80, 0.3, 0.10, 40, "giữa", "Hỏa", "Legendary")      # 10%
card3 = create_card("Archer", 800, 13, 70, 0.25, 0.15, 50, "sau", "Phong", "Legendary")# 15%

card4 = create_card("Knight", 2100, 35, 30, 0.1, 0.08, 60, "đầu", "Thổ", "Jounin")      # 8%
card5 = create_card("Assassin", 850, 8, 85, 0.4, 0.20, 40, "sau", "Lôi", "Kage")       # 20%
card6 = create_card("Cleric", 1400, 12, 55, 0.15, 0.06, 0, "giữa", "Thể", "Jounin")      # 6%

team1 = [card1, card2, card3]
team2 = [card4, card5, card6]

for card in team1:
    card.team = team1
    card.enemyTeam = team2

for card in team2:
    card.team = team2
    card.enemyTeam = team1

simulate_battle(team1, team2)
