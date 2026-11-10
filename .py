w = int(800/int(input()))
h = int(600/int(input()))

rectangles = [
    
]
for j in range(-h, 601, h):
    for i in range(-w, 751, w):
        rectangles.append([i+w, j, w, w])
print(rectangles)