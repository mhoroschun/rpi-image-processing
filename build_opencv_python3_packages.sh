
sudo apt-get update

sudo apt-get install -y build-essential git cmake pkg-config
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk2.0-dev
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y libprotobuf-dev
sudo apt-get install -y libopenexr-dev
sudo apt-get install -y libdc1394-22-dev

cd ~
git clone https://github.com/Itseez/opencv.git
cd opencv
git checkout 3.2.0

cd ~
git clone https://github.com/Itseez/opencv_contrib.git
cd opencv_contrib
git checkout 3.2.0

sudo pip3 install numpy
mkdir -p ~/opencv
cd ~/opencv
mkdir -p build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D ENABLE_PRECOMPILED_HEADERS=OFF \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D CPACK_BINARY_DEB:BOOL=ON \
    -D BUILD_EXAMPLES=ON .. 

make -j4
sudo make package 
