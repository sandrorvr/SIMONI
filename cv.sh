#!/bin/bash

echo ""
echo "-----------------------------------------------"
echo "Instalacao de pacotes necessarios para o OpenCV"
echo "-----------------------------------------------"
echo ""

sudo apt-get install -y build-essential cmake unzip pkg-config
sudo apt-get install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk-3-dev
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y python3-dev


echo ""
echo "----------------------------------------"
echo "Download do codigo-fonte do OpenCV 3.1.0"
echo "----------------------------------------"
echo ""

cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip

unzip opencv.zip
unzip opencv_contrib.zip

mv opencv-4.0.0 opencv
mv opencv_contrib-4.0.0 opencv_contrib

echo ""
echo "------------------------------------------------------------------------"
echo "Instalacao do numpy "
echo "(pacote do Python para operacoes com arrays e matrizes multidimensionais"
echo "------------------------------------------------------------------------"
echo ""


echo ""
echo "--------------------------"
echo "Compilacao do OpenCV 3.1.0"
echo "--------------------------"
echo ""

cd ~/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	-D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
	-D BUILD_EXAMPLES=ON ..

make -j4

echo ""
echo "--------------------------"
echo "Instalacao do OpenCV 4.0.0"
echo "--------------------------"
echo ""

sudo make install

echo ""
echo "--------------------------------------------"
echo "cria links e cache para bibliotecas"
echo "recentemente adicionadas (no caso, o OpenCV)"
echo "--------------------------------------------"
echo ""

sudo ldconfig
