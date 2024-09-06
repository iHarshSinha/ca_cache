from driver import q3, q2, q4
import matplotlib.pyplot as plt
import numpy as np
coll=[q2,q3,q4]
files=['gcc.trace','gzip.trace','mcf.trace','swim.trace','twolf.trace']

for i in range(3):
    data=coll[i]
    m = len(data)
    n = len(data[0])

    # Iterate over each row to plot the corresponding graph
    for j in range(n):
        column_data = [row[j] for row in data]  # Extract the i-th column
        # custom_text = f'{files[j]}'
        plt.plot([2**k for k in range(m)], column_data, marker='o', linestyle='-', label=f'Graph of {files[j]}')

    # Set x-axis labels to display 2^k instead of the default range(m) values
    x_values = [2**k for k in range(m)]
    plt.xticks(x_values, [2**k for k in range(m)])

    # Add labels and title
    if i==0:
        plt.xlabel('Cache Size')
        plt.ylabel('Miss Rate')
        plt.title('Miss Rate V/S Cache Size')
    if i==1:
        plt.xlabel('Block Size')
        plt.ylabel('Miss Rate')
        plt.title('Miss Rate V/S Block Size')
    if i==2:
        plt.xlabel('Associativity')
        plt.ylabel('Hit Rate')
        plt.title('Hit Rate V/s Associativity')
# Add a legend to differentiate between the graphs
    plt.legend()

    # Display the plot
    plt.grid(True)  # Adds a grid for better readability
    plt.show()