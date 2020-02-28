
#-----------------------------START GET_COLOUR_PIXELS---------------------------------
hex_str = hex_string.lstrip("#")
lv = len(hex_str)
colorRGB = tuple(int(hex_str[i:i+ lv // 3], 16) for i in range(0, lv, lv // 3))
colorHSV = np.full([1,1,3], colorRGB, dtype=np.uint8)
colorHSV = cv2.cvtColor(colorHSV, cv2.COLOR_RGB2HSV)[0,0]

image_l = rospy.wait_for_message('/miro/sensors/caml/compressed', CompressedImage, timeout=10)
image_r = rospy.wait_for_message('/miro/sensors/camr/compressed', CompressedImage, timeout=10)
data_l = np.frombuffer(image_l.data, np.uint8)
data_l = cv2.imdecode(data_l, 1)
h  = data_l.shape[1]
w  = data_l.shape[0]
data_l = np.reshape(data_l, (h, w, 3))

data_r = np.frombuffer(image_r.data, np.uint8)
data_r = cv2.imdecode(data_r, 1)
data_r = np.reshape(data_r, (h, w, 3))

frac = int(round(w/2))
data = np.hstack([data_l[:,-frac:,:], 
                  data_r[:,:frac,:]])

hsv_image = cv2.cvtColor(data, cv2.COLOR_RGB2HSV)

offset = 30
lower = np.array([colorHSV[0]-offset, 0, 0])
upper = np.array([colorHSV[0]+offset, 255, 255])

mask = cv2.inRange(hsv_image, lower, upper)

result_left = float(cv2.countNonZero(mask[:,:frac])) / mask.size
result_right = float(cv2.countNonZero(mask[:,-frac:])) / mask.size

result = result_left + result_right


#-----------------------------END GET_COLOUR_PIXELS---------------------------------
