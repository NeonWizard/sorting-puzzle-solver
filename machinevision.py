import cv2
import numpy as np

# cv2.namedWindow("main")
# cv2.namedWindow("extra")

frame = cv2.imread("screenshots/screenshot1.png")

output = frame.copy()
image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray_blurred = cv2.blur(gray, (3, 3))

# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(
    gray_blurred,
    cv2.HOUGH_GRADIENT,
    1,
    20,
    param1=50,
    param2=60,
    minRadius=20,
    maxRadius=60,
)

potential_bubbles = []  # (color, position, radius)

# Draw circles that are detected.
if detected_circles is not None:
    if len(detected_circles) > 80:
        print("WARNING: More than 80 circles were detected, truncating.")
        detected_cicles = detected_circles[:80]  # cap at 80 detections

    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0, :]:
        a, b, r = int(pt[0]), int(pt[1]), int(pt[2])

        # Draw the circumference of the circle.
        cv2.circle(output, (a, b), r, (0, 255, 0), 2)
        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(output, (a, b), 1, (0, 0, 255), 3)
        # Draw a tag
        tag_loc = (round(a+r*1.7), round(b-r*0.8))
        cv2.line(
            output,
            (a, b),
            tag_loc,
            (255, 0, 0),
            2,
        )
        # cv2.putText(
        #     output,
        #     "#1",
        #     (tag_loc[0] + 10, tag_loc[1]+5),
        #     0,
        #     1.3,
        #     (0, 0, 0),
        #     2,
        # )

        # cut out interior of circle
        height, width, _ = frame.shape
        mask = np.zeros((height, width), np.uint8)

        # draw on mask
        cv2.circle(mask, (a, b), r, (255, 255, 255), thickness=-1)

        # copy image using mask
        masked_data = cv2.bitwise_and(frame, frame, mask=mask)

        # apply threshold
        _, thresh = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

        # find contours
        contours = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        x, y, w, h = cv2.boundingRect(contours[0])

        w4 = round(w/4)
        h4 = round(h/4)
        crop = masked_data[y+h4:y+h-h4, x+w4:x+w-w4]
        # swag = round(len(masked_data)/2)
        # sweg = round(swag / 4)
        # crop = masked_data[swag-sweg:swag+sweg, swag-sweg:swag+sweg]

        # ensure relatively uniform color distribution in circle
        average = [0, 0, 0]
        average_count = 0
        average_switch = 0
        for pixel in crop:
            for thing in pixel:
                average_switch = (average_switch + 1) % 4
                if average_switch == 0:
                    average[0] += thing[0]
                    average[1] += thing[1]
                    average[2] += thing[2]
                    average_count += 1

        if (average_count == 0):
            continue
        average[0] /= average_count
        average[1] /= average_count
        average[2] /= average_count
        cv2.circle(
            output,
            tag_loc,
            round(r/2.2),
            average,
            -1
        )
        # print(f"Circle finished: {average}")

        # save average color and circle info to list
        potential_bubbles.append(
            {
                "color": average,
                "radius": r,
                "position": (a, b)
            }
        )


potential_bubbles2 = []

for pbub in potential_bubbles:
    # filter out bubbles that don't have 3 in close y-axis proximity
    closest_x_axis = list(
        filter(
            lambda x: abs(x["position"][0]-pbub["position"][0]) < 20,
            potential_bubbles
        ),
    )

    # closest_x_axis_better = sorted(potential_bubbles, key=lambda x: abs(
    #     x["position"][0] - pbub["position"][0]), reverse=False)
    # print()
    # print()
    # print("TARGET:")
    # print(pbub)
    # print("5 closest:")
    # bleh = closest_x_axis_better[:5]
    # print("\n".join([str(x) for x in bleh]))
    # temp_output = frame.copy()
    # cv2.circle(temp_output, pbub["position"], 10, (0, 0, 0), -1)
    # for x in bleh:
    #     cv2.circle(temp_output, x["position"], 5, (0, 255, 255), -1)
    # cv2.imwrite("tmp.png", temp_output)
    # input()

    closest_y_axis = list(filter(
        lambda x: abs(x["position"][1]-pbub["position"][1]) < 200, closest_x_axis))

    swag = (pbub["position"][0]-100, pbub["position"][1])
    cv2.line(output, pbub["position"], swag, (0, 0, 0), 2)
    if len(closest_x_axis) >= 4:
        potential_bubbles2.append(pbub)
        cv2.circle(output, swag, pbub["radius"]//3, (0, 255, 0), -1)
    else:
        cv2.putText(output, str(len(closest_x_axis)), swag, 0, 2, (0, 0, 0), 2)
        cv2.circle(output, swag, pbub["radius"]//3, (0, 0, 255), -1)

for pbub in sorted(potential_bubbles2, key=lambda x: x["radius"]):
    # filter every bubble that has 3 other bubbles with similar average color
    closest_bubbles = sorted(potential_bubbles2,
                             key=lambda x:
                             abs(x["color"][0] - pbub["color"][0])
                             + abs(x["color"][1] - pbub["color"][1])
                             + abs(x["color"][2] - pbub["color"][2]),
                             reverse=True)

    # print("Bubble:")
    # print(pbub["color"])
    # print()
    # print("4 closest:")
    # print(closest_bubbles[1])
    # print(closest_bubbles[2])
    # print(closest_bubbles[3])
    # print(closest_bubbles[4])
    # input()
    for i in range(1):
        cv2.line(output, pbub["position"],
                 closest_bubbles[i+1]["position"], pbub["color"], 2)

# cv2.imshow("main", output)
cv2.imwrite("output.png", output)

# -- state validation
# TODO:
# contour match vials to know how many bubbles we should be looking for
# make sure each bubble is in a vertical group of 3 other bubbles (weed out false flags)
# check for all circles with uniform color inside
# make sure there are four of each color
