from typing import List, Tuple
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position, Properties
from ..util import clamp

# Fungsi hitung jarak Manhattan antar dua posisi
def count_steps(a: Position, b: Position) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)

# Fungsi cek apakah dua koordinat sama persis
def coordinate_equals(x1, y1, x2, y2) -> bool:
    return x1 == x2 and y1 == y2

# Fungsi cek apakah dua posisi berada di kuadran yang sama relatif pivot
def same_direction(pivot: Position, a: Position, b: Position) -> bool:
    if a.x >= pivot.x and a.y >= pivot.y:
        return b.x >= pivot.x and b.y >= pivot.y
    if a.x >= pivot.x and a.y <= pivot.y:
        return b.x >= pivot.x and b.y <= pivot.y
    if a.x <= pivot.x and a.y >= pivot.y:
        return b.x <= pivot.x and b.y >= pivot.y
    if a.x <= pivot.x and a.y <= pivot.y:
        return b.x <= pivot.x and b.y <= pivot.y
    return False

# Fungsi alternatif arah langkah ke target (prioritaskan vertikal lalu horizontal)
def get_direction_alt(cx, cy, dx, dy) -> Tuple[int,int]:
    dx_ = clamp(dx - cx, -1, 1)
    dy_ = clamp(dy - cy, -1, 1)
    # Jika gerak vertikal ada, pilih itu, jika tidak pilih horizontal
    return (0, dy_) if dy_ != 0 else (dx_, 0)

# Kelas pengelola dua portal dan perhitungan jarak terkait portal
class Portals:
    def __init__(self, portals: List[GameObject], pos: Position):
        p0, p1 = portals
        # Tentukan portal terdekat dan terjauh dari posisi pemain saat ini
        if count_steps(pos, p0.position) < count_steps(pos, p1.position):
            self.closest_portal, self.farthest_portal = p0, p1
        else:
            self.closest_portal, self.farthest_portal = p1, p0

    # Hitung jarak jalur melalui portal: posisi sekarang ke portal terdekat + portal terjauh ke target
    def count_steps_by_portal(self, curr: Position, target: Position) -> int:
        return count_steps(curr, self.closest_portal.position) + count_steps(self.farthest_portal.position, target)

    # Cek apakah jalur lewat portal lebih dekat dari jalur langsung
    def is_closer_by_portal(self, curr: Position, target: Position) -> bool:
        return self.count_steps_by_portal(curr, target) < count_steps(curr, target)

# Kelas mewakili pemain dengan status dan gerakan
class Player:
    def __init__(self, pos: Position, props: Properties):
        self.current_position = pos
        self.base_position = props.base
        self.inventory_size = props.inventory_size
        self.diamonds_held = props.diamonds
        self.milliseconds_left = props.milliseconds_left
        self.is_inside_portal = False  # Status apakah pemain sedang di portal
        self.is_avoiding_portal = False # Status menghindari portal
        self.current_target = None      # Target objek saat ini
        self.target_position = None     # Posisi target
        self.next_move = None           # Gerakan berikutnya (dx, dy)

    # Cek apakah inventory penuh
    def is_inventory_full(self) -> bool:
        return self.diamonds_held == self.inventory_size

    # Set target objek
    def set_target(self, obj: GameObject):
        self.current_target = obj
        self.target_position = obj.position

    # Set posisi target secara langsung
    def set_target_position(self, pos: Position):
        self.target_position = pos

    # Cek apakah gerakan keluar dari board
    def is_invalid_move(self, dx: int, dy: int, board: Board) -> bool:
        nx, ny = self.current_position.x + dx, self.current_position.y + dy
        return not (0 <= nx < board.width and 0 <= ny < board.height)

    # Logika menghindari portal saat bergerak ke target
    def avoid_obstacles(self, portals: Portals, is_avoiding: bool, board: Board):
        dx, dy = get_direction_alt(self.current_position.x, self.current_position.y,
                               self.target_position.x, self.target_position.y)
        nx, ny = self.current_position.x + dx, self.current_position.y + dy

        # Jika sedang menghindar atau target bukan portal tapi langkah berikutnya portal
        if (is_avoiding or (not self.current_target or self.current_target.type != "TeleportGameObject") and
            (coordinate_equals(nx, ny, portals.closest_portal.position.x, portals.closest_portal.position.y) or
             coordinate_equals(nx, ny, portals.farthest_portal.position.x, portals.farthest_portal.position.y))):

            dx_alt, dy_alt = get_direction_alt(self.current_position.x, self.current_position.y,
                                               self.target_position.x, self.target_position.y)

            if (dx, dy) == (dx_alt, dy_alt):
                dx, dy = dy, dx
                if self.is_invalid_move(dx, dy, board):
                    dx, dy = -dx, -dy
                if dy == 0:
                    self.is_avoiding_portal = True
            else:
                dx, dy = dx_alt, dy_alt

        self.next_move = dx, dy

# Kelas pengelola berlian dan pemilihan target berlian
class Diamonds:
    def __init__(self, diamonds_list: List[GameObject], red_button: GameObject, diamonds_held: int):
        # Simpan berlian bernilai 1 poin atau saat inventory belum penuh
        self.diamonds_list = [d for d in diamonds_list if d.properties.points == 1 or diamonds_held < 4]
        self.chosen_diamond = diamonds_list[0] if diamonds_list else None
        self.chosen_distance = float('inf')
        self.red_button = red_button
        self.chosen_target = None

    # Filter berlian agar tidak berada searah dengan musuh
    def filter_diamond(self, curr: Position, enemy: Position):
        if curr.x != enemy.x and curr.y != enemy.y:
            self.diamonds_list = [d for d in self.diamonds_list if not same_direction(curr, enemy, d.position)]

    # Pilih berlian terbaik berdasarkan jarak dan poin dengan pertimbangan portal dan inventory penuh
    def choose_diamond(self, player: Player, portals: Portals):
        max_diff = 2
        for d in self.diamonds_list:
            dist = count_steps(player.current_position, d.position)
            if player.diamonds_held == 4:
                dist += min(
                    count_steps(d.position, player.base_position),
                    count_steps(d.position, portals.closest_portal.position) + count_steps(portals.farthest_portal.position, player.base_position),
                    count_steps(d.position, portals.farthest_portal.position) + count_steps(portals.closest_portal.position, player.base_position),
                )
            diff_points = d.properties.points - (self.chosen_diamond.properties.points if self.chosen_diamond else 0)
            if dist - (diff_points * max_diff) < self.chosen_distance:
                self.chosen_diamond, self.chosen_distance, self.chosen_target = d, dist, d

        # Cek opsi lewat portal jika lebih cepat
        if not player.is_inside_portal and count_steps(player.current_position, portals.closest_portal.position) < self.chosen_distance:
            for d in self.diamonds_list:
                dist = portals.count_steps_by_portal(player.current_position, d.position)
                if player.diamonds_held == 4:
                    dist += min(
                        count_steps(d.position, player.base_position),
                        count_steps(d.position, portals.closest_portal.position) + count_steps(portals.farthest_portal.position, player.base_position),
                        count_steps(d.position, portals.farthest_portal.position) + count_steps(portals.closest_portal.position, player.base_position),
                    )
                diff_points = d.properties.points - (self.chosen_diamond.properties.points if self.chosen_diamond else 0)
                if dist - (diff_points * max_diff) < self.chosen_distance:
                    self.chosen_diamond, self.chosen_distance, self.chosen_target = d, dist, portals.closest_portal

    # Cek apakah tombol merah lebih menguntungkan untuk dijadikan target
    def check_red_button(self, player: Player, portals: Portals):
        dist = (min(count_steps(player.current_position, self.red_button.position),
                    portals.count_steps_by_portal(player.current_position, self.red_button.position))
                if not player.is_inside_portal else count_steps(player.current_position, self.red_button.position))
        if player.diamonds_held == 4:
            dist += min(
                count_steps(self.red_button.position, player.base_position),
                count_steps(self.red_button.position, portals.closest_portal.position) + count_steps(portals.farthest_portal.position, player.base_position),
                count_steps(self.red_button.position, portals.farthest_portal.position) + count_steps(portals.closest_portal.position, player.base_position),
            )
        if dist + 4 <= self.chosen_distance:
            self.chosen_target = portals.closest_portal if portals.is_closer_by_portal(player.current_position, self.red_button.position) else self.red_button

# Kelas pengelola musuh dan strategi tackle atau avoidance
class Enemies:
    def __init__(self, bots_list: List[GameObject], player_bot: GameObject):
        self.enemies_list = [b for b in bots_list if b.id != player_bot.id]
        self.target_enemy = None
        self.target_enemy_distance = float('inf')
        self.try_tackle = False

    # Cek musuh terdekat dan tentukan aksi tackle atau hindari
    def check_nearby_enemy(self, diamonds: Diamonds, player: Player, portals: Portals, has_tackled: bool):
        for e in self.enemies_list:
            dist = count_steps(player.current_position, e.position)
            if dist < self.target_enemy_distance:
                self.target_enemy, self.target_enemy_distance = e, dist

        if self.target_enemy_distance == 2 and not has_tackled and player.current_position.x != self.target_enemy.position.x and player.current_position.y != self.target_enemy.position.y:
            player.next_move = get_direction_alt(player.current_position.x, player.current_position.y, self.target_enemy.position.x, self.target_enemy.position.y)
            self.try_tackle = True
        elif self.target_enemy_distance == 3:
            self.avoid_enemy(player, diamonds, portals)

    # Strategi menghindari musuh dengan update target berlian
    def avoid_enemy(self, player: Player, diamonds: Diamonds, portals: Portals):
        diamonds.filter_diamond(player.current_position, self.target_enemy.position)
        diamonds.choose_diamond(player, portals)
        if not same_direction(player.current_position, self.target_enemy.position, diamonds.red_button.position):
            diamonds.check_red_button(player, portals)

# Kelas penyimpan state board dan player untuk proses perhitungan
class GameState:
    def __init__(self, board_bot: GameObject, board: Board):
        self.board = board
        self.player_bot = board_bot

    # Inisialisasi list objek penting di board
    def initialize(self) -> Tuple[Player, Diamonds, Portals, Enemies]:
        diamonds = []
        portals = []
        bots = []
        red_button = None

        for obj in self.board.game_objects:
            if obj.type == "DiamondGameObject":
                diamonds.append(obj)
            elif obj.type == "DiamondButtonGameObject":
                red_button = obj
            elif obj.type == "TeleportGameObject":
                portals.append(obj)
            elif obj.type == "BotGameObject":
                bots.append(obj)

        return (
            Player(self.player_bot.position, self.player_bot.properties),
            Diamonds(diamonds, red_button, self.player_bot.properties.diamonds),
            Portals(portals, self.player_bot.position),
            Enemies(bots, self.player_bot)
        )

    # Cek apakah waktu tersisa cukup untuk balik ke base
    def no_time_left(self, current_position: Position, base_position: Position) -> bool:
        dist = count_steps(current_position, base_position)
        if dist == 0:
            return False
        return self.player_bot.properties.milliseconds_left / dist <= 1300

# Kelas utama bot yang mengontrol logika gerak dan strategi
class NotUnderstand(BaseLogic):
    def __init__(self):
        self.back_to_base = False
        self.is_avoiding_portal = False
        self.tackle = False

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int,int]:
        # Inisialisasi state permainan
        gs = GameState(board_bot, board)
        player, diamonds, portals, enemies = gs.initialize()

        # Update status posisi base dan portal
        if coordinate_equals(player.current_position.x, player.current_position.y,
                             player.base_position.x, player.base_position.y):
            self.back_to_base = False
        elif coordinate_equals(player.current_position.x, player.current_position.y,
                               portals.closest_portal.position.x, portals.closest_portal.position.y):
            player.is_inside_portal = True

        # Prioritas balik ke base jika inventory penuh atau waktu mepet
        if (self.back_to_base or player.is_inventory_full() or
            gs.no_time_left(player.current_position, player.base_position)):
            player.set_target_position(player.base_position)
            self.back_to_base = True

            # Gunakan portal kalau lebih cepat ke base
            if (not player.is_inside_portal and
                (not gs.no_time_left(player.current_position, player.base_position) or
                 count_steps(player.current_position, portals.closest_portal.position) == 1) and
                portals.is_closer_by_portal(player.current_position, player.base_position)):
                player.set_target(portals.closest_portal)
        else:
            # Pilih berlian terbaik sebagai target
            diamonds.choose_diamond(player, portals)
            if diamonds.chosen_target:
                diamonds.check_red_button(player, portals)
                player.set_target(diamonds.chosen_target)
            else:
                # Jika tidak ada berlian, balik ke base
                player.set_target_position(player.base_position)
                self.back_to_base = True

        # Jika masih ada waktu, cek musuh terdekat dan lakukan tackle atau hindari
        if not gs.no_time_left(player.current_position, player.base_position):
            enemies.check_nearby_enemy(diamonds, player, portals, self.tackle)
            self.tackle = enemies.try_tackle

        # Jika tidak sedang tackle, jalankan logika menghindari portal
        if not enemies.try_tackle:
            player.avoid_obstacles(portals, self.is_avoiding_portal, board)
            self.is_avoiding_portal = player.is_avoiding_portal

        # Kembalikan langkah berikutnya (dx, dy)
        return player.next_move
