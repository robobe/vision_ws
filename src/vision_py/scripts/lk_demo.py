import cv2
import numpy as np

feature_params = dict(maxCorners=100,
                    qualityLevel=0.3,
                    minDistance=7,
                    blockSize=7)
# Parameters for lucas kanade optical flow
lk_params = dict( winSize = (15, 15),
 maxLevel = 2,
 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

tracking_request = False
tracking_request_point = None
def draw_rectangle(event, x, y, flags, param):
    global tracking_request, tracking_request_point
    if event == cv2.EVENT_LBUTTONDOWN:
        tracking_request = True
        tracking_request_point = (x,y)
        

    # elif event == cv2.EVENT_MOUSEMOVE:
    #     if drawing:
    #         top_left_pt = (min(x_start, x), min(y_start, y))
    #         bottom_right_pt = (max(x_start, x), max(y_start, y))
    #         cv2.rectangle(frame, top_left_pt, bottom_right_pt, (0, 255, 0), 2)

    # elif event == cv2.EVENT_LBUTTONUP:
    #     drawing = False
    #     top_left_pt = (min(x_start, x), min(y_start, y))
    #     bottom_right_pt = (max(x_start, x), max(y_start, y))
    #     cv2.rectangle(frame, top_left_pt, bottom_right_pt, (0, 255, 0), 2)
    #     cv2.imshow("Frame", frame)

WINDOW_NAME = "Frame"
cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, draw_rectangle)

def main():
    global tracking_request, tracking_request_point
    # cv2.namedWindow("frame")
    # frame = cv2.imread("/home/user/workspaces/vision_ws/src/vision_py/scripts/lk_image.png")
    cap = cv2.VideoCapture("/home/user/workspaces/vision_ws/src/vision_py/scripts/slow_traffic_small.mp4")
    ret, old_frame = cap.read()
    print(old_frame.shape)
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = None
    # Create some random colors
    color = np.random.randint(0, 255, (100, 3))
    # for i in p0:
    #     x, y = i.ravel()
    #     print(x,y)
    #     cv2.circle(frame, (int(x), int(y)), 3, (0, 0, 255), -1)
    # cv2.imshow("Frame", frame)
    mask = np.zeros_like(old_frame)
    rect_width, rect_height = 100, 100
    while(1):
        ret, frame = cap.read()
        if not ret:
            print('No frames grabbed!')
            break
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # calculate optical flow
        if tracking_request:
            x, y = tracking_request_point
            mask = np.zeros_like(frame)
            feature_mask = np.zeros_like(frame_gray)
            top_left_pt = (x - rect_width // 2, y - rect_height // 2)
            bottom_right_pt = (x + rect_width // 2, y + rect_height // 2)
            feature_mask = cv2.rectangle(feature_mask, top_left_pt, bottom_right_pt, (255,255,255), -1)
            # print(np.shape(feature_mask))
            # cv2.waitKey(10000)
            p0 = cv2.goodFeaturesToTrack(old_gray, mask=feature_mask, **feature_params)
            tracking_request = False
            
            
  
            
            print("Pressed", tracking_request_point)

        if p0 is not None:
            
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
            # Select good points
            if p1 is not None:
                good_new = p1[st==1]
                good_old = p0[st==1]
                # draw the tracks
                for i, (new, old) in enumerate(zip(good_new, good_old)):
                    a, b = new.ravel()
                    c, d = old.ravel()
                    mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
                    frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
            img = cv2.add(frame, mask)
            p0 = good_new.reshape(-1, 1, 2)
        else:
            img = frame
        cv2.imshow(WINDOW_NAME, img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        

    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()