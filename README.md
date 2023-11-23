# Introduction

This Python program, created by Ahmad Arif Sultoni, is designed for image processing tasks. The main objective is to analyze images, detect objects, and apply color-coded annotations based on certain criteria. The program utilizes the OpenCV library for image processing and manipulation.

# Running Using Executable


# Running Using Python Code

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/arifsoul/tips_inspections.git
   ```

2. Navigate to the project directory:

   ```bash
   cd repository
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the program, you need to configure the parameters in the `config.py` file. This file includes essential settings for image processing, such as rules, transparency, epsilon value, kernel sizes, folder paths, file extensions, and threshold values.

## Usage

To use the program, follow these steps:

1. Ensure that your input images are located in the specified `input_folder_path`.

2. Run the main script:

   ```bash
   inspections.py
   ```

3. The program will process each image in the input folder according to the defined rules and parameters. The annotated images will be saved in the specified `output_folder_path`.

## Results

The output images are color-coded based on the detected features, such as the number of angles and the percentage of a circular object in the image. The color codes represent different categories, as defined in the `config.py` file.

The program also provides textual information on the detected angles and circle percentage, displayed on the processed images.

## Example

Here is an example of the program's output structure:

```
result/
|-- GO/
|   |-- GO_image1.jpg
|   |-- GO_image2.jpg
|-- GO_arguably/
|   |-- GO_arguably_image3.jpg
|   |-- GO_arguably_image4.jpg
|-- NG/
|   |-- NG_image5.jpg
|   |-- NG_image6.jpg
```

In this example, images are categorized into different folders based on the defined rules.

## License

This program is distributed under the [MIT License](LICENSE). Feel free to modify and use it in your projects.