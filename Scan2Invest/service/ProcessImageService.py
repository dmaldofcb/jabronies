import os
import cv2
from exceptions import ServiceExceptions


class ProcessImageService:
    
    def __init__(self) -> None:
        pass
    
    def preprocess_image(self, file):
    
        try:
            save_processed = "processed_image"
            image_path = self.pre_process_setup(file, save_processed)
            # Load and preprocess the image using OpenCV
            img = cv2.imread(image_path)
            # Check the file size
            file_size = os.path.getsize(image_path)
            max_size = 3.5*1024*1024
            
            print(f"Image file name: {file.filename} Size: {file_size}")

            # Resize the image
                # Resize the image if it's larger than max_size
            if file_size > max_size:
                # Calculate the scaling factor needed to reduce the image to under max_size
                # This is a simple approach and might need adjustment for your use case
                scale_factor = (max_size / file_size) ** 0.5  # Square root to account for 2 dimensions
                new_size = (int(img.shape[1] * scale_factor), int(img.shape[0] * scale_factor))
                
                img = cv2.resize(img, new_size)

            
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(img, (5, 5), 0)
            
            # Save or return the preprocessed image
            preprocessed_path = 'preprocessed_' + os.path.basename(image_path)
            filepath = os.path.join(save_processed, preprocessed_path)
            print(f"Filepath {filepath}")
            cv2.imwrite(filepath, blurred)
        except Exception as e:
            print(f"Failed to Preprocess image error: {e}")
            raise ServiceExceptions.ServiceError(f"Error Pre-Processing Image: {str(e)}")
    
        return filepath
    
    def pre_process_setup(self, file, save_directory):
        # Ensure the original image directory exists
        save_dir = 'original_image'
        os.makedirs(save_dir, exist_ok=True)
        
        # Ensure the processed directory exists
        os.makedirs(save_directory, exist_ok=True)
        
        # Save the file temporarily
        filepath = os.path.join(save_dir, file.filename)
        file.save(filepath)
        return filepath