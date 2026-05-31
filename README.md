# People Entry Counter — Door Entrance Monitoring

This project is a computer vision pipeline designed to detect and count the number of people entering a building through a door, using a provided video dataset.

## 📦 Submitted Files
- `count-person.ipynb`: The main Jupyter Notebook containing the full tracking and counting pipeline.
- `roi_tuner.py`: An interactive GUI tool to help visualize and tune the ROI and counting line coordinates in real-time.
- `custom_botsort.yaml`: Custom configuration for the BoT-SORT tracker to handle occlusion near the door.
- `requirements.txt`: Python dependencies required to run the code.
- `IDEA_DESCRIPTION.md`: Document detailing the approach, reasoning, and limitations.
- `entrance_result.mp4`: The final processed video result showing the people counting in action.

## 🚀 Installation

1. Ensure you have Python 3.8+ installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ How to Run

### 1. Main Pipeline
Open and run all cells in `count-person.ipynb`. The notebook is structured step-by-step:
1. Configuration (Set video paths, thresholds, and line coordinates)
2. Core Logic (PeopleCounter class with YOLOv8 and tracking logic)
3. Run Pipeline (Generates the output video)

### 2. ROI & Line Tuner (Optional Utility)
If you are testing on a new video with a different camera angle, you can use the tuner script to visually set up the counting boundaries:
```bash
python roi_tuner.py
```
*Controls:* Use the on-screen sliders to adjust the line and ROI. Press `s` to save and print the coordinates, then `q` to quit.

## 🧠 Methodology & Idea Description
Please see the **[IDEA_DESCRIPTION.md](./IDEA_DESCRIPTION.md)** file for a detailed explanation of the tracking algorithms, direction classification logic, and system limitations.
