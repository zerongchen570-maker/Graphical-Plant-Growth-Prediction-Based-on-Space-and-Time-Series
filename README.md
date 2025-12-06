# CS230 Project: Graphical Plant Growth Prediction

This project implements deep learning models to predict the future appearance of a plant (Day 10) based on a sequence of early-stage growth images (Days 1-5).

## Models Implemented
The notebook contains four distinct architectures for spatiotemporal prediction:
* **3D U-Net:** Processes spatial and temporal dimensions simultaneously using 3D convolutions.
* **2D U-Net:** Adapts the standard U-Net by treating temporal frames as input channels.
* **ConvLSTM U-Net:** Uses Convolutional LSTM cells within a U-Net encoder-decoder to model temporal evolution.


## Loss Function
The training utilizes a `CombinedLoss` function consisting of:
* L1 Loss (pixel-wise accuracy)
* LPIPS Loss
* Perceptual Loss
* PSNR Loss
* Background Regularization and Color Difference Loss.

## Dependencies
* Python 3.x
* PyTorch, torchvision
* lpips, tqdm, numpy, matplotlib, PIL.

## Usage
1. Update the `DATA_ROOT` path in the `Config` class to point to the local dataset.
2. Select the desired model architecture by initializing it in the training block (e.g., `model = UNet3D(...)`).
3. Run the notebook cells to train, validate, and visualize predictions.
