import random
import time

# 初期キャッスル設定
initial_castles = [
{'name': '姫路城', 'point': 8, 'defense': 7, 'owner': None, 'stability': 4, 'cycle': 0},
{'name': '小田原城', 'point': 5, 'defense': 5, 'owner': None, 'stability': 5, 'cycle': 0},
{'name': 'バッキンガム', 'point': 4, 'defense': 2, 'owner': None, 'stability': 2, 'cycle': 0},
{'name': '甲子園', 'point': 5, 'defense': 3, 'owner': None, 'stability': 7, 'cycle': 0},
]

castles = []
cpu_points = 0
cpu2_points = 0
player_points = 0
username = ""

# ゲームを初期化する関数
def reset_game():
    global castles, cpu_points, cpu2_points, player_points, username
    castles = [castle.copy() for castle in initial_castles]
    for castle in castles:
        castle['cycle'] = 0
    cpu_points = 0
    cpu2_points = 0
    player_points = 0
    username = ""
    start_game()

# キャッスルの所有状況を表示
def print_castle_status():
    print("\nキャッスルの現在の所有状況:")
    for castle in castles:
        owner = castle['owner'] if castle['owner'] else "フリー"
        cycle_info = f"開発済{castle['cycle']}" if castle['cycle'] > 0 else ""
        print(f"- {castle['name']}: ポイント {castle['point']}, 防御力 {castle['defense']}, 開発成功率 {castle['stability']},({owner} {cycle_info})")

# ゲーム開始前の準備
def start_game():
    while True:
        ready = input("準備はいいですか？ (入力: 'start') ").strip().lower()
        if ready == 'start':
            break

    global username
    username = input("あなたの名前は？ ").strip()

    main_game_loop()

# 勝者が敗者のキャッスルを総取りする関数
def handle_victory(winner):
    print(f"\n{winner}は、他の全てのキャッスルを開発しようとしている")
    time.sleep(1)
    for castle in castles:
        previous_owner = castle['owner'] if castle['owner'] else "フリー"
        if previous_owner != winner:
            print(f"'{castle['name']}'を{previous_owner}から奪取した！")
            time.sleep(1)
        castle['owner'] = winner
    
    # 各キャッスルを開発させる
    for castle in castles:
        if castle['cycle'] == 0:  # まだ開発されていないキャッスルを開発させる
            print(f"{winner}は'{castle['name']}'の開発に成功した！")
            castle['cycle'] = 2  # 開発済状態にする
            time.sleep(1)
    
    print_castle_status()


# 勝利判定をする関数
def check_for_victory():
    global cpu_points, cpu2_points, player_points

    if player_points >= 15:
        print(f"\n{username}は勝利した！")
        handle_victory(username)
        return True
    elif cpu_points >= 15:
        print("\nCPUは勝利した！")
        handle_victory('CPU')
        return True
    elif cpu2_points >= 15:
        print("\nCPU2は勝利した！")
        handle_victory('CPU2')
        return True

    return False
# キャッスルの開発段階管理とポイント付与
def process_player_cycles():
    global player_points

    for castle in castles:
        if castle['cycle'] > 0 and castle['owner'] == username:
            castle['cycle'] -= 1
            print(f"{username}の'{castle['name']}'の開発段階が1進んだ！")
            time.sleep(1)
            if castle['cycle'] == 0:
                print(f"'{castle['name']}'は{username}の開発を完了した！")
                player_points += castle['point']
                time.sleep(1)
                print(f"{username}は現在{player_points}ポイント獲得！")
                time.sleep(1)

def process_cpu_cycles():
    global cpu_points

    for castle in castles:
        if castle['cycle'] > 0 and castle['owner'] == 'CPU':
            castle['cycle'] -= 1
            print(f"CPUの'{castle['name']}'の開発段階が1進んだ！")
            time.sleep(1)
            if castle['cycle'] == 0:
                print(f"'{castle['name']}'はCPUの開発を完了した！")
                cpu_points += castle['point']
                time.sleep(1)
                print(f"CPUは現在{cpu_points}ポイント獲得！")
                time.sleep(1)

def process_cpu2_cycles():
    global cpu2_points

    for castle in castles:
        if castle['cycle'] > 0 and castle['owner'] == 'CPU2':
            castle['cycle'] -= 1
            print(f"CPU2の'{castle['name']}'の開発段階が1進んだ！")
            time.sleep(1)
            if castle['cycle'] == 0:
                print(f"'{castle['name']}'はCPU2の開発を完了した！")
                cpu2_points += castle['point']
                time.sleep(1)
                print(f"CPU2は現在{cpu2_points}ポイント獲得！")
                time.sleep(1)

# プレイヤーのターン
def player_turn():
    time.sleep(1)
    print(f"\n{username}は誰を攻撃/開発する？")
    print(f"CPUのポイント: {cpu_points}")
    print(f"CPU2のポイント: {cpu2_points}")
    print(f"{username}のポイント: {player_points}")
    print_castle_status()

    while True:
        player_input = input("どのキャッスルを選びますか？ (ゲームをリセットしたい場合は 'reset'  パスしたい場合は 'skip')と入力) ").strip()

        if player_input == 'reset':
            print("\nゲームをリセットします...")
            time.sleep(1)
            reset_game()
            return
        
        elif player_input == 'skip':
            print(f"\n{username}はパスし、次のターンへ移動します。")
            time.sleep(1)
            return

        player_target = next((castle for castle in castles if castle['name'] == player_input), None)

        if player_target and player_target['owner'] == username:
            if player_target['cycle'] == 0:
                print(f"\n{username}は'{player_target['name']}'を開発している...")
                time.sleep(1)

                success_chance = player_target['stability'] / 10
                if random.random() < success_chance:
                    print(f"{username}は'{player_target['name']}'の開発に成功した！")
                    player_target['cycle'] = 2
                else:
                    print(f"{username}は'{player_target['name']}'の開発に失敗した！")
                time.sleep(1)
                break
            else:
                print(f"'{player_target['name']}'はすでに開発済です。")
        elif player_target and player_target['owner'] is None:
            print(f"{username}は'{player_target['name']}'を攻撃した！")
            time.sleep(1)

            success_chance = (10 - (player_target['defense'] / 2)) / 10
            if random.random() < success_chance:
                print(f"{username}は'{player_target['name']}'を手に入れた！")
                player_target['owner'] = username
            else:
                print(f"{username}は'{player_target['name']}'の攻撃に失敗した！")
            time.sleep(1)
            break
        elif player_target and player_target['owner'] != username and player_target['cycle'] == 0:
            print(f"{username}は'{player_target['name']}'を攻撃しようとしている...")
            time.sleep(1)

            success_chance = (10 + player_target['stability'] - player_target['defense']) / 20
            if random.random() < success_chance:
                print(f"{username}は'{player_target['owner']}'の'{player_target['name']}'を奪取した！")
                player_target['owner'] = username
            else:
                print(f"{username}は'{player_target['name']}'の攻撃に失敗した！")
            time.sleep(1)
            break
        else:
            print(f"{player_input}は攻撃/開発できません。再度選択してください。")
    time.sleep(1)

# CPUのターン
def cpu_turn():
    available_castles = [castle for castle in castles if castle['owner'] is None]
    developed_castles = [castle for castle in castles if castle['owner'] == 'CPU' and castle['cycle'] == 0]
    owned_by_player = [castle for castle in castles if castle['owner'] == username and castle['cycle'] == 0]

    if developed_castles:
        target = random.choice(developed_castles)
        success_chance = target['stability'] / 10
        print(f"\nCPUは'{target['name']}'を開発している...")
        time.sleep(1)

        if random.random() < success_chance:
            print(f"CPUは'{target['name']}'の開発に成功した！")
            target['cycle'] = 2
        else:
            print(f"CPUは'{target['name']}'の開発に失敗した！")
    elif available_castles:
        target = random.choice(available_castles)
        print(f"\nCPUは'{target['name']}'を攻撃した！")
        time.sleep(1)

        success_chance = (10 - (target['defense'] / 2)) / 10
        if random.random() < success_chance:
            print(f"CPUは'{target['name']}'を手に入れた！")
            target['owner'] = 'CPU'
        else:
            print(f"CPUは'{target['name']}'の攻撃に失敗した！")
    elif owned_by_player:
        target = random.choice(owned_by_player)
        success_chance = (10 + target['stability'] - target['defense']) / 20
        print(f"\nCPUは'{target['name']}'を攻撃しようとしている...")
        time.sleep(1)

        if random.random() < success_chance:
            print(f"CPUは'{username}'の'{target['name']}'を奪取した！")
            target['owner'] = 'CPU'
        else:
            print(f"CPUは'{target['name']}'の攻撃に失敗した！")
    time.sleep(1)

# CPU2のターン
def cpu2_turn():
    available_castles = [castle for castle in castles if castle['owner'] is None]
    developed_castles = [castle for castle in castles if castle['owner'] == 'CPU2' and castle['cycle'] == 0]
    owned_by_player = [castle for castle in castles if castle['owner'] == username and castle['cycle'] == 0]
    owned_by_cpu = [castle for castle in castles if castle['owner'] == 'CPU' and castle['cycle'] == 0]

    if developed_castles:
        target = random.choice(developed_castles)
        success_chance = target['stability'] / 10
        print(f"\nCPU2は'{target['name']}'を開発している...")
        time.sleep(1)

        if random.random() < success_chance:
            print(f"CPU2は'{target['name']}'の開発に成功した！")
            target['cycle'] = 2
        else:
            print(f"CPU2は'{target['name']}'の開発に失敗した！")
    elif available_castles:
        target = random.choice(available_castles)
        print(f"\nCPU2は'{target['name']}'を攻撃した！")
        time.sleep(1)

        success_chance = (10 - (target['defense'] / 2)) / 10
        if random.random() < success_chance:
            print(f"CPU2は'{target['name']}'を手に入れた！")
            target['owner'] = 'CPU2'
        else:
            print(f"CPU2は'{target['name']}'の攻撃に失敗した！")
    elif owned_by_player:
        target = random.choice(owned_by_player)
        success_chance = (10 + target['stability'] - target['defense']) / 20
        print(f"\nCPU2は'{target['name']}'を攻撃しようとしている...")
        time.sleep(1)

        if random.random() < success_chance:
            print(f"CPU2は'{username}'の'{target['name']}'を奪取した！")
            target['owner'] = 'CPU2'
        else:
            print(f"CPU2は'{target['name']}'の攻撃に失敗した！")
    elif owned_by_cpu:
        target = random.choice(owned_by_cpu)
        success_chance = (10 + target['stability'] - target['defense']) / 20
        print(f"\nCPU2は'CPU'の'{target['name']}'を攻撃しようとしている...")
        time.sleep(1)

        if random.random() < success_chance:
            print(f"CPU2は'CPU'の'{target['name']}'を奪取した！")
            target['owner'] = 'CPU2'
        else:
            print(f"CPU2は'{target['name']}'の攻撃に失敗した！")
    time.sleep(1)

# メインのゲームループ
def main_game_loop():
    while not check_for_victory():
        player_turn()
        process_player_cycles()
        if check_for_victory():
            break

        cpu_turn()
        process_cpu_cycles()
        if check_for_victory():
            break

        cpu2_turn()
        process_cpu2_cycles()
        if check_for_victory():
            break

# ゲームを開始する
reset_game()

