'''
Created by: Ahmad Arif Sultoni

'''
import cv2
import numpy as np
import os
import shutil
import configparser

from skimage import exposure


def read_config(file_path='config.cfg'):
    config = configparser.ConfigParser()
    config.read(file_path)

    rules = dict(config['Rules'])
    transparency = float(config['Settings']['transparency'])
    epsilon_value = float(config['Settings']['epsilon_value'])
    kernel_blur = int(config['Settings']['kernel_blur'])
    kernel_smooth = int(config['Settings']['kernel_smooth'])
    input_folder_path = config['Paths']['input_folder_path']
    output_folder_path = config['Paths']['output_folder_path']
    extensions = tuple(config['FileExtensions']['extensions'].split())
    light_threshold = int(config['Thresholds']['light_threshold'])
    dark_threshold = int(config['Thresholds']['dark_threshold'])
    font_color = tuple(map(int, config['Colors']['font_color'].split(',')))

    return (
        rules, transparency, epsilon_value, kernel_blur, kernel_smooth,
        input_folder_path, output_folder_path, extensions,
        light_threshold, dark_threshold, font_color
    )

def count_angles(approx):
    # Count the number of angles in the contour approximation
    num_angles = len(approx)
    return num_angles

def process_images(input_folder, output_folder):

    # Get the list of image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith(extensions)]

    for image_file in image_files:
        # Read the image from the file
        image_path = os.path.join(input_folder, image_file)
        original_image = cv2.imread(image_path)

        # Apply Gaussian filter to the image
        original_image_blurred = cv2.GaussianBlur(original_image, ksize=(kernel_blur, kernel_blur), sigmaX=0, sigmaY=0)

        # Convert the image to HSV format
        hsv_image = cv2.cvtColor(original_image_blurred, cv2.COLOR_BGR2HSV)

        # Split the image into H, S, V channels
        ha, es, ve = cv2.split(hsv_image)

        # Perform operations on the ve (Value) channel

        # Detect edges using Canny on the ve channel
        edges = cv2.Canny(ve, 30, 90)

        # Closing to fill small holes
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        # Find contours in the closed image
        contours, _ = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Choose the contour with the largest area if any contours are present
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            # Approximate the curve of the largest contour
            epsilon = epsilon_value * cv2.arcLength(largest_contour, True)
            approximated_contour = cv2.approxPolyDP(largest_contour, epsilon, True)

            
            # Get the bounding box of the main contour
            x, y, w, h = cv2.boundingRect(approximated_contour)
            
            
            bbox_padding = int((w+h)/4)
            
            # Add padding of 10 pixels to the bounding box
            x_light = x - bbox_padding
            y_light = y - bbox_padding
            w_light = w + 2 * bbox_padding
            h_light = h + 2 * bbox_padding

            # Ensure the coordinates are within the image boundaries
            x_light = max(0, x_light)
            y_light = max(0, y_light)

            # Get the area covered by the enlarged bounding box
            roi_dark = ve[y:y+h, x:x+w]
            roi_light = ve[y_light:y_light+h_light, x_light:x_light+w_light]

            _, dark_mask = cv2.threshold(roi_dark, dark_threshold, 255, cv2.THRESH_BINARY_INV)
            
            # Identify light pixels using thresholding
            _, light_mask = cv2.threshold(roi_light, light_threshold, 255, cv2.THRESH_BINARY)

            # Find contours in the dark_mask
            contours_dark_mask, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Find contours in the light_mask
            contours_light_mask, _ = cv2.findContours(light_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            masks = {
                'Dark': [dark_mask, contours_dark_mask],
                'Light': [light_mask, contours_light_mask],
                }
            
            center_dark = 0
            radius_dark = 0
            num_dark_angles = 0
            percentage_circle_dark = 0
            category = 'not defined'
            
            transparant_mask_light = np.zeros_like(original_image)
            transparant_mask_dark = np.zeros_like(original_image)

            ypos = 50
            
            for mask in masks:
                    
                # Choose the contour with the largest area if any contours are present
                if masks[mask][1]:
                    largest_contour_mask = max(masks[mask][1], key=cv2.contourArea)
                    # Approximate the curve of the largest contour
                    epsilon_mask = epsilon_value * cv2.arcLength(largest_contour_mask, True)
                    approximated_contour_mask = cv2.approxPolyDP(largest_contour_mask, epsilon_mask, True)
                
                    # Count the number of angles in the contour of masks[mask][0]
                    num_angles = count_angles(approximated_contour_mask)
                
                else:
                    num_angles = 0

                score = num_angles
                
            
                if mask == 'Dark':
                    # Create an empty mask with the same size as the original mask
                    circle_mask = np.zeros_like(masks[mask][0])
                    
                    # Draw the circle on the empty mask
                    cv2.drawContours(circle_mask, [largest_contour_mask], 0, (255), thickness=cv2.FILLED)

                    # Calculate the area of the circle
                    circle_area_dark = np.sum(circle_mask == 255)

                    # Calculate the radius of the circle based on the area of circle_mask
                    radius_dark = int(np.sqrt(circle_area_dark / np.pi))

                    # Find the center coordinates of the bounding box
                    center_dark = (x + w // 2, y + h // 2)
    
                    # Calculate the total area of the original mask
                    total_area = np.sum(masks[mask][0] == 255)

                    # Calculate the percentage of the circle
                    percentage_circle_dark = (circle_area_dark / total_area) * 100
                    
                    if percentage_circle_dark > 100:
                        percentage_circle_dark = int(percentage_circle_dark - 100)
                        
                    else:
                        percentage_circle_dark = int(percentage_circle_dark)
                        
                # Rescale intensity of masks[mask][0] to enhance contrast
                contrast = exposure.rescale_intensity(masks[mask][0], in_range=(100, 200), out_range=(0, 255)).clip(0, 255).astype(np.uint8)

                # Apply smoothing (blurring) operation on the contour area inside the bounding box
                masker = cv2.GaussianBlur(contrast, (kernel_smooth, kernel_smooth), 0)

                # Draw the number of angles on the original image
                font = cv2.FONT_HERSHEY_SIMPLEX
                    
                cv2.putText(original_image, f'{mask} Angles     : {num_angles}', (10, ypos), font, 1, font_color, 2, cv2.LINE_AA)
                ypos += 50
                
                # Default color for dark objects is blue
                color = [255, 0, 0]
                filename = f'{image_file}'
                
                # Update color and filename based on the number of angles
                if percentage_circle_dark == key_1:
                    dir = rules[key_1]
                    name = f'{dir}_{image_file}'
                    filename = os.path.join(dir, name)
                    color = [0, 255, 0] #green
                    category = 'GO'
                    
                if key_2 <= percentage_circle_dark < key_1:
                    dir = rules[key_2]
                    name = f'{dir}_{image_file}'
                    filename = os.path.join(dir, name)
                    color = [0, 255, 255] #yellow
                    category = 'Arguably Good'
                    
                if percentage_circle_dark <= key_3 or score == 0 :
                    dir = rules[key_3]
                    name = f'{dir}_{image_file}'
                    filename = os.path.join(dir, name)
                    color = [0, 0, 255] #red
                    category = 'NG'
                
                if mask == 'Light':
                    
                    x = x_light
                    y = y_light
                    w = w_light
                    h = h_light
                    ypos = 100
                    
                    min_value = min(num_angles, num_dark_angles)
                    if min_value != 0:
                        score = (num_angles + num_dark_angles)/2
                    else:
                        score = 0
                
                if mask == 'Dark':
                    transparant_mask_dark[y:y+h, x:x+w][masker < dark_threshold] = color
                    cv2.putText(original_image, f'Hole Circle       : {percentage_circle_dark} %', (10, ypos+50), font, 1, font_color, 2, cv2.LINE_AA)
                    num_dark_angles = num_angles
                       
                if mask == 'Light':
                    transparant_mask_light[y:y+h, x:x+w][masker > light_threshold] = color
                    
                    
                
            
            # Combine transparant_mask_light and transparant_mask_dark using bitwise_or
            transparant_mask_combined = cv2.bitwise_or(transparant_mask_light, transparant_mask_dark)
            
            # Blend the original image with the combined transparent mask using alpha blending
            result = cv2.addWeighted(original_image, 1, transparant_mask_combined, transparency, 0)

            cv2.putText(result, f'Category          : {category}', (10, ypos+150), font, 1, tuple(color), 2, cv2.LINE_AA)
            
            # Draw bounding box on the original image
            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 255, 0), 2)
            
            # Draw rectangle based on center and radius
            cv2.rectangle(result, (center_dark[0] - radius_dark, center_dark[1] - radius_dark), (center_dark[0] + radius_dark, center_dark[1] + radius_dark), (255, 0, 255), 2)

            # Save the resulting image to the output folder
            output_path = os.path.join(output_folder, filename)
            print(f'output : {output_path}')
            cv2.imwrite(output_path, result)
            
        else:
            print(f'File {image_file} Corrupt!!!')
            filename = f'Corrupt_{image_file}'
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, original_image)
            

if __name__ == "__main__":
    (
        rules, transparency, epsilon_value, kernel_blur, kernel_smooth,
        input_folder_path, output_folder_path, extensions,
        light_threshold, dark_threshold, font_color
    ) = read_config()
    
    # Convert keys to integer
    rules = {int(key): value for key, value in rules.items()}
    
    # Extract keys from the rules dictionary
    key_1 = list(rules.keys())[0]
    key_2 = list(rules.keys())[1]
    key_3 = list(rules.keys())[2]

    # Extract all the values from the rules dictionary
    list_values = list(rules.values())
    # Check if the output folder already exists
    if os.path.exists(output_folder_path):
        # Remove all contents of the folder (files and subfolders)
        shutil.rmtree(output_folder_path)

    # Recreate the output folder
    for value in list_values:
        folder = os.path.join(output_folder_path, value)
        os.makedirs(folder)
        
        
    process_images(input_folder_path, output_folder_path)
