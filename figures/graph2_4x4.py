import matplotlib.pyplot as plt
import numpy as np

# Raw data
rawData = {
    "success": {
        "size1": [
            {"Sample": 17.44, "MoveTo": 22.58, "FSPlan": 20.50, "Qlearning": 100.00},
            {"Sample": 33.96, "MoveTo": 83.49, "FSPlan": 83.20, "Qlearning": 100.00},
            {"Sample": 12.53, "MoveTo": 49.76, "FSPlan": 52.20, "Qlearning": 100.00},
            {"Sample": 29.10, "MoveTo": 21.51, "FSPlan": 33.00, "Qlearning": 100.00},
            {"Sample": 18.97, "MoveTo": 21.61, "FSPlan": 27.10, "Qlearning": 100.00}
        ],
        "size2": [
            {"Sample": 5.16, "MoveTo": 30.11, "FSPlan": 31.60, "Qlearning": 100.00},
            {"Sample": 3.69, "MoveTo": 11.21, "FSPlan": 10.20, "Qlearning": 100.00},
            {"Sample": 2.77, "MoveTo": 11.35, "FSPlan": 7.90, "Qlearning": 100.00},
            {"Sample": 8.11, "MoveTo": 18.07, "FSPlan": 19.30, "Qlearning": 100.00},
            {"Sample": 24.43, "MoveTo": 79.84, "FSPlan": 80.90, "Qlearning": 100.00}
        ],
        "size3": [
            {"Sample": 2.03, "MoveTo": 8.35, "FSPlan": 6.20, "Qlearning": 100.00},
            {"Sample": 2.83, "MoveTo": 7.49, "FSPlan": 11.80, "Qlearning": 100.00},
            {"Sample": 4.74, "MoveTo": 22.81, "FSPlan": 27.20, "Qlearning": 100.00},
            {"Sample": 3.48, "MoveTo": 20.55, "FSPlan": 22.70, "Qlearning": 100.00},
            {"Sample": 1.93, "MoveTo": 8.04, "FSPlan": 4.60, "Qlearning": 50.01}
        ],
        "size4": [
            {"Sample": 0.31, "MoveTo": 0.98, "FSPlan": 0.50, "Qlearning": 19.58},
            {"Sample": 3.29, "MoveTo": 9.77, "FSPlan": 10.90, "Qlearning": 100.00},
            {"Sample": 3.36, "MoveTo": 5.91, "FSPlan": 9.70, "Qlearning": 100.00},
            {"Sample": 0.79, "MoveTo": 2.47, "FSPlan": 1.70, "Qlearning": 50.20},
            {"Sample": 5.74, "MoveTo": 7.93, "FSPlan": 8.50, "Qlearning": 100.00}
        ],
        "size5": [
            {"Sample": 2.19, "MoveTo": 2.48, "FSPlan": 5.30, "Qlearning": 100.00},
            {"Sample": 0.84, "MoveTo": 3.53, "FSPlan": 2.60, "Qlearning": 37.13},
            {"Sample": 0.84, "MoveTo": 4.68, "FSPlan": 5.60, "Qlearning": 57.99},
            {"Sample": 0.80, "MoveTo": 1.37, "FSPlan": 3.20, "Qlearning": 100.00},
            {"Sample": 0.24, "MoveTo": 0.71, "FSPlan": 0.90, "Qlearning": 8.80}
        ],
        "size6": [
            {"Sample": 0.19, "MoveTo": 0.66, "FSPlan": 0.70, "Qlearning": 5.15},
            {"Sample": 0.44, "MoveTo": 1.49, "FSPlan": 1.30, "Qlearning": 25.08},
            {"Sample": 0.21, "MoveTo": 0.85, "FSPlan": 0.80, "Qlearning": 12.69},
            {"Sample": 0.96, "MoveTo": 2.69, "FSPlan": 2.80, "Qlearning": 100.00},
            {"Sample": 0.17, "MoveTo": 0.65, "FSPlan": 0.40, "Qlearning": 8.78}
        ]
    },
    "steps": {
        "size1": [
            {"Sample": 28.41, "MoveTo": 13.15, "FSPlan": 13.37, "Qlearning": 27.39},
            {"Sample": 32.25, "MoveTo": 19.19, "FSPlan": 19.02, "Qlearning": 19.92},
            {"Sample": 23.64, "MoveTo": 18.13, "FSPlan": 19.04, "Qlearning": 21.82},
            {"Sample": 39.47, "MoveTo": 13.65, "FSPlan": 16.65, "Qlearning": 30.57},
            {"Sample": 24.32, "MoveTo": 11.76, "FSPlan": 12.65, "Qlearning": 20.44}
        ],
        "size2": [
            {"Sample": 18.59, "MoveTo": 18.85, "FSPlan": 18.31, "Qlearning": 25.14},
            {"Sample": 16.17, "MoveTo": 12.70, "FSPlan": 12.76, "Qlearning": 26.66},
            {"Sample": 15.32, "MoveTo": 12.09, "FSPlan": 12.58, "Qlearning": 27.83},
            {"Sample": 17.95, "MoveTo": 11.40, "FSPlan": 11.94, "Qlearning": 23.97},
            {"Sample": 26.56, "MoveTo": 18.61, "FSPlan": 19.10, "Qlearning": 20.78}
        ],
        "size3": [
            {"Sample": 14.27, "MoveTo": 11.11, "FSPlan": 10.98, "Qlearning": 36.11},
            {"Sample": 14.33, "MoveTo": 10.37, "FSPlan": 13.37, "Qlearning": 37.51},
            {"Sample": 14.18, "MoveTo": 13.45, "FSPlan": 14.11, "Qlearning": 20.89},
            {"Sample": 13.36, "MoveTo": 13.15, "FSPlan": 14.85, "Qlearning": 24.42},
            {"Sample": 19.37, "MoveTo": 14.98, "FSPlan": 12.54, "Qlearning": 62.56}
        ],
        "size4": [
            {"Sample": 10.39, "MoveTo": 9.10, "FSPlan": 7.60, "Qlearning": 31.03},
            {"Sample": 12.81, "MoveTo": 11.01, "FSPlan": 11.53, "Qlearning": 38.76},
            {"Sample": 16.38, "MoveTo": 11.19, "FSPlan": 12.11, "Qlearning": 24.04},
            {"Sample": 13.11, "MoveTo": 9.73, "FSPlan": 9.51, "Qlearning": 39.99},
            {"Sample": 9.19, "MoveTo": 10.81, "FSPlan": 10.47, "Qlearning": 28.24}
        ],
        "size5": [
            {"Sample": 5.60, "MoveTo": 5.70, "FSPlan": 6.10, "Qlearning": 22.87},
            {"Sample": 6.55, "MoveTo": 5.82, "FSPlan": 5.63, "Qlearning": 31.99},
            {"Sample": 8.17, "MoveTo": 6.50, "FSPlan": 5.94, "Qlearning": 25.56},
            {"Sample": 7.72, "MoveTo": 5.13, "FSPlan": 4.35, "Qlearning": 35.22},
            {"Sample": 9.33, "MoveTo": 7.64, "FSPlan": 7.38, "Qlearning": 30.49}
        ],
        "size6": [
            {"Sample": 4.16, "MoveTo": 3.91, "FSPlan": 3.81, "Qlearning": 22.88},
            {"Sample": 3.98, "MoveTo": 4.05, "FSPlan": 3.73, "Qlearning": 27.94},
            {"Sample": 5.06, "MoveTo": 5.23, "FSPlan": 5.02, "Qlearning": 23.14},
            {"Sample": 4.25, "MoveTo": 3.57, "FSPlan": 4.59, "Qlearning": 31.61},
            {"Sample": 3.92, "MoveTo": 3.60, "FSPlan": 4.36, "Qlearning": 27.31}
        ]
    }
}

methods = ['Sample', 'MoveTo', 'FSPlan', 'Qlearning']
sizes = range(1, 7)
n_methods = len(methods)
n_sizes = len(sizes)
bar_width = 0.2

data = np.zeros((n_methods, n_sizes))
for i, method in enumerate(methods):
    for j, size in enumerate(sizes):
        values = [entry[method] for entry in rawData['success'][f'size{size}']]
        data[i, j] = np.mean(values)

fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(n_sizes)
for i in range(n_methods):
    ax.bar(x + i * bar_width, data[i], bar_width, label=methods[i])

ax.set_xlabel('# of Hole(s)')
ax.set_ylabel('Success Rate')
ax.set_xticks(x + bar_width * (n_methods-1)/2)
ax.set_xticklabels([f'{size}' for size in sizes])
ax.legend()
plt.tight_layout()
plt.show()