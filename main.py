import numpy as np

# Generate some random data
data = np.random.randn(1000)

# Create a histogram
plt.hist(data, bins=30, alpha=0.7)
plt.title('Normal Distribution Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True)
