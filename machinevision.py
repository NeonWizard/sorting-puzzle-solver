import cv2
import numpy as np

import utils


def get_vials(filename, write_image=False):
    frame = cv2.imread(filename)
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

            # ensure relatively uniform color distribution in circle
            average = [0, 0, 0]
            average_count = 0
            average_switch = 0
            for pixel in crop:
                for thing in pixel:
                    average_switch = (average_switch + 1) % 4
                    if average_switch == 0:
                        average[0] += int(thing[0])
                        average[1] += int(thing[1])
                        average[2] += int(thing[2])
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
        swag = (pbub["position"][0]-83, pbub["position"][1])
        cv2.line(output, pbub["position"], swag, (0, 0, 0), 2)
        cv2.circle(output, swag, 13, (0, 0, 255), -1)

        # filter out bubbles that don't have 3 in close y-axis proximity
        closest_x_axis = list(
            filter(
                lambda x: abs(x["position"][0]-pbub["position"][0]) < 20,
                potential_bubbles
            ),
        )
        closest_y_axis = sorted(
            list(
                filter(lambda x: abs(x["position"][1] -
                                     pbub["position"][1]) < 300, closest_x_axis)
            ),
            key=lambda x: abs(x["position"][1]-pbub["position"][1]),
        )

        if len(closest_y_axis) >= 4:
            pbub["buddies"] = closest_y_axis[1:4]
            potential_bubbles2.append(pbub)

    bubbles = []
    skip_is = set()
    for i, pbub in enumerate(potential_bubbles2):
        if i in skip_is:
            continue
        # filter every bubble that has 3 other bubbles with similar average color
        closest_bubbles = list(filter(lambda x:
                                      (abs(x["color"][0] - pbub["color"][0])
                                       + abs(x["color"][1] - pbub["color"][1])
                                       + abs(x["color"][2] - pbub["color"][2])) < 5,
                                      potential_bubbles2))[:4]

        if len(closest_bubbles) == 4:
            pbub["color_index"] = i
            for x in closest_bubbles[1:]:
                x["color_index"] = i
                skip_is.add(potential_bubbles2.index(x))
                bubbles.append(x)

            bubbles.append(pbub)
        else:
            cv2.circle(output, swag, pbub["radius"]//3, (0, 0, 255), -1)

    vials = []
    bubbles_visited = set()
    for i, pbub in enumerate(bubbles):
        swag = (pbub["position"][0]-83, pbub["position"][1])
        cv2.circle(output, swag, 13, (0, 255, 0), -1)

        if i in bubbles_visited:
            continue

        bubbles_visited.add(i)
        for buddy in pbub["buddies"]:
            bubbles_visited.add(bubbles.index(buddy))

        vial = {"bubbles": [pbub], "height": pbub["position"][1]}
        cv2.circle(output, pbub["position"], 10, (255, 0, 255), -1)
        for buddy in pbub["buddies"]:
            vial["bubbles"].append(buddy)
            vial["height"] += buddy["position"][1]
            cv2.line(output, pbub["position"], buddy["position"], (0, 0, 0), 2)

        vial["height"] /= 4
        vials.append(vial)

    # Sort vials into rows (by y-axis)
    vials = sorted(vials, key=lambda x: x["height"])
    vial_rows = utils.cluster(vials, 50, key=lambda x: x["height"])

    vials = []
    # Sort rows by x position and refill vials array in order
    for row in vial_rows:
        row.sort(key=lambda x: x["bubbles"][0]["position"][0])
        vials += row

    # Sort the contents of each vial
    for i, vial in enumerate(vials):
        # print(vial["bubbles"][0]["position"])
        cv2.putText(output, f"#{i}", vial["bubbles"]
                    [0]["position"], 0, 2, (0, 0, 0), 2)

        vial["bubbles"].sort(key=lambda x: x["position"][1])

    if write_image:
        cv2.imwrite("output.png", output)

    return vials


def simplify_vials(vials):
    out = []
    for vial in vials:
        out.append([bubble["color_index"] for bubble in vial["bubbles"]])
    return out


def main():
    vials = get_vials("screenshots/screenshot1.png", True)
    simple_vials = simplify_vials(vials)
    print(simple_vials)


if __name__ == "__main__":
    main()
