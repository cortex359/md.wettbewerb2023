import math

c_radius = 20
c_full_line = 4000 // c_radius


DELTA = math.sqrt(
    (c_radius * 2) * (c_radius * 2) - (c_radius * c_radius)
)

c_full_col = (4000 // DELTA) - 1
h_space = (4000 - ((c_full_col * DELTA) + 2 * c_radius))
h_spacing = h_space / (c_full_col + 1)

#h_spacing = 0.2712645503767833

#print("Delta:")
#print(DELTA)
#DELTA_normal = 34.641016151377545870548926830117
#print(DELTA_normal)
#print(DELTA - DELTA_normal)

#last_line = 3969.0758412570467
#print(last_line/DELTA)

MAX_CIRCLES = 11443
CIRCLE_TYPES = 100

i = 0
row = 0

y = c_radius + h_spacing
while y < 4000:
    delta = 0 if row % 2 == 0 else c_radius
    for c in range(1, int(c_full_line - (row % 2)), 2):
        print(f'{delta + c*c_radius} {y} 20 {i % 100}')
        i += 1
    row += 1
    y += DELTA + h_spacing

row -= 1
y -= (DELTA + h_spacing)

show_stats = False
if show_stats:
    print(f'c_full_col: {c_full_col}')
    print(f'h_space: {h_space}')
    print(f'h_spacing: {h_spacing}')

    print(f'Toal number of rows: {row}')
    print(f'Map extending to y = {y+c_radius}')
    print(f'Available total space: {(4000-y-c_radius)}')
    print(f'Available space per row: {(4000-y-c_radius)/(row)}')


