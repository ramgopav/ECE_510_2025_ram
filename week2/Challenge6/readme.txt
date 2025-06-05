 Challenge 6 · TwoInput Perceptron (Sigmoid)

This miniproject shows how a single sigmoid neuron (perceptron) learns
the logic gates NAND, AND, OR and _tries_ to learn XOR.  
During training the script records each weight vector and renders an
animated decision boundary, so you can literally watch learning happen.

<! If GitHub previews MP4, it displays; otherwise a screenshot works >
![NAND animation](nand_perceptron_animation.mp4)



 1 · File list

 File  Role 

 NAND_AND_OR_XOR_perceptron.py  Allinone script: data generator, perceptron class, training loop, Matplotlib animation 
 nand_perceptron_animation.mp4  Sample output for the 2input NAND gate 
 and_perceptron_animation.mp4   Sample output for the 2input AND gate 



 2 · Replicate the experiment (Linux/macOS)

bash
 1. Get into the project folder
git clone <your_repo_url>
cd Challenge_6           or the folder that contains the files

 2. Create a clean Python environment
python3 m venv .venv
source .venv/bin/activate
pip install numpy matplotlib         only two deps

 3. (Optional) install ffmpeg if you want MP4 saved
 sudo apt install ffmpeg            Debian/Ubuntu
 brew install ffmpeg                macOS

 4. Run the script
python NAND_AND_OR_XOR_perceptron.py
