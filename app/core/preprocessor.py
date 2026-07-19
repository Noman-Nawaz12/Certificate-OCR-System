"""
Image preprocessing utilities to improve OCR accuracy.
"""
import cv2
import numpy as np


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load an image and apply a series of enhancements to make text
    easier for Tesseract to read:
    - grayscale conversion
    - thresholding (binarization)
    - noise removal
    - deskewing (straightening tilted scans)

    Returns the processed image as a numpy array (ready for OCR).
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adaptive thresholding handles uneven lighting better than a fixed value
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 15
    )

    # Remove speckle noise
    denoised = cv2.fastNlMeansDenoising(thresh, h=30)

    # Deskew (straighten) the image if it's tilted
    denoised = _deskew(denoised)

    return denoised


def _deskew(image: np.ndarray) -> np.ndarray:
    """Detects and corrects slight rotation in scanned documents."""
    coords = np.column_stack(np.where(image > 0))
    if coords.size == 0:
        return image

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = 90 + angle
    else:
        angle = angle

    # Ignore negligible skew to avoid unnecessary distortion
    if abs(angle) < 0.5:
        return image

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    return rotated
