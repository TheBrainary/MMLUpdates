
#-----------------------------START CAPTURE_IMAGE---------------------------------
timestr = time.strftime("%d-%m-%Y_%H-%M-%S.png")

msg_image = rospy.wait_for_message('/miro/sensors/camr/compressed', CompressedImage, timeout=7)
np_arr = np.frombuffer(msg_image.data, np.uint8)
image_np = cv2.imdecode(np_arr, 1)

rospack = rospkg.RosPack()
images_path = '/home/cqr/lib/mei/blockly_ws/install_isolated/share/robot_blockly/frontend/pages/images/'
cv2.imwrite(images_path+ 'image_' + timestr, image_np)

files = len(os.listdir(images_path)) #amount of files in /frontend/images/ folder

if files > 7 : #allow 5 images max
    os.system("find "+images_path+" -name '*.png' | xargs ls -t | tail -n 1 | xargs rm")#remove oldest image
#-----------------------------END CAPTURE_IMAGE---------------------------------
