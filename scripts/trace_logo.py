import pathlib
import sys

import cv2
import numpy as np

UPSCALE = 6
BLUR_SIGMA = 3.2
SIMPLIFY_EPSILON = 0.16
VIEWBOX_PADDING = 4


def load_alpha_mask(source):
    image = cv2.imread(str(source), cv2.IMREAD_UNCHANGED)
    alpha = image[:, :, 3].astype(np.float32) / 255
    enlarged = cv2.resize(alpha, None, fx=UPSCALE, fy=UPSCALE, interpolation=cv2.INTER_CUBIC)
    smoothed = cv2.GaussianBlur(enlarged, (0, 0), BLUR_SIGMA)
    return (smoothed > 0.5).astype(np.uint8) * 255


def contour_to_path(contour, origin_x, origin_y):
    points = contour.reshape(-1, 2).astype(np.float32)
    commands = [
        f"{'M' if index == 0 else 'L'}{(x - origin_x) / UPSCALE:.2f} {(y - origin_y) / UPSCALE:.2f}"
        for index, (x, y) in enumerate(points)
    ]
    return "".join(commands) + "Z"


def trace(source, output):
    mask = load_alpha_mask(source)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    x, y, width, height = cv2.boundingRect(mask)
    origin_x = x - VIEWBOX_PADDING * UPSCALE
    origin_y = y - VIEWBOX_PADDING * UPSCALE
    simplified = [
        cv2.approxPolyDP(contour, SIMPLIFY_EPSILON * UPSCALE, True)
        for contour in contours
        if cv2.contourArea(contour) > 4 * UPSCALE * UPSCALE
    ]
    path = "".join(contour_to_path(contour, origin_x, origin_y) for contour in simplified)
    view_width = width / UPSCALE + 2 * VIEWBOX_PADDING
    view_height = height / UPSCALE + 2 * VIEWBOX_PADDING
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_width:.2f} {view_height:.2f}">'
        f'<path fill="currentColor" fill-rule="evenodd" d="{path}"/></svg>\n'
    )
    pathlib.Path(output).write_text(svg)
    print(f"{len(simplified)} contours, viewBox {view_width:.1f}x{view_height:.1f}, {len(svg)} bytes")


if __name__ == "__main__":
    trace(*sys.argv[1:3])
