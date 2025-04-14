Open Google Colab at https://colab.research.google.com.

Create a new notebook.

Paste the full corrected code from above into a cell.

Install FFmpeg (in a separate cell):

!apt-get update
!apt-get install -y ffmpeg

Run the notebook, and the animation will be saved as perceptron_learning.mp4.

Download the video in another cell:

from google.colab import files
files.download("perceptron_learning.mp4")
