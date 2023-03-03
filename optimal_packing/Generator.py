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

MAX_CIRCLES = 11444
CIRCLE_TYPES = 100

i = 0
row = 0
c_type = 0
c_counter = 0
color_counter = 0

##
##  43x 115 Kreise
##  57x 114 Kreise
##
circle_types = []
for c in range(8):
    for i in range(CIRCLE_TYPES):
        if i % 8 == c:
            circle_types.append(i)

# easy way: i % 100
# clustering way:
def circle_type(i: int) -> int:
    global c_counter
    global c_type
    c_max = 115 if c_type < 44 else 114
    if c_counter == c_max:
        c_counter = 0
        c_type += 1

    c_counter += 1
    return circle_types[c_type]

double_line = 57

y = c_radius
while y < 4000:
    delta = 0 if row % 2 == 0 or row == double_line else c_radius
    if row == double_line:
        c_in_line = int(c_full_line)
    else:
        c_in_line = int(c_full_line - (row % 2))
    for c in range(1, c_in_line, 2):
        print(f'{delta + c*c_radius} {y} 20 {circle_type(i)}')
        i += 1
    row += 1
    if row == double_line or row == (double_line + 1):
        y += (c_radius * 2)
    else:
        y += DELTA

row -= 1
y -= (DELTA)

show_stats = False
if show_stats:
    print(f'c_full_col: {c_full_col}')
    print(f'h_space: {h_space}')
    print(f'h_spacing: {h_spacing}')

    print(f'Toal number of rows: {row}')
    print(f'Map extending to y = {y+c_radius}')
    print(f'Available total space: {(4000-y-c_radius)}')
    print(f'Available space per row: {(4000-y-c_radius)/(row)}')


