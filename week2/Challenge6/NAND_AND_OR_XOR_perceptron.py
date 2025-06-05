import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Set the path to FFmpeg if it's not being recognized
os.environ['FFMPEG_BINARY'] = r'C:\Users\Student\PythonS\ffmpeg\bin\ffmpeg.exe'  # Update this path to where FFmpeg is located

# Perceptron Activation Function (Sigmoid)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Perceptron Model
class Perceptron:
    def __init__(self, n_inputs, learning_rate=0.1):
        self.n_inputs = n_inputs
        self.learning_rate = learning_rate
        self.weights = np.random.rand(n_inputs + 1)  # Include the bias weight

    def predict(self, inputs):
        weighted_sum = np.dot(inputs, self.weights[1:]) + self.weights[0]  # Bias weight at index 0
        return sigmoid(weighted_sum)

    def train(self, X, y, epochs=100):
        history = []  # To store weights for animation
        for _ in range(epochs):
            for inputs, target in zip(X, y):
                prediction = self.predict(inputs)
                error = target - prediction
                self.weights[1:] += self.learning_rate * error * inputs  # Update weights (excluding bias)
                self.weights[0] += self.learning_rate * error  # Update bias
            history.append(self.weights.copy())  # Store weights for animation
        return history

# Function to create training data for different gates
def get_gate_data(gate_type, num_inputs):
    if gate_type == "NAND":
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([1, 1, 1, 0])  # NAND Gate Outputs
    elif gate_type == "AND":
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 0, 0, 1])  # AND Gate Outputs
    elif gate_type == "OR":
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 1])  # OR Gate Outputs
    elif gate_type == "XOR":
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 0])  # XOR Gate Outputs
    else:
        raise ValueError("Unsupported gate type")
    return X, y

# Animation Function
def animate_perceptron(X, y, history, save_as_mp4=False):
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.bwr)

    def plot_decision_boundary(ax, weights, x_min, x_max):
        x = np.linspace(x_min, x_max, 100)
        y = -(weights[1] * x + weights[0]) / weights[2]  # Assuming the model is 3D (2 inputs + 1 bias)
        ax.plot(x, y, label="Decision Boundary", color="k", linestyle="--")

    def update(frame):
        ax.cla()  # Clear the axis
        ax.set_xlim(-1, 2)
        ax.set_ylim(-1, 2)
        w = history[frame]
        plot_decision_boundary(ax, w, 0, 2)
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.bwr)

    ani = animation.FuncAnimation(fig, update, frames=len(history), interval=100, repeat=False)

    if save_as_mp4:
        writer = animation.FFMpegWriter(fps=1, metadata=dict(artist='Perceptron'), bitrate=1800)
        ani.save(f"{gate_type.lower()}_perceptron_animation.mp4", writer=writer)
        print(f"Animation saved as '{gate_type.lower()}_perceptron_animation.mp4'")

    plt.show()

# Main Program
if __name__ == "__main__":
    gate_type = input("Enter gate type (NAND, AND, OR, XOR): ").upper()
    num_inputs = int(input("Enter number of inputs: "))
    
    # Get the gate data
    X, y = get_gate_data(gate_type, num_inputs)

    # Initialize Perceptron
    perceptron = Perceptron(n_inputs=num_inputs)
    history = perceptron.train(X, y, epochs=100)  # Train and record history

    # Animate the learning process
    animate_perceptron(X, y, history, save_as_mp4=True)
