
#-----------------------------START FIND_CIRCLE---------------------------------
# Extract circles
# YCrCb YUV HSV GRAY LAB LUV HLS
output = data.copy()
methods = [cv2.COLOR_RGB2YCrCb, cv2.COLOR_RGB2YUV, cv2.COLOR_RGB2HSV, 
           cv2.COLOR_RGB2GRAY, cv2.COLOR_RGB2LAB, cv2.COLOR_RGB2LUV, cv2.COLOR_RGB2HLS]

dp = 3 #accumulator
minDist = 1 # minimum distance between circles
param1 = 100
param2 = 50
minRad = 5
maxRad = 0
num_iters = 0

circles = []
for m in methods:
    use = cv2.cvtColor(data, m)

    if len(use.shape) == 2:
        use = use[:,:,None]

    for dim in range(use.shape[2]):
        num_iters += 1
        circs = cv2.HoughCircles(use[:,:, dim] ,cv2.HOUGH_GRADIENT, dp, minDist,
                                 param1=param1,param2=param2,minRadius=minRad,maxRadius=maxRad)
        if circs is not None:
            circles.append(np.round(circs[0]).astype("int"))

lin = None
if len(circles) > 0:
    for p in circles:
        if lin is None:
            lin = p
        else:
            lin = np.vstack([lin, p])

    threshx = 5
    threshy = 5

    for a in range(lin.shape[0]):
        for b in range(lin.shape[0]):
            if abs(lin[b][0] - lin[a][0]) < threshx and abs(lin[b][1] - lin[a][1]) < threshy:
                lin[b] = lin[a]

    unique, counts = np.unique(lin[:,:3], axis=0, return_counts=True)
    unique_counts = np.hstack([unique, counts[:, None]])

    count_thresh = np.percentile(counts, 90)
    if count_thresh > num_iters*0.5:
        result = True
    else:
        result = False
    
    # ensure at least some circles were found
    mask_list = []
    if unique_counts.shape[0] > 0:
        # loop over the (x, y) coordinates and radius of the circles
        for x,y,r,c in unique_counts:
            if c > count_thresh:
                # draw the circle in the output image
                this_mask = np.full(output.shape[:2], 0, dtype=np.uint8)
                cv2.circle(this_mask, (x, y), r, (255, 255, 255), -1)
                mask_list.append(this_mask)

    res = np.full(output.shape[:2], 0, dtype=np.uint8)
    if len(mask_list) > 0:
        # show the output image
        for m in mask_list:
            res = cv2.bitwise_or(res, m)
        output = cv2.bitwise_and(output,output,mask = res)
else:
    result = False

#-----------------------------END FIND_CIRCLE---------------------------------
