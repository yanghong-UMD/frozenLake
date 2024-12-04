import matplotlib.pyplot as plt
import numpy as np

# Raw data
rawData = {
    "success": {
        "size2": [
            {"Sample": 3.98, "MoveTo": 48.23, "FSPlan": 48.50, "Qlearning": 100.00},
            {"Sample": 18.61, "MoveTo": 66.07, "FSPlan": 63.80, "Qlearning": 100.00},
            {"Sample": 22.47, "MoveTo": 96.91, "FSPlan": 96.40, "Qlearning": 100.00},
            {"Sample": 23.30, "MoveTo": 93.19, "FSPlan": 92.20, "Qlearning": 100.00},
            {"Sample": 7.52, "MoveTo": 48.53, "FSPlan": 48.00, "Qlearning": 100.00}
        ],
        "size4": [
            {"Sample": 0.77, "MoveTo": 8.22, "FSPlan": 5.60, "Qlearning": 100.00},
            {"Sample": 0.98, "MoveTo": 8.00, "FSPlan": 6.80, "Qlearning": 100.00},
            {"Sample": 2.38, "MoveTo": 13.03, "FSPlan": 22.90, "Qlearning": 100.00},
            {"Sample": 1.48, "MoveTo": 11.27, "FSPlan": 10.70, "Qlearning": 100.00},
            {"Sample": 2.25, "MoveTo": 5.27, "FSPlan": 11.20, "Qlearning": 100.00}
        ],
        "size6": [
            {"Sample": 0.27, "MoveTo": 0.75, "FSPlan": 7.80, "Qlearning": 86.39},
            {"Sample": 0.56, "MoveTo": 6.44, "FSPlan": 5.80, "Qlearning": 100.00},
            {"Sample": 1.13, "MoveTo": 11.95, "FSPlan": 17.70, "Qlearning": 100.00},
            {"Sample": 0.36, "MoveTo": 1.07, "FSPlan": 2.10, "Qlearning": 97.90},
            {"Sample": 0.30, "MoveTo": 7.04, "FSPlan": 5.50, "Qlearning": 99.57}
        ],
        "size8": [
            {"Sample": 0.19, "MoveTo": 1.23, "FSPlan": 3.20, "Qlearning": 82.28},
            {"Sample": 0.22, "MoveTo": 0.85, "FSPlan": 2.50, "Qlearning": 100.00},
            {"Sample": 0.15, "MoveTo": 1.22, "FSPlan": 1.00, "Qlearning": 56.77},
            {"Sample": 0.40, "MoveTo": 3.82, "FSPlan": 3.50, "Qlearning": 100.00},
            {"Sample": 0.27, "MoveTo": 1.85, "FSPlan": 1.70, "Qlearning": 70.14}
        ],
        "size10": [
            {"Sample": 0.10, "MoveTo": 4.37, "FSPlan": 5.40, "Qlearning": 64.18},
            {"Sample": 0.10, "MoveTo": 0.37, "FSPlan": 0.70, "Qlearning": 74.63},
            {"Sample": 0.05, "MoveTo": 0.35, "FSPlan": 0.10, "Qlearning": 0.00},
            {"Sample": 0.05, "MoveTo": 0.31, "FSPlan": 0.60, "Qlearning": 24.81},
            {"Sample": 0.02, "MoveTo": 0.22, "FSPlan": 0.50, "Qlearning": 0.00}
        ],
        "size12": [
            {"Sample": 0.02, "MoveTo": 0.54, "FSPlan": 0.60, "Qlearning": 17.37},
            {"Sample": 0.06, "MoveTo": 0.52, "FSPlan": 1.20, "Qlearning": 0.00},
            {"Sample": 0.14, "MoveTo": 1.92, "FSPlan": 3.10, "Qlearning": 0.00},
            {"Sample": 0.00, "MoveTo": 0.26, "FSPlan": 0.20, "Qlearning": 0.00},
            {"Sample": 0.00, "MoveTo": 0.05, "FSPlan": 0.00, "Qlearning": 0.00}
        ]
    },
    "steps": {
        "size2": [
            {"Sample": 78.41, "MoveTo": 48.85, "FSPlan": 47.23, "Qlearning": 52.07},
            {"Sample": 101.59, "MoveTo": 40.76, "FSPlan": 40.98, "Qlearning": 43.23},
            {"Sample": 129.15, "MoveTo": 48.14, "FSPlan": 47.87, "Qlearning": 44.31},
            {"Sample": 180.04, "MoveTo": 49.37, "FSPlan": 48.55, "Qlearning": 47.06},
            {"Sample": 148.12, "MoveTo": 47.53, "FSPlan": 47.51, "Qlearning": 64.75}
        ],
        "size4": [
            {"Sample": 60.42, "MoveTo": 41.44, "FSPlan": 44.48, "Qlearning": 71.94},
            {"Sample": 59.15, "MoveTo": 40.74, "FSPlan": 37.82, "Qlearning": 69.89},
            {"Sample": 59.50, "MoveTo": 31.76, "FSPlan": 35.78, "Qlearning": 55.99},
            {"Sample": 58.49, "MoveTo": 35.97, "FSPlan": 35.56, "Qlearning": 110.00},
            {"Sample": 64.52, "MoveTo": 27.83, "FSPlan": 33.69, "Qlearning": 81.31}
        ],
        "size6": [
            {"Sample": 65.63, "MoveTo": 26.25, "FSPlan": 47.87, "Qlearning": 86.38},
            {"Sample": 47.46, "MoveTo": 38.93, "FSPlan": 34.38, "Qlearning": 82.69},
            {"Sample": 63.88, "MoveTo": 45.61, "FSPlan": 48.02, "Qlearning": 76.09},
            {"Sample": 78.97, "MoveTo": 27.77, "FSPlan": 31.00, "Qlearning": 63.86},
            {"Sample": 54.39, "MoveTo": 45.48, "FSPlan": 44.87, "Qlearning": 73.71}
        ],
        "size8": [
            {"Sample": 43.79, "MoveTo": 24.72, "FSPlan": 31.94, "Qlearning": 65.66},
            {"Sample": 53.05, "MoveTo": 25.71, "FSPlan": 31.28, "Qlearning": 102.27},
            {"Sample": 33.60, "MoveTo": 27.38, "FSPlan": 28.50, "Qlearning": 61.52},
            {"Sample": 47.55, "MoveTo": 28.13, "FSPlan": 29.66, "Qlearning": 71.37},
            {"Sample": 50.48, "MoveTo": 27.91, "FSPlan": 27.00, "Qlearning": 105.51}
        ],
        "size10": [
            {"Sample": 43.60, "MoveTo": 35.70, "FSPlan": 35.69, "Qlearning": 77.50},
            {"Sample": 31.20, "MoveTo": 25.95, "FSPlan": 28.57, "Qlearning": 84.57},
            {"Sample": 27.80, "MoveTo": 22.77, "FSPlan": 18.00, "Qlearning": 0.00},
            {"Sample": 35.60, "MoveTo": 27.00, "FSPlan": 33.00, "Qlearning": 96.96},
            {"Sample": 31.50, "MoveTo": 27.64, "FSPlan": 29.00, "Qlearning": 0.00}
        ],
        "size12": [
            {"Sample": 47.00, "MoveTo": 24.57, "FSPlan": 32.50, "Qlearning": 62.07},
            {"Sample": 33.50, "MoveTo": 23.77, "FSPlan": 28.67, "Qlearning": 0.00},
            {"Sample": 33.36, "MoveTo": 28.73, "FSPlan": 29.90, "Qlearning": 0.00},
            {"Sample": 0.00, "MoveTo": 36.62, "FSPlan": 29.50, "Qlearning": 0.00},
            {"Sample": 0.00, "MoveTo": 21.60, "FSPlan": 0.00, "Qlearning": 0.00}
        ]
    }
}
methods = ['Sample', 'MoveTo', 'FSPlan', 'Qlearning']
sizes = [2,4,6,8,10,12]
n_methods = len(methods)
n_sizes = len(sizes)
bar_width = 0.2

data = np.zeros((n_methods, n_sizes))
for i, method in enumerate(methods):
    for j, size in enumerate(sizes):
        values = [entry[method] for entry in rawData['steps'][f'size{size}']]
        data[i, j] = np.mean(values)

fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(n_sizes)
for i in range(n_methods):
    ax.bar(x + i * bar_width, data[i], bar_width, label=methods[i])

ax.set_xlabel('Hole Size')
ax.set_ylabel('Path Length')
ax.set_xticks(x + bar_width * (n_methods-1)/2)
ax.set_xticklabels([f'{size}' for size in sizes])
ax.legend()
plt.tight_layout()
plt.show()