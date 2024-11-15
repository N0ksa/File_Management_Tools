import cv2
import numpy as np
import math
from PIL import Image as PILImage


class ImageToPdfScanner:
    def __init__(self, input_image_path, output_pdf_path):
        self.input_image_path = input_image_path
        self.output_pdf_path = output_pdf_path

    def load_image(self):
        image = cv2.imread(self.input_image_path, cv2.IMREAD_COLOR)
        if image is None:
            print(f"ERROR: Couldn't find an image at the path: {self.input_image_path}.")
            exit()
        return image

    def resize_image(self, image, width=800, height=600):
        # Resize the image to the specified width and height for display
        return cv2.resize(image, (width, height))

    def preprocess_image(self, image):
        # Step 0: Show original image
        resized_original = self.resize_image(image)
        cv2.imshow("Original Image", resized_original)  # Show original image
        cv2.waitKey(0)

        # Step 1: Convert to grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized_grayscale = self.resize_image(grayscale_image)

        cv2.imshow("Grayscale Image", resized_grayscale)  # Show grayscale image
        cv2.waitKey(0)

        # Step 2: Apply Gaussian Blur
        blurred_image = cv2.GaussianBlur(grayscale_image, (99, 99), 0)

        resized_blurred = self.resize_image(blurred_image)
        cv2.imshow("Blurred Image", resized_blurred)  # Show blurred image
        cv2.waitKey(0)

        # Step 3: Thresholding
        _, binary_image = cv2.threshold(blurred_image, 90, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        resized_binary = self.resize_image(binary_image)
        cv2.imshow("Binary Image", resized_binary)  # Show binary image
        cv2.waitKey(0)

        # Step 4: Find contours
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Step 5: Draw contours in black and white
        contour_image_bw = np.zeros_like(binary_image)  # Create a black image
        cv2.drawContours(contour_image_bw, contours, -1, (255), 1)  # Draw white contours

        resized_contour_bw = self.resize_image(contour_image_bw)
        cv2.imshow("Contours (Black and White)", resized_contour_bw)  # Show contours in black and white
        cv2.waitKey(0)

        # Step 6: Approximate polygon and calculate the corner points
        largest_contour = max(contours, key=cv2.contourArea)
        epsilon = 0.1 * cv2.arcLength(largest_contour, True)
        approx_polygon = cv2.approxPolyDP(largest_contour, epsilon, True)
        point1 = approx_polygon[0][0]
        point2 = approx_polygon[1][0]
        point3 = approx_polygon[2][0]
        point4 = approx_polygon[3][0]

        # Draw approximated polygon on the image
        approx_polygon_image = image.copy()
        cv2.polylines(approx_polygon_image, [approx_polygon], isClosed=True, color=(0, 255, 0), thickness=3)

        resized_approx_image = self.resize_image(approx_polygon_image)
        cv2.imshow("Approximated Polygon", resized_approx_image)  # Show approximated polygon
        cv2.waitKey(0)

        # Step 7: Calculate edges and decide on the corners' order
        edge1 = math.sqrt(((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2))
        edge2 = math.sqrt(((point2[0] - point3[0]) ** 2) + ((point2[1] - point3[1]) ** 2))
        edge3 = math.sqrt(((point3[0] - point4[0]) ** 2) + ((point3[1] - point4[1]) ** 2))
        edge4 = math.sqrt(((point4[0] - point1[0]) ** 2) + ((point4[1] - point1[1]) ** 2))

        side_1 = round(min(edge1, edge3))
        side_2 = round(min(edge2, edge4))

        if side_1 > side_2:
            height = side_1
            width = side_2
            ordered_corners = [point1, point4, point2, point3]
        else:
            height = side_2
            width = side_1
            ordered_corners = [point2, point1, point3, point4]

        # Step 8: Perform perspective transform
        source_points = np.float32(ordered_corners)
        destination_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)

        transformed_image = cv2.warpPerspective(image, perspective_matrix, (width, height))

        resized_transformed = self.resize_image(transformed_image)
        cv2.imshow("Transformed Image", resized_transformed)  # Show transformed image
        cv2.waitKey(0)
        return transformed_image

    def save_image_as_pdf(self, transformed_image):
        try:
            pil_image = PILImage.fromarray(cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB))
            pil_image.save(self.output_pdf_path, "PDF")
            print(f"Processed image saved as PDF to {self.output_pdf_path}")
        except Exception as error:
            print(f"ERROR: Unable to save image as PDF. {error}")

    def process_and_save(self):
        image = self.load_image()

        try:
            transformed_image = self.preprocess_image(image)
        except Exception as error:
            print(f"ERROR: {error}")
            exit()

        self.save_image_as_pdf(transformed_image)


if __name__ == "__main__":
    input_image_path = r"C:\Users\phant\Desktop\slika.jpg"
    output_pdf_path = r"C:\Users\phant\Desktop\slikaOUT.pdf"

    scanner = ImageToPdfScanner(input_image_path, output_pdf_path)
    scanner.process_and_save()
