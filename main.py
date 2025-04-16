import time
import random  # Import module random để tính tỉ lệ chí mạng và dodge

# Giả sử rằng class Card đã được định nghĩa ở file khác hoặc có thể copy lại ở đây.
# Ở đây, chúng ta bổ sung thêm thuộc tính target để hỗ trợ trường hợp dùng skill đặc biệt.
class Card:
    def __init__(self, name, health, armor, base_damage, crit_rate, speed, chakra, position, element):
        self.name = name             # Tên của thẻ
        self.health = health         # Máu hiện tại của thẻ
        self.max_health = health     # Lưu lại max health để hiển thị thanh máu
        self.armor = armor           # Giáp giúp giảm sát thương
        self.base_damage = base_damage  # Damage cơ bản khi tấn công
        self.crit_rate = crit_rate   # Tỉ lệ chí mạng (ví dụ: 0.2 tức 20% cơ hội chí mạng)
        self.speed = speed           # Tốc độ của thẻ (cũng dùng để tính dodge nếu dưới 1; nếu không, dodge_rate = speed/100)
        self.chakra = chakra              # Chakra ban đầu mặc định là 0
        self.position = position     # Vị trí của thẻ (đầu, giữa, sau)
        self.element = element       # Hệ của thẻ (thủy, hỏa, thổ, phong, lôi, thể)
        self.target = None           # Thuộc tính target dùng khi dùng skill đặc biệt

    def is_alive(self):
        """Kiểm tra thẻ còn sống khi health > 0."""
        return self.health > 0

    def health_bar(self, bar_length=20):
        """Trả về chuỗi thanh máu theo định dạng HP: [██████░░░░] current/max."""
        ratio = self.health / self.max_health if self.max_health else 0
        filled_length = int(ratio * bar_length)
        empty_length = bar_length - filled_length
        bar = '█' * filled_length + '░' * empty_length
        return f"HP: [{bar}] {self.health}/{self.max_health}"

    def __str__(self):
        return (f"Card(name={self.name}, {self.health_bar()}, armor={self.armor}, "
                f"base_damage={self.base_damage}, crit_rate={self.crit_rate}, speed={self.speed}, "
                f"chakra={self.chakra}, position={self.position}, element={self.element})")


def get_default_target(enemy_team):
    """
    Chọn target mặc định trong team địch:
      - Kiểm tra theo thứ tự: index 0 (hàng đầu), index 1 (hàng giữa), index 2 (hàng sau).
      - Trả về thẻ đầu tiên còn sống (health > 0).
    """
    if enemy_team[0].is_alive():
        return enemy_team[0]
    elif enemy_team[1].is_alive():
        return enemy_team[1]
    elif enemy_team[2].is_alive():
        return enemy_team[2]
    else:
        return None


def battle_turn(attacker_team, enemy_team):
    """
    Mỗi thẻ trong attacker_team nếu còn sống sẽ tấn công một thẻ trong enemy_team.
      - Nếu thẻ attacker có thuộc tính target (được thiết lập bởi skill đặc biệt) và target đó còn sống,
        thì tấn công target đó.
      - Ngược lại, chọn target mặc định theo thứ tự: hàng đầu -> hàng giữa -> hàng sau.
    Sau đó, thực hiện tấn công bằng cách tính sát thương:
         damage = max((attacker.base_damage * multiplier) - target.armor, 0)
    Trong đó, multiplier = 2 nếu ra chí mạng (dựa trên random < attacker.crit_rate), ngược lại multiplier = 1.
    Trước đó, kiểm tra dodge của target dựa trên "dodge rate" được tính từ thuộc tính speed:
         dodge_rate = target.speed nếu target.speed < 1, ngược lại dodge_rate = target.speed / 100.
    Nếu dodge thành công, target sẽ né và không nhận sát thương.
    """
    for attacker in attacker_team:
        if not attacker.is_alive():
            continue  # Bỏ qua thẻ đã chết

        # Xác định target theo target đặc biệt nếu có, ngược lại chọn target mặc định
        if attacker.target and attacker.target.is_alive():
            target = attacker.target
        else:
            target = get_default_target(enemy_team)
        if target:
            print(f"{attacker.name} tấn công {target.name}!")
            
            # Trước khi tính chí mạng và sát thương, kiểm tra dodge cho target.
            # Nếu target.speed < 1 thì coi đó là tỷ lệ dodge trực tiếp, còn nếu >=1 thì đổi thành phần trăm (chia cho 100)
            dodge_rate = target.speed if target.speed < 1 else target.speed / 100.0
            if random.random() < dodge_rate:
                print(f"  => {target.name} đã né tránh cuộc tấn công! (Dodge chance: {dodge_rate:.2f})")
                continue  # Bỏ qua sát thương nếu dodge thành công

            # Xác định chí mạng dựa trên tỉ lệ của attacker
            is_crit = random.random() < attacker.crit_rate
            multiplier = 2 if is_crit else 1
            damage = max(attacker.base_damage * multiplier - target.armor, 0)
            target.health -= damage
            if target.health < 0:
                target.health = 0  # Đảm bảo máu không bị âm
                
            if is_crit:
                print(f"  => Chí mạng! Sát thương: {damage}; {target.name} còn {target.health} máu.")
            else:
                print(f"  => Sát thương: {damage}; {target.name} còn {target.health} máu.")
        else:
            print(f"Không có target hợp lệ cho {attacker.name}.")


def is_team_alive(team):
    """Kiểm tra liệu team có ít nhất 1 thẻ còn sống hay không."""
    return any(card.is_alive() for card in team)


def get_team_total_speed(team):
    """
    Tính tổng tốc độ của các thẻ trong team (chỉ tính các thẻ còn sống).
    Dành cho trạng thái ban đầu khi tất cả đều còn sống.
    """
    return sum(card.speed for card in team if card.is_alive())


def print_team_health(team, team_name):
    """In thông tin thanh máu của tất cả các thẻ trong một team."""
    print(f"\nTeam {team_name} Health Status:")
    for card in team:
        print(f"{card.name}: {card.health_bar()}")


def simulate_battle(team1, team2):
    """
    Mô phỏng battle giữa 2 team:
      - Tính tổng tốc độ ban đầu (khi tất cả đều còn sống) để quyết định team nào tấn công trước (theo logic ban đầu).
      - Thứ tự tấn công được xác định chỉ ở lần đầu và giữ nguyên cho toàn bộ trận battle.
      - Sau mỗi turn, in cập nhật thanh máu của cả 6 nhân vật.
      - Mỗi turn có delay 2 giây.
    """
    # Tính tổng tốc độ ban đầu
    initial_speed_team1 = get_team_total_speed(team1)
    initial_speed_team2 = get_team_total_speed(team2)

    if initial_speed_team1 >= initial_speed_team2:
        first_team = team1
        second_team = team2
        print("Team 1 sẽ tấn công trước trong toàn bộ trận battle.")
    else:
        first_team = team2
        second_team = team1
        print("Team 2 sẽ tấn công trước trong toàn bộ trận battle.")

    turn = 1
    while is_team_alive(team1) and is_team_alive(team2):
        print(f"\n--- Turn {turn} ---")
        
        # Đội tấn công thứ nhất tấn công đội thứ hai
        battle_turn(first_team, second_team)
        if not is_team_alive(second_team):
            print("Team bị tấn công đã bị tiêu diệt!")
            break
        
        print("\n")
        # Đội tấn công thứ hai tấn công đội thứ nhất
        battle_turn(second_team, first_team)
        if not is_team_alive(first_team):
            print("Team bị tấn công đã bị tiêu diệt!")
            break

        # In cập nhật thanh máu của cả 6 nhân vật sau mỗi turn
        print_team_health(team1, "1")
        print_team_health(team2, "2")

        turn += 1
        time.sleep(2)  # Delay 2 giây mỗi turn


# Khởi tạo các đối tượng Card cho 2 team theo thứ tự vị trí:
# Team 1: index 0 -> hàng đầu; index 1 -> hàng giữa; index 2 -> hàng sau
card1 = Card("Warrior", 100, 5, 20, 0.2, 5, 20, "đầu", "hỏa")
card2 = Card("Mage", 80, 3, 25, 0.3, 10, 40, "giữa", "thủy")
card3 = Card("Archer", 90, 4, 18, 0.25, 15, 50, "sau", "phong")

# Team 2: tương tự
card4 = Card("Knight", 120, 8, 15, 0.1, 8, 60, "đầu", "thổ")
card5 = Card("Assassin", 70, 2, 30, 0.4, 5, 40, "sau", "lôi")
card6 = Card("Cleric", 110, 6, 12, 0.15, 4, 30, "giữa", "thủy")

# Tạo 2 team dưới dạng danh sách
team1 = [card1, card2, card3]
team2 = [card4, card5, card6]


# Ví dụ: Nếu cần, có thể thiết lập target đặc biệt cho 1 số thẻ (ví dụ: card2 muốn tấn công card5)
# card2.target = card5

# Bắt đầu mô phỏng battle
simulate_battle(team1, team2)
