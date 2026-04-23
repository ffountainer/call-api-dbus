from skimage.metrics import structural_similarity as ssim
import cv2


def compare_png(expected, actual) -> bool:
    img1 = cv2.imread(expected)
    img2 = cv2.imread(actual)

    if img1 is None or img2 is None:
        return False

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    score, diff = ssim(gray1, gray2, full=True)

    if score > 0.9:
        return True
    else:
        return False
