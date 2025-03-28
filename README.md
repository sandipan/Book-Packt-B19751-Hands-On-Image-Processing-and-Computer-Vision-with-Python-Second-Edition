# Hands-On-Image-Processing-with-Python-Second-Edition
Hands-On Image Processing with Python, Second Edition, Published by Packt

### Book Chapters

1.	Getting Started with Digital Image Processing
2.	Image Manipulation
3.	More Image Manipulation
4.	Sampling & Fourier Transform 
5.	Convolution & Frequency Domain Filtering
6.	Image Enhancement 
7.	Image Enhancements using Derivatives 
8.	Image Restoration
9.	Morphological Image Processing
10.	Extracting Image Features and Descriptors  
11.	Image Segmentation 
12.	Classical Machine Learning Methods 
13.	Deep Learning in Image Processing - Image Classification 
14.	Deep Learning in Image Processing - Object Detection, and more
15.	Additional Problems in Image Processing 


### Setting up different Image Processing Libraries in Python

The next few paragraphs describe how to install different image processing libraries and
setup the environment for writing codes to process images using the classical image
processing techniques in python. In the last few chapters of the book, we shall need to use a
different setup when we shall use deep-learning-based methods.


### 1 Installing pip

We are going to use the pip (or pip3) tool to install the libraries, so we need to
install pip first, in case it's not installed. As mentioned here, pip is already installed if we
use python 3 >=3.4 downloaded from python.org or if we are working in a Virtual
Environment created by virtualenv or pyvenv. Just we need to make sure to upgrade pip.
How to install pip for different OS / platforms can be found here.

### 2 Installing Some Image Processing Libraries in Python

In python, there are many libraries which we can use for image processing. Some of the
following libraries we are going to use are as below:

* numpy
* scipy
* scikit-image
* PIL (pillow)
* wand
* opencv-python
* scikit-learn
* mahotas
* matplotlib
* seaborn

The library `matplotlib` and `seaborn` will primarily be used for display purpose, where as
numpy will be used for storing an image. The scikit-learn library will be used for building
machine-learning models for image processing, scipy will be used mainly for image
enhancements. The scikit-image, mahotas and opencv will be used for different image
processing algorithms.

The following code block shows how the libraries that we are going to use can be
downloaded and installed with pip from a python prompt (interactive mode) or in jupyter notebook:


```python
!pip install numpy
!pip install scipy
!pip install scikit-image
!pip install scikit-learn
!pip install matplotlib
!pip install pillow
!pip install mahotas
!pip install opencv-python
!pip install jupyter
!pip install -U wand
```

There may be some additional installation instructions, depending on the OS platform one is going to use. We suggest the reader to go through the documentation sites for each of the
libraries to get a detailed platform-specific installation instructions for each library. For
example, for the scikit-image library, detailed installation instructions for different OS
platforms can be found here. Also, one should be familiar to websites such
as stackoverflow to resolve platform-dependent installation issues for different libraries.

Finally, we can verify whether a library is properly installed or not by importing it from the
python prompt. If the library is imported successfully (no error message is thrown), then
we don't have any installation issue. We can print the version of the library installed by
printing it to the console.

The following code block shows the same for the python library scikit-image.


```python
import skimage
print(skimage.__version__)
```

    0.17.2
    

As can be seen from above, an example output of the above code block 0.17.2.

The following code-block shows the version of PIL and numpy libraries, respectively, as a `tuple`:


```python
import PIL
import numpy
PIL.__version__, numpy.__version__
```


    ('8.3.2', '1.21.6')



Let's ensure that we have the latest versions for all the libraries.

### 3 Installing the Anaconda Distribution

We also recommend to download and install the latest version of the anaconda distribution
from here, this will eliminate the need of explicit installation of many python packages.

More about installing anaconda for different OS can be found '<here>'.
    
### 4 Installing Jupyter Notebook

We are going to use jupyter notebooks to write our python code. So we need to install
the jupyter package first from a python prompt with>>> pip install jupyter
and then launch the jupyter notebook app in the browser using>>> jupyter notebook
where we can create new python notebooks and choose a kernel. If we use anaconda, we do
not need to install jupyter explicitly, the latest anaconda distribution comes with jupyter.

More about running jupyter notebooks can be found here.

We can even install a python package from inside a notebook cell, e.g., we can
install scipy with the command !pip install scipy

For more information on installing Jupyter please
refer to: http://jupyter.readthedocs.io/en/latest/install.html   
