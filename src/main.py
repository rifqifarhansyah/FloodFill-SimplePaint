import pygame
from pygame import Surface
import pygame.gfxdraw
import pygame.constants
import pygame.locals
import sys
import random

# Inisialisasi pygame dan membuat tampilan dengan ukuran 1200 x 800 piksel
pygame.init()
size = resX, resY = 1200, 800
screen = pygame.display.set_mode(size)

# Mengatur ikon dan judul aplikasi
icon = pygame.image.load("../img/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Flood Fill Application")
clock = pygame.time.Clock()

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

# Fungsi untuk flood fill dengan algoritma DFS atau BFS
def fillDfsBfs(grid, start, newColor=(150, 150, 0), algoritma="dfs"):
    oldColor = grid[start[0]][start[1]]
    if oldColor == newColor:
        return grid
    stack = [start]
    removeIndex = -1 if algoritma == "dfs" else 0
    while len(stack) > 0:
        '''
        Pada implementasi ini, jika Algoritma adalah DFS,
        maka penjelajahan akan dilakukan menggunakan stack
        dan elemen yang ditambahkan ke stack akan dihapus
        dari bagian paling belakang stack dengan perintah pop(-1).
        Sedangkan jika Algoritma adalah BFS, maka penjelajahan
        akan dilakukan menggunakan queue dan elemen yang ditambahkan
        akan dihapus dari bagian depan queue dengan perintah pop(0).

        Untuk setiap titik yang dikunjungi selama penjelajahan,
        warnanya akan diubah menjadi newColor dan tetangganya akan
        ditambahkan ke stack atau queue. Pada implementasi ini,
        setiap kali ada sel yang berhasil diisi dengan warna,
        maka fungsi yield akan dipanggil dan grid yang baru diisi
        warna akan dikembalikan sebagai generator. Proses pengisian sel
        dalam grid akan terus dilakukan hingga seluruh area yang terhubung
        dengan sel awal (start) telah diisi dengan warna.
        '''
        x, y = stack.pop(removeIndex)
        if grid[x][y] != oldColor:
            continue
        grid[x][y] = newColor
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
            gridStateIterator = fillDfsBfs(grid, pos, newColor=fillColor, algoritma=algoritma)
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