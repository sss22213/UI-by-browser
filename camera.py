import cv2
import threading

class mycamera:
    def __init__(self, device):
        # Initialize camera in lcoation of device
        self.camera = cv2.VideoCapture(device)

        # Catch first frame
        (fps, self.frame_origin) = self.camera.read()

        # Get calibrate image
        self.frame_calib = self.image_calibration(self.frame_origin)

        # Load haarcascade feature
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Add thread for reading
        threading.Thread(target=self.read_frame_forever, args=()).start()

    def image_calibration(self, img):
       return cv2.rotate(img, cv2.ROTATE_180)

    def read_frame_forever(self):
        while True:
            # Delay for 5 seconds
            cv2.waitKey(5)

            # Catch the frame
            (fps, self.frame_origin) = self.camera.read()

            # Calibrate image
            self.frame_calib = self.image_calibration(self.frame_origin)
            
            # Detect face
            self.face_detect(self.frame_calib)
            
    def get_frame(self):
        image = self.frame_calib

        # Convert raw image to jpeg
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def face_detect(self, frame):
        # For speed up, Convert RGB image to gray image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4, minSize = (200, 200))

        # Find maximum area
        max_rectangle = 0
        max_pos = None
        for (x, y, w, h) in faces:
            if w*h >= max_rectangle:
                max_pos = [x, y, w, h]
                max_rectangle = w*h
        if max_pos is not None:
            x, y, w, h = max_pos[0], max_pos[1], max_pos[2], max_pos[3]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 4)
            
def gen(camera):
    while True:
        frame_raw = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame_raw + b'\r\n\r\n')
