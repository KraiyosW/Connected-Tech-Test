"""
ROI & Counting Line Tuner — Real-time Interactive Tool
=======================================================
Use trackbars (sliders) to adjust:
  - Counting Line position (X, Y_start, Y_end)
  - ROI boundaries (X_min, X_max, Y_min, Y_max)

Controls:
  - Sliders: Drag to adjust values in real-time
  - 'n' / Right Arrow: Next frame (+30 frames)
  - 'p' / Left Arrow:  Previous frame (-30 frames)
  - 'space': Play/pause video
  - 's': Save current config and print to console
  - 'q' / ESC: Quit

The final config will be printed to the console for copy-paste into the notebook.
"""

import cv2
import numpy as np
import sys

# =====================================================================
# CONFIG
# =====================================================================
VIDEO_PATH = "entrance.mov"
WINDOW_NAME = "ROI & Line Tuner"
DISPLAY_WIDTH = 1280  # Resize for display (original is 1920x1080)

# Initial values (current defaults)
INIT_LINE_X = 620
INIT_LINE_Y_START = 150
INIT_LINE_Y_END = 750
INIT_ROI_X_MIN = 250
INIT_ROI_X_MAX = 1000
INIT_ROI_Y_MIN = 100
INIT_ROI_Y_MAX = 900


def nothing(x):
    """Trackbar callback (required by OpenCV)."""
    pass


def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"Error: Cannot open video '{VIDEO_PATH}'")
        sys.exit(1)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale = DISPLAY_WIDTH / orig_w
    display_h = int(orig_h * scale)

    print(f"Video: {orig_w}x{orig_h} @ {fps:.1f} FPS, {total_frames} frames")
    print(f"Display: {DISPLAY_WIDTH}x{display_h} (scale: {scale:.2f})")
    print()
    print("Controls:")
    print("  Sliders  — Adjust ROI & counting line in real-time")
    print("  n / →    — Next frame (+30)")
    print("  p / ←    — Previous frame (-30)")
    print("  Space    — Play/pause video")
    print("  s        — Save & print current config")
    print("  q / ESC  — Quit")
    print()

    # Create window
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)

    # Create trackbars (values in ORIGINAL pixel coordinates)
    cv2.createTrackbar("Line X",      WINDOW_NAME, INIT_LINE_X,       orig_w, nothing)
    cv2.createTrackbar("Line Y Top",  WINDOW_NAME, INIT_LINE_Y_START, orig_h, nothing)
    cv2.createTrackbar("Line Y Bot",  WINDOW_NAME, INIT_LINE_Y_END,   orig_h, nothing)
    cv2.createTrackbar("ROI X Min",   WINDOW_NAME, INIT_ROI_X_MIN,    orig_w, nothing)
    cv2.createTrackbar("ROI X Max",   WINDOW_NAME, INIT_ROI_X_MAX,    orig_w, nothing)
    cv2.createTrackbar("ROI Y Min",   WINDOW_NAME, INIT_ROI_Y_MIN,    orig_h, nothing)
    cv2.createTrackbar("ROI Y Max",   WINDOW_NAME, INIT_ROI_Y_MAX,    orig_h, nothing)
    cv2.createTrackbar("Frame",       WINDOW_NAME, 0,                 total_frames - 1, nothing)

    playing = False
    current_frame_idx = 0

    while True:
        # Read trackbar values
        line_x     = cv2.getTrackbarPos("Line X",     WINDOW_NAME)
        line_y_top = cv2.getTrackbarPos("Line Y Top", WINDOW_NAME)
        line_y_bot = cv2.getTrackbarPos("Line Y Bot", WINDOW_NAME)
        roi_x_min  = cv2.getTrackbarPos("ROI X Min",  WINDOW_NAME)
        roi_x_max  = cv2.getTrackbarPos("ROI X Max",  WINDOW_NAME)
        roi_y_min  = cv2.getTrackbarPos("ROI Y Min",  WINDOW_NAME)
        roi_y_max  = cv2.getTrackbarPos("ROI Y Max",  WINDOW_NAME)
        slider_frame = cv2.getTrackbarPos("Frame",    WINDOW_NAME)

        # Handle frame navigation
        if playing:
            current_frame_idx += 1
            if current_frame_idx >= total_frames:
                current_frame_idx = 0
            cv2.setTrackbarPos("Frame", WINDOW_NAME, current_frame_idx)
        elif slider_frame != current_frame_idx:
            current_frame_idx = slider_frame

        # Read frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_idx)
        ret, frame = cap.read()
        if not ret:
            current_frame_idx = 0
            continue

        # --- Draw ROI (green rectangle with semi-transparent fill outside) ---
        overlay = frame.copy()
        # Dim area outside ROI
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        mask[roi_y_min:roi_y_max, roi_x_min:roi_x_max] = 255
        dimmed = frame.copy()
        dimmed[mask == 0] = (dimmed[mask == 0] * 0.4).astype(np.uint8)
        frame = dimmed

        # ROI border
        cv2.rectangle(frame, (roi_x_min, roi_y_min), (roi_x_max, roi_y_max),
                      (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "ROI", (roi_x_min + 8, roi_y_min + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # --- Draw Counting Line (yellow) ---
        cv2.line(frame, (line_x, line_y_top), (line_x, line_y_bot),
                 (0, 255, 255), 3, cv2.LINE_AA)

        # Direction labels
        cv2.putText(frame, "INSIDE", (line_x - 140, line_y_top - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        cv2.putText(frame, "OUTSIDE", (line_x + 15, line_y_top - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        # --- Info panel ---
        panel_h = 70
        cv2.rectangle(frame, (0, orig_h - panel_h), (orig_w, orig_h), (0, 0, 0), -1)
        timestamp = current_frame_idx / fps
        info1 = (f"Frame: {current_frame_idx}/{total_frames}  |  "
                 f"Time: {timestamp:.1f}s  |  "
                 f"{'PLAYING' if playing else 'PAUSED'}")
        info2 = (f"Line: x={line_x}, y=[{line_y_top},{line_y_bot}]  |  "
                 f"ROI: x=[{roi_x_min},{roi_x_max}], y=[{roi_y_min},{roi_y_max}]")
        cv2.putText(frame, info1, (15, orig_h - panel_h + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        cv2.putText(frame, info2, (15, orig_h - panel_h + 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

        # Resize for display
        display = cv2.resize(frame, (DISPLAY_WIDTH, display_h))

        # Show
        cv2.imshow(WINDOW_NAME, display)

        # --- Key handling ---
        key = cv2.waitKey(30 if playing else 0) & 0xFF

        if key == ord('q') or key == 27:  # q or ESC
            break
        elif key == ord('s'):
            # Save / print config
            config = f"""
# ========================================
# SAVED CONFIGURATION
# ========================================
LINE_X = {line_x}
LINE_Y_START = {line_y_top}
LINE_Y_END = {line_y_bot}

ROI_X_MIN = {roi_x_min}
ROI_X_MAX = {roi_x_max}
ROI_Y_MIN = {roi_y_min}
ROI_Y_MAX = {roi_y_max}
# ========================================
"""
            print(config)
        elif key == ord('n') or key == 83:  # n or Right arrow
            current_frame_idx = min(current_frame_idx + 30, total_frames - 1)
            cv2.setTrackbarPos("Frame", WINDOW_NAME, current_frame_idx)
        elif key == ord('p') or key == 81:  # p or Left arrow
            current_frame_idx = max(current_frame_idx - 30, 0)
            cv2.setTrackbarPos("Frame", WINDOW_NAME, current_frame_idx)
        elif key == ord(' '):  # Space = play/pause
            playing = not playing
        elif key == 255 or key == -1:
            # No key pressed (waitKey timeout in play mode)
            pass

    # Final config print
    print("\n" + "=" * 50)
    print("FINAL CONFIG (copy to notebook Cell 2):")
    print("=" * 50)
    print(f"LINE_X = {line_x}")
    print(f"LINE_Y_START = {line_y_top}")
    print(f"LINE_Y_END = {line_y_bot}")
    print(f"ROI_X_MIN = {roi_x_min}")
    print(f"ROI_X_MAX = {roi_x_max}")
    print(f"ROI_Y_MIN = {roi_y_min}")
    print(f"ROI_Y_MAX = {roi_y_max}")
    print("=" * 50)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
