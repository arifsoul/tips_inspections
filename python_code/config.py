# Dictionary defining rules for color coding based on angle ranges
rules = {
    100 : 'GO',
    96  : 'GO_arguably',
    95  : 'NG',
}

# Transparency level for blending images
transparency = 0.2

# Epsilon value for contour approximation
epsilon_value = 0.005

# Kernel size for Gaussian blur
kernel_blur = 7

# Kernel size for smoothing
kernel_smooth = 7

input_folder_path = "test"
output_folder_path = "result"

# File extensions for image files
extensions = ('.jpg', '.jpeg', '.png')

light_threshold = 100
dark_threshold = 50