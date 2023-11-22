# Image Processing README

## Introduction

This Python program, created by Ahmad Arif Sultoni, is designed for image processing tasks. The main objective is to analyze images, detect objects, and apply color-coded annotations based on certain criteria. The program utilizes the OpenCV library for image processing and manipulation.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/username/repository.git
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
   python main.py
   ```

3. The program will process each image in the input folder according to the defined rules and parameters. The annotated images will be saved in the specified `output_folder_path`.

## Results

The output images are color-coded based on the detected features, such as the number of angles and the percentage of a circular object in the image. The color codes represent different categories, as defined in the `config.py` file.

The program also provides textual information on the detected angles and circle percentage, displayed on the processed images.

## Example

Here is an example of the program's output structure:

```
output_folder/
|-- category_1/
|   |-- image1.jpg
|   |-- image2.jpg
|-- category_2/
|   |-- image3.jpg
|   |-- image4.jpg
|-- category_3/
|   |-- image5.jpg
|   |-- image6.jpg
```

In this example, images are categorized into different folders based on the defined rules.

## License

This program is distributed under the [MIT License](LICENSE). Feel free to modify and use it in your projects.

## Acknowledgments

Special thanks to Ahmad Arif Sultoni for creating this image processing tool.

If you have any questions or issues, please contact [author@example.com](mailto:author@example.com).

Happy image processing!
