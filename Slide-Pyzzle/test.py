import pygame
import random
import os

# Kích thước của cửa sổ
WINDOW_SIZE = 600
TILE_SIZE = WINDOW_SIZE // 3

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Khởi tạo pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Slide Puzzle")

# Tải hình ảnh
def load_images():
    images = []
    for i in range(9):
        img = pygame.image.load(os.path.join("puzz-pieces", f"{i}.jpg"))
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        images.append(img)
    return images

# Hiển thị hình ảnh
def draw_grid(state, images):
    window.fill(WHITE)
    for i in range(3):
        for j in range(3):
            index = state[i * 3 + j]
            if index != 8:  # Ô trống không hiển thị hình ảnh
                window.blit(images[index], (j * TILE_SIZE, i * TILE_SIZE))
    pygame.display.update()

# Kiểm tra xem trò chơi đã được giải quyết chưa
def is_solved(state):
    return state == list(range(9))

# Hoán đổi vị trí của các ô
def swap(state, pos1, pos2):
    state[pos1], state[pos2] = state[pos2], state[pos1]

# Lấy vị trí của ô trống
def find_blank(state):
    return state.index(8)

# Di chuyển ô
def move(state, direction):
    blank_pos = find_blank(state)
    if direction == "UP" and blank_pos > 2:
        swap(state, blank_pos, blank_pos - 3)
    elif direction == "DOWN" and blank_pos < 6:
        swap(state, blank_pos, blank_pos + 3)
    elif direction == "LEFT" and blank_pos % 3 > 0:
        swap(state, blank_pos, blank_pos - 1)
    elif direction == "RIGHT" and blank_pos % 3 < 2:
        swap(state, blank_pos, blank_pos + 1)

# Hiển thị thông điệp chúc mừng
def show_congratulations():
    font = pygame.font.Font(None, 74)
    text = font.render("Congratulation!!!", True, (253,204,13))
    window.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, WINDOW_SIZE // 2 - text.get_height() // 2))
    pygame.display.update()

def shuffle_tiles():
    while True:
        tiles = list(range(9))
        random.shuffle(tiles)
        inversions = count_inversions(tiles)
        blank_row = tiles.index(8) // 3  # Dòng của ô trống (0-based)
        
        # Điều kiện giải được: số inversions chẵn nếu ô trống nằm ở hàng chẵn từ dưới lên
        if (inversions % 2 == 0) or (blank_row % 2 == 1):
            return tiles
        
# Hàm kiểm tra số lần đảo chỗ (inversions)
def count_inversions(tiles):
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] != 8 and tiles[j] != 8 and tiles[i] > tiles[j]:
                inversions += 1
    return inversions

def main():
    # Tải hình ảnh
    images = load_images()

    # Trạng thái ban đầu
    state = shuffle_tiles()

    clock = pygame.time.Clock()
    running = True
    solved = False

    while running:
        if not solved:
            draw_grid(state, images)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        move(state, "DOWN")
                    elif event.key == pygame.K_DOWN:
                        move(state, "UP")
                    elif event.key == pygame.K_LEFT:
                        move(state, "RIGHT")
                    elif event.key == pygame.K_RIGHT:
                        move(state, "LEFT")

            if is_solved(state):
                solved = True

            clock.tick(30)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        move(state, "DOWN")
                    elif event.key == pygame.K_DOWN:
                        move(state, "UP")
                    elif event.key == pygame.K_LEFT:
                        move(state, "RIGHT")
                    elif event.key == pygame.K_RIGHT:
                        move(state, "LEFT")
            show_congratulations()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Khi người chơi nhấn phím, khởi động lại trò chơi
                    state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                    random.shuffle(state)
                    solved = False

    pygame.quit()

if __name__ == "__main__":
    main()
