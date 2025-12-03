# card_game.py

class Card:
    """แสดงการ์ดแต่ละใบในเกม"""
    def __init__(self, name, attack, cost):
        self.name = name
        self.attack = attack  # พลังโจมตี
        self.cost = cost      # พลังงานที่ใช้ในการเล่นการ์ด

    def __str__(self):
        return f"{self.name} (โจมตี: {self.attack}, ใช้พลังงาน: {self.cost})"

class Player:
    """แสดงตัวผู้เล่นแต่ละคน"""
    def __init__(self, name, starting_hp=100, starting_energy=3):
        self.name = name
        self.hp = starting_hp
        self.max_energy = starting_energy
        self.current_energy = starting_energy
        self.hand = []
        self.is_turn = False

    def play_card(self, card_index, target):
        """ผู้เล่นเลือกเล่นการ์ด และใช้โจมตีเป้าหมาย"""
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            
            if self.current_energy >= card.cost:
                # 1. ใช้พลังงานและเอาการ์ดออกจากมือ
                self.current_energy -= card.cost
                self.hand.pop(card_index)
                
                # 2. โจมตีเป้าหมาย
                target.hp -= card.attack
                
                print(f"--- {self.name} เล่น: **{card.name}** ใช้ {card.cost} พลังงาน")
                print(f"--- โจมตี {target.name} สร้างความเสียหาย {card.attack} หน่วย")
                return True
            else:
                print(f"!!! พลังงานไม่พอ: {card.name} ต้องใช้ {card.cost} แต่มีเพียง {self.current_energy} !!!")
                return False
        else:
            print("!!! เลือกการ์ดไม่ถูกต้อง !!!")
            return False

def setup_game():
    """ตั้งค่าผู้เล่นและการ์ดเริ่มต้น"""
    # สร้างสำรับการ์ดพื้นฐาน
    all_cards = [
        Card("โจมตีเบา", 10, 1),
        Card("โจมตีหนัก", 25, 3),
        Card("ออมพลังงาน", 0, 0), # การ์ดที่ไม่โจมตี แต่อาจมีประโยชน์อื่นในอนาคต
        Card("ยิงเวทย์", 15, 2),
    ]

    # สร้างผู้เล่น
    player1 = Player("P1 (กฤษณ์)")
    player2 = Player("P2 (นภา)")

    # แจกการ์ดเริ่มต้น (สุ่มให้ง่ายขึ้น)
    import random
    random.shuffle(all_cards)
    
    player1.hand = random.sample(all_cards, 2)
    player2.hand = random.sample(all_cards, 2)

    return player1, player2

def display_status(p1, p2):
    """แสดงสถานะปัจจุบันของผู้เล่นทั้งสอง"""
    print("\n" + "="*50)
    print(f"  **สถานะปัจจุบัน**")
    print(f"  {p1.name}: HP={p1.hp}, พลังงาน={p1.current_energy}")
    print(f"  {p2.name}: HP={p2.hp}, พลังงาน={p2.current_energy}")
    print("="*50)

def take_turn(current_player, opponent):
    """จัดการขั้นตอนในแต่ละเทิร์น"""
    current_player.current_energy = current_player.max_energy # ฟื้นฟูพลังงาน
    print(f"\n<<< *** เทิร์นของ {current_player.name} *** >>> (HP: {current_player.hp})")
    
    # แสดงการ์ดในมือ
    print("การ์ดในมือ:")
    for i, card in enumerate(current_player.hand):
        print(f"  [{i+1}] {card}")

    # การดำเนินการของผู้เล่น (จำลอง Input)
    while True:
        try:
            # ใช้ -1 เพื่อจบเทิร์น, ใช้ 1, 2, 3... เพื่อเล่นการ์ด
            action = input("เลือกการ์ดที่จะเล่น (1-N) หรือพิมพ์ '0' เพื่อจบเทิร์น: ")
            
            if action == '0':
                print(f"{current_player.name} จบเทิร์น.")
                break # จบเทิร์น
            
            card_index = int(action) - 1
            if current_player.play_card(card_index, opponent):
                # ถ้าเล่นการ์ดสำเร็จ ให้ถามต่อว่าจะเล่นอีกไหม
                if opponent.hp <= 0:
                    break # จบเกม
                continue
            else:
                # ถ้าเล่นการ์ดไม่สำเร็จ (เช่น พลังงานไม่พอ) ให้วนถามใหม่
                continue
            
        except ValueError:
            print("!!! กรุณาใส่ตัวเลขที่ถูกต้อง !!!")
            continue

def main_game_loop():
    """ลูปหลักของเกม"""
    p1, p2 = setup_game()
    turn_count = 1
    current_turn_player = p1
    opponent_player = p2

    while p1.hp > 0 and p2.hp > 0:
        display_status(p1, p2)
        
        # ผู้เล่นปัจจุบันเล่น
        take_turn(current_turn_player, opponent_player)

        # ตรวจสอบผู้ชนะ
        if opponent_player.hp <= 0:
            print(f"\n🎉🎉 **{current_turn_player.name} ชนะแล้ว!** 🎉🎉")
            break
        
        # สลับเทิร์น
        current_turn_player, opponent_player = opponent_player, current_turn_player
        turn_count += 1
        
    if p1.hp <= 0 and p2.hp <= 0:
        print("\nเสมอ!")
    elif p1.hp > 0 and turn_count > 100: # เพิ่มเงื่อนไขป้องกันลูปไม่รู้จบ (ถ้ามี)
        print("จบเกม: ถึงขีดจำกัดเทิร์น")

# เริ่มเกม
if __name__ == "__main__":
    main_game_loop()from random import shuffle


class Card:
    suits = ["spades",
             "hearts",
             "diamonds",
             "clubs"]

    values = [None, None,"2", "3",
              "4", "5", "6", "7",
              "8", "9", "10",
              "Jack", "Queen",
              "King", "Ace"]

    def __init__(self, v, s):
        """suit + value are ints"""
        self.value = v
        self.suit = s

    def __lt__(self, c2):
        if self.value < c2.value:
            return True
        if self.value == c2.value:
            if self.suit < c2.suit:
                return True
            else:
                return False
        return False

    def __gt__(self, c2):
        if self.value > c2.value:
            return True
        if self.value == c2.value:
            if self.suit > c2.suit:
                return True
            else:
                return False
        return False

    def __repr__(self):
        v = self.values[self.value] +\
            " of " + \
            self.suits[self.suit]
        return v


class Deck:
    def __init__(self):
        self.cards = []
        for i in range(2, 15):
            for j in range(4):
                self.cards\
                    .append(Card(i,
                                 j))
        shuffle(self.cards)

    def rm_card(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.wins = 0
        self.card = None
        self.name = name


class Game:
    def __init__(self):
        name1 = input("p1 name ")
        name2 = input("p2 name ")
        self.deck = Deck()
        self.p1 = Player(name1)
        self.p2 = Player(name2)

    def wins(self, winner):
        w = "{} wins this round"
        w = w.format(winner)
        print(w)

    def draw(self, p1n, p1c, p2n, p2c):
        d = "{} drew {} {} drew {}"
        d = d.format(p1n,
                     p1c,
                     p2n,
                     p2c)
        print(d)

    def play_game(self):
        cards = self.deck.cards
        print("beginning War!")
        while len(cards) >= 2:
            m = "q to quit. Any " + \
                "key to play:"
            response = input(m)
            if response == 'q':
                break
            p1c = self.deck.rm_card()
            p2c = self.deck.rm_card()
            p1n = self.p1.name
            p2n = self.p2.name
            self.draw(p1n,
                      p1c,
                      p2n,
                      p2c)
            if p1c > p2c:
                self.p1.wins += 1
                self.wins(self.p1.name)
            else:
                self.p2.wins += 1
                self.wins(self.p2.name)

        win = self.winner(self.p1,
                         self.p2)
        print("War is over.{} wins"
              .format(win))

    def winner(self, p1, p2):
        if p1.wins > p2.wins:
            return p1.name
        if p1.wins < p2.wins:
            return p2.name
        return "It was a tie!"

game = Game()
game.play_game()
