import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        pass
    def order_points(self,pts):

        rect = np.zeros((4,2), dtype = "float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect
    
    def deskew(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 75, 200)
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        doc_contour = None
        for c in contours:
            epsilon = 0.02 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            if len(approx) == 4:
                doc_contour = approx
                break
        if doc_contour is not None:

            rect = self.order_points(doc_contour.reshape(4,2))
            (tl, tr, br, bl) = rect    
            widthA = np.sqrt((br[0]-bl[0])**2 + (br[1]-bl[1])**2)
            widthB = np.sqrt((tr[0]-tl[0])**2 + (tr[1]-tl[1])**2) 
            maxWidth = max(int(widthA),int(widthB))

            heightA = np.sqrt((tr[0]-br[0])**2 + (tr[1]-br[1])**2)
            heightB = np.sqrt((tl[0]-bl[0])**2 + (tl[1]-bl[1])**2)
            maxHeight = max(int(heightA), int(heightB))

            dst = np.array([
            [0,0],
            [maxWidth-1,0],
            [maxWidth-1, maxHeight-1],
            [0, maxHeight-1]],
            dtype = "float32"
            )
            matrix = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(image, matrix, (maxWidth,maxHeight))
            return warped
        else:
            coords = np.column_stack(np.where(edges>0))
            if len(coords) == 0:
                return image
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle =  -angle
            if abs(angle) < 0.5:
                return image
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(
                image,
                rotation_matrix,
                (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )
        return rotated
    
    def binarize(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(5,5),0)
        thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
        )
        return thresh