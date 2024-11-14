import cv2
import numpy as np


class DocumentScanner:
    def __init__(self, image_path):
        """
        Initialize the scanner with the image path.
        """
        self.image_path = image_path
        self.input_image = cv2.imread(image_path)  # Read the image
        self.resized_image = cv2.resize(self.input_image, (1800, 1600))  # Resize for processing (optional)
        self.original_image = self.resized_image.copy()  # Make a copy of the original image
        self.scanned_image = None  # Will hold the final scanned image

    def reorder_points(self, points):
        """
        Reorder the points to make sure they are in the correct order:
        top-left, top-right, bottom-right, bottom-left.
        """
        points = points.reshape((4, 2))
        ordered_points = np.zeros((4, 2), dtype=np.float32)

        # Sum of the points' coordinates to find the top-left and bottom-right
        sum_points = points.sum(axis=1)
        ordered_points[0] = points[np.argmin(sum_points)]  # Top-left point
        ordered_points[2] = points[np.argmax(sum_points)]  # Bottom-right point

        # Difference of the points' coordinates to find top-right and bottom-left
        diff_points = np.diff(points, axis=1)
        ordered_points[1] = points[np.argmin(diff_points)]  # Top-right point
        ordered_points[3] = points[np.argmax(diff_points)]  # Bottom-left point

        return ordered_points

    def process_image(self):
        """
        Process the image to find the document, extract the edges,
        and apply a perspective transform.
        """
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(self.resized_image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to the grayscale image
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        # Perform Canny edge detection
        edges = cv2.Canny(blurred_image, 30, 50)

        # Find contours in the edge-detected image
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Sort contours based on area (largest contour first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Find the contour with 4 corners (i.e., the document)
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx_corners = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            if len(approx_corners) == 4:
                document_contour = approx_corners
                break

        # Reorder the points to ensure the correct corners (top-left, top-right, bottom-right, bottom-left)
        ordered_points = self.reorder_points(document_contour)

        # Define the target points (for a new 800x800 image)
        target_points = np.float32([[0, 0], [800, 0], [800, 800], [0, 800]])

        # Calculate the perspective transform matrix
        perspective_matrix = cv2.getPerspectiveTransform(ordered_points, target_points)

        # Apply the perspective warp to the original image
        self.scanned_image = cv2.warpPerspective(self.original_image, perspective_matrix, (800, 800))

    def save_scanned_image(self, output_path):
        """
        Save the final scanned result as a JPEG image.
        """
        if self.scanned_image is not None:
            cv2.imwrite(output_path, self.scanned_image)
        else:
            print("Error: No scanned image available to save.")

    def show_scanned_image(self):
        """
        Display the scanned image.
        """
        if self.scanned_image is not None:
            cv2.imshow("Scanned Document", self.scanned_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Error: No scanned image available to display.")


# Example Usage
if __name__ == "__main__":
    # Initialize the scanner with the image path
    scanner = DocumentScanner(r"C:\Users\phant\Desktop\slika.jpg")

    # Process the image to scan the document
    scanner.process_image()

    # Save the scanned result
    output_path = r"C:\Users\phant\Desktop\scanned_output.jpg"
    scanner.save_scanned_image(output_path)

    # Optionally show the scanned image
    scanner.show_scanned_image()