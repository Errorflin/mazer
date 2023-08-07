import pygame

pygame.init()

# ------------------------------ FONTS ------------------------------
# Load the font files once
SegoeUIFile = "fonts/Segoe/Segoe UI.ttf"
SegoeUI = {}
SegoeUIBoldFile = "fonts/Segoe/Segoe UI Bold.ttf"
SegoeUIBold = {}

# Define the font sizes
font_sizes = [10, 20, 30, 40, 50, 60, 80, 120]

# Load the fonts and store them in the dictionary
for size in font_sizes:
    SegoeUI[size] = pygame.font.Font(SegoeUIFile, size)
    SegoeUIBold[size] = pygame.font.Font(SegoeUIBoldFile, size)

# Access fonts in different sizes:
SegoeUI10 = SegoeUI[10]; SegoeUIBold10 = SegoeUIBold[10]
SegoeUI20 = SegoeUI[20]; SegoeUIBold20 = SegoeUIBold[20]
SegoeUI30 = SegoeUI[30]; SegoeUIBold30 = SegoeUIBold[30]
SegoeUI40 = SegoeUI[40]; SegoeUIBold40 = SegoeUIBold[40]
SegoeUI60 = SegoeUI[60]; SegoeUIBold60 = SegoeUIBold[60]
SegoeUI80 = SegoeUI[80]; SegoeUIBold80 = SegoeUIBold[80]
SegoeUI120 = SegoeUI[120]; SegoeUIBold120 = SegoeUIBold[120]; 