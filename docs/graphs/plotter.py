import matplotlib.pyplot as plt

# Data for clique size distribution
clique_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
frequencies = [1184, 8649, 13711, 27290, 48403, 68854, 83242, 76722, 54456, 35470, 21736, 11640, 5449, 2329, 740, 208, 23]

# Create the plot
plt.figure(figsize=(10, 6))
plt.bar(clique_sizes, frequencies, color='skyblue')

# Add titles and labels
plt.title('Clique Size Distribution (Wikipedia Vote Network)')
plt.xlabel('Clique Size')
plt.ylabel('Frequency')

# Save the plot as an image file
plt.savefig('wiki-graph.png')

# Show the plot
plt.show()