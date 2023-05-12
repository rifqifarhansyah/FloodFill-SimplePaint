import pygame
from pygame import Surface
import pygame.gfxdraw
import pygame.constants
import pygame.locals
import sys
import random
import os

# Inisialisasi pygame dan membuat tampilan dengan ukuran 1200 x 800 piksel
pygame.init()
size = resX, resY = 1200, 800
screen = pygame.display.set_mode(size)

# Mengatur ikon dan judul aplikasi
iconPath = os.path.join("img", "icon.png")
icon = pygame.image.load(iconPath)
pygame.display.set_icon(icon)
pygame.display.set_caption("Flood Fill Application")
clock = pygame.time.Clock()
fileName = 'changes.txt'

# Mengatur waktu frame dan font teks
FPS = 60
font = pygame.font.SysFont('verdana', 20)

# Variabel untuk algoritma (dfs atau bfs), dimensi sel dan grid
algoritma = "dfs"
cellDimension = cellWidth, cellHeight = 20, 20
gridDimension = rows, cols = resX // cellWidth, resY // cellHeight

# Membuat grid dengan warna putih (255, 255, 255) pada setiap selnya
grid = [[(255, 255, 255) for _ in range(cols)] for _ in range(rows)]

# Membuat variabel untuk posisi acak dan warna saat ini
randomPosition = None
currentColor = (210, 210, 210)

# Menggambar grid pada layar
def display_grid(screen, grid, width=2, height=2) -> None:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x, y = i * width, j * height
            cellColor = grid[i][j]
            pygame.draw.rect(
                screen,
                cellColor,
                pygame.Rect(x, y, width, height),
            )

# Fungsi untuk menyimpan perubahan warna pada grid
def recordChanges(grid, fileName):
    with open(fileName, 'w') as f:
        for row in grid:
            for cell in row:
                f.write(f"{cell[0]} {cell[1]} {cell[2]} ")


# Fungsi untuk flood fill dengan algoritma DFS atau BFS
def fillDfsBfs(grid, start, newColor=(150, 150, 0), algoritma="dfs", fileName=None):
    oldColor = grid[start[0]][start[1]]
    if oldColor == newColor:
        return grid
    stack = [start]
    removeIndex = -1 if algoritma == "dfs" else 0
    while len(stack) > 0:
        x, y = stack.pop(removeIndex)
        if grid[x][y] != oldColor:
            continue
        grid[x][y] = newColor
        if fileName:
            recordChanges(grid, fileName)
        if x > 0:
            stack.append((x - 1, y))
        if y > 0:
            stack.append((x, y - 1))
        if x < len(grid) - 1:
            stack.append((x + 1, y))
        if y < len(grid[0]) - 1:
            stack.append((x, y + 1))
        yield grid

# Fungsi untuk mengkonversi koordinat mouse ke koordinat grid
def postToGrid(pos):
    row, col = pos[0] // cellWidth, pos[1] // cellHeight
    if row >= rows or col >= cols:
        return None, None
    return row, col

# Fungsi untuk mewarnai sel berdasarkan posisi mouse
def coloring(pos, color):
    row, col = pos[0] // cellWidth, pos[1] // cellHeight
    if row >= rows or col >= cols:
        return
    grid[row][col] = color

# Inisiali gridStateIterator untuk menyimpan hasil dari pemanggilan fungsi fillDfsBfs
gridStateIterator = None

# Variabel untuk warna kiri, kanan, dan isi
currentColor = (210, 210, 210)
leftColor = (0, 0, 0)
rightColor = (255, 255, 255)
fillColor = (random.randrange(256), random.randrange(256), random.randrange(256))

# Text untuk menampilkan algoritma dan pilihan warna
text = font.render(f"Algoritma: {algoritma.upper()}     Pilih Warna:", False, (0, 0, 0))

# colorButtonAbsis dan colorButtonOrdinat digunakan untuk menentukan posisi tombol warna di layar
colorButtonAbsis, colorButtonOrdinat = text.get_width() + 10, 10

# colorButtonWidth dan colorButtonHeight digunakan untuk menentukan ukuran tombol warna di layar
colorButtonWidth, colorButtonHeight = 50, 30

while True:
    pygame.display.flip()
    clock.tick(FPS)
    screen.fill(0)
    for event in pygame.event.get():
        # Jika tombol keluar ditekan, keluar dari aplikasi
        if event.type == pygame.QUIT:
            sys.exit()
        # Jika tombol C pada keyboard ditekan, ganti algoritma
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                algoritma = "bfs" if algoritma.lower() == "dfs" else "dfs"
        # Jika tombol mouse ditekan, lakukan aksi sesuai tombol yang ditekan
        if pygame.mouse.get_pressed()[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            if abs(mouseX-colorButtonAbsis) <= colorButtonWidth and abs(mouseY-colorButtonOrdinat) <= colorButtonHeight:
                fillColor = (random.randrange(256), random.randrange(256), random.randrange(256))
            pos = pygame.mouse.get_pos()
            coloring(pos, leftColor)
        if pygame.mouse.get_pressed()[1] or pygame.key.get_pressed()[pygame.K_f]:
            pos = pygame.mouse.get_pos()
            pos = postToGrid(pos)
            gridStateIterator = fillDfsBfs(grid, pos, newColor=fillColor, algoritma=algoritma, fileName="changes.txt")
        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            coloring(pos, rightColor)
    # Jika gridStateIterator tidak kosong, ambil grid dari gridStateIterator
    if gridStateIterator:
        try:
            grid = next(gridStateIterator)
        except StopIteration:
            pass

    # Gambar grid dan tombol warna
    display_grid(screen, grid, *cellDimension)
    text = font.render(f"Algoritma: {algoritma.upper()}     Pilih Warna:", False, (0, 0, 0))
    screen.blit(text, text.get_rect(topleft=(10, 10)))
    pygame.draw.rect(screen, fillColor, pygame.Rect(colorButtonAbsis, colorButtonOrdinat, colorButtonWidth, colorButtonHeight))