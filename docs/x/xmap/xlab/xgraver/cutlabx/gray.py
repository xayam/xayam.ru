import cv2
import numpy as np

from png2nc import heightA4, widthA4, boundX, boundY, line_pixels

def get_gray_trajectory(filename):
    gray_image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    # _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
    # binary_image = 255 - binary_image

    trajectory = []
    last_point = np.array([0, 0])
    for cluster in ordered_clusters:
        pixels = cluster['pixels']  # (N, 2) — [y, x]
        chunks =  [
            pixels[i:i + max_cluster_size]
            for i in range(0, len(pixels), max_cluster_size)]
        for chunk in chunks:
            result, last_point = algorithm(chunk, last_point)
            trajectory.append(result)
            trajectory.append(result)
    return image.shape[1], image.shape[0], binary_image, trajectory
    return 1, 2, 3, [[4]]

def gray_optimize(filename: str, speed: str, power: str) -> str:
    width, height, binary_image, trajectory = \
        get_gray_trajectory(filename=filename)
    image = np.ones_like(binary_image) * 255
    result = ""
    for i in range(len(trajectory)):
        print(f"{i + 1}/{len(trajectory)}")
        cluster = trajectory[i]
        y_pred = None
        for j in range(1, len(cluster)):
            flag = False
            ys1, xs1 = cluster[j - 1]
            ys2, xs2 = cluster[j]
            y1 = round(heightA4 - ys1 / height * heightA4 + boundY, 2)
            x1 = round(xs1 / width * widthA4 + boundX, 2)
            if j == 1:
                result += f"G0X{x1}Y{y1}{speed}\n"
                y_pred = y1
            y2 = round(heightA4 - ys2 / height * heightA4 + boundY, 2)
            x2 = round(xs2 / width * widthA4 + boundX, 2)
            points = line_pixels(ys1, xs1, ys2, xs2)
            for yy, xx in points:
                if binary_image[yy, xx] == 0:
                    flag = True
                    break
            if flag:
                result += f"G0X{x2}Y{y2}\n"
                y_pred = y2
            else:
                s1 = f"G0X{x1}"
                if y1 != y_pred:
                    s1 += f"Y{y1}"
                    y_pred = y1
                s1 += "\n"
                if x1 != x2:
                    result += s1
                result += f"G1X{x2}"
                result += "\n"
                image = cv2.line(image, (xs1, ys1), (xs2, ys2),
                                     color=(0, 0, 0), thickness=1)
    cv2.imwrite(filename[:-3] + "nc.png", image)
    return result

def gray_algorithm(filename, speed, power):
    return gray_optimize(filename=filename, speed=speed, power=power)
