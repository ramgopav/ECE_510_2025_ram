import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# Sample dataset (2D points, binary labels)
X = np.array([
    [2, 3],
    [4, 5],
    [5, 2],
    [1, 1],
    [2, 1],
    [6, 4]
])
y = np.array([1, 1, 1, -1, -1, -1])  # Labels must be +1 or -1

# Perceptron training with weight history
def perceptron_train(X, y, learning_rate=1.0, epochs=10):
    w = np.zeros(3)  # [bias, w1, w2]
    history = [w.copy()]
    for epoch in range(epochs):
        for i in range(len(X)):
            x_i = np.insert(X[i], 0, 1)  # Add bias input
            if y[i] * np.dot(w, x_i) <= 0:
                w += learning_rate * y[i] * x_i
                history.append(w.copy())
    return history

# Plot decision boundary
def plot_decision_boundary(ax, w, xmin, xmax):
    if w[2] != 0:
        x_vals = np.array([xmin, xmax])
        y_vals = -(w[1] * x_vals + w[0]) / w[2]
        ax.plot(x_vals, y_vals, 'k--')
    else:
        ax.axvline(-w[0]/w[1], color='k', linestyle='--')

# Animate learning process and save as MP4
def animate_perceptron(X, y, history, save_as_mp4=True):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 7)
    ax.set_title("Perceptron Learning Process")

    for label, marker, color in zip([-1, 1], ['o', 's'], ['red', 'blue']):
        ax.scatter(X[y == label, 0], X[y == label, 1], c=color, marker=marker, label=f'Class {label}')
    ax.legend()

    def update(frame):
        ax.clear()  # Clear the existing plot
        ax.set_xlim(0, 7)
        ax.set_ylim(0, 7)
        ax.set_title(f"Step {frame}")
        
        # Plot data points again
        for label, marker, color in zip([-1, 1], ['o', 's'], ['red', 'blue']):
            ax.scatter(X[y == label, 0], X[y == label, 1], c=color, marker=marker, label=f'Class {label}')
        
        # Plot the decision boundary for this step
        w = history[frame]
        plot_decision_boundary(ax, w, 0, 7)
        return ax.lines

    anim = FuncAnimation(fig, update, frames=len(history), interval=1000, repeat=False)

    if save_as_mp4:
        writer = FFMpegWriter(fps=1, metadata=dict(artist='Perceptron'), bitrate=1800)
        anim.save("perceptron_learning.mp4", writer=writer)
        print("MP4 saved as 'perceptron_learning.mp4'")

    plt.show()