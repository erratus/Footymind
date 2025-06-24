import os
import xml.etree.ElementTree as ET
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Team color definitions
team_colors = {
    'Arsenal': 'red',
    'Aston Villa': 'maroon',
    'Bournemouth': 'crimson',
    'Brentford': 'red',
    'Brighton': 'blue',
    'Chelsea': 'blue',
    'Crystal Palace': 'red',
    'Everton': 'blue',
    'Fulham': 'white',
    'Liverpool': 'red',
    'Luton Town': 'blue',
    'Manchester City': 'skyblue',
    'Manchester United': 'red',
    'Newcastle United': 'black',
    'Nottingham Forest': 'red',
    'Sheffield United': 'red',
    'Tottenham Hotspur': '#0000FF',
    'West Ham United': '#7A0000',
}

# Set paths relative to project root
xml_path = os.path.join('xml_labels', 'img00.xml')
image_path = os.path.join('model', 'images', 'train', 'img00.jpg')

# Parse XML
tree = ET.parse(xml_path)
root = tree.getroot()

# Load image
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Set up plot
fig, ax = plt.subplots(figsize=(20, 10))
ax.imshow(image)

# Draw each object
for obj in root.findall('object'):
    name = obj.find('name').text
    bndbox = obj.find('bndbox')
    xmin = int(bndbox.find('xmin').text)
    ymin = int(bndbox.find('ymin').text)
    xmax = int(bndbox.find('xmax').text)
    ymax = int(bndbox.find('ymax').text)

    color = team_colors.get(name, 'yellow')

    rect = patches.Rectangle(
        (xmin, ymin),
        xmax - xmin,
        ymax - ymin,
        linewidth=2,
        edgecolor=color,
        facecolor='none',
        label=name
    )
    ax.add_patch(rect)
    ax.text(xmin, ymin - 5, name, color=color, fontsize=10, weight='bold')

# Show legend and output
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.axis('off')
plt.tight_layout()
plt.show()
