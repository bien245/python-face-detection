import cv2
import dlib

def draw_points(mat, landmarks, start, end, is_closed=False):
    points = [landmarks.part(i) for i in range(start, end+1)]
    for i in range(len(points)-1):
        cv2.line(mat, (points[i].x, points[i].y), (points[i+1].x, points[i+1].y), (0, 255, 0), 1)
    if is_closed:
        cv2.line(mat, (points[-1].x, points[-1].y), (points[0].x, points[0].y), (0, 255, 0), 1)

def main():
    # Khởi tạo detector khuôn mặt và predictor 68 điểm landmark
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("C:/Users/white.DESKTOP-GJ9453F/Downloads/shape_predictor_68_face_landmarks_GTX.dat/shape_predictor_68_face_landmarks_GTX.dat") # đường dẫn đến file pretrained

    # Đọc video từ webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, mat = cap.read()
        if not ret:
            break


        gray = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            draw_points(mat, landmarks, 0, 16)
            draw_points(mat, landmarks, 17, 21)
            draw_points(mat, landmarks, 22, 26)
            draw_points(mat, landmarks, 27, 30)
            draw_points(mat, landmarks, 30, 35, True)
            draw_points(mat, landmarks, 36, 41, True)
            draw_points(mat, landmarks, 42, 47, True)
            draw_points(mat, landmarks, 48, 59, True)
            draw_points(mat, landmarks, 60, 67, True)
        cv2.imshow("Face Landmarks", mat)

        # Thoát nếu nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng bộ nhớ và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
