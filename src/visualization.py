import matplotlib.pyplot as plt
from collections import Counter

# Membaca file txt dan mengubahnya menjadi list of tuples
with open('changes.txt', 'r') as f:
    colors_str = f.read().split()
colors = [(int(colors_str[i]), int(colors_str[i+1]), int(colors_str[i+2])) for i in range(0, len(colors_str), 3)]

# Menghitung frekuensi kemunculan warna
color_counts = Counter(colors)

# Memvisualisasikan frekuensi kemunculan warna dalam pie chart
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(list(color_counts.values()), startangle=90)
ax.axis('equal')
ax.set_title('Color Frequency')
labels = []
for c in color_counts:
    labels.append(f'({c[0]}, {c[1]}, {c[2]}): {color_counts[c]}')
ax.legend(labels, loc='center left', bbox_to_anchor=(0.7, 0.5), fancybox=True, shadow=True)
plt.show()
