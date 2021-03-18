# TODO:

- Get a list of all the sensors
  - Handle camera calibration data
- Collect all the sample_data into sample_data.json
- Collect all the annotations from samples/<MAIN_SENSOR_NAME>/anotations into sample_annotations.json

# Simplified

### The following is the format your data should be in:

```
universal-data-format
├── logs
├── samples
│   ├── LIDAR_TOP
│   │   ├── calibrated_sensor.json
│   │   ├── data
│   │   │   └── 1532402927647951.pcd
│   │   └── annotations
│   │       └── 1532402927647951.pcd.json
│   ├── CAMERA_FRONT // no annotations for the CAMERA
│   │   ├── calibrated_sensor.json
│   │   └── data
│   │       └── 1532402927647951.png
│   ├── CAMERA_LEFT
│   ├── CAMERA_RIGHT
│   ├── HYDROPHONE_FRONT
│   ├── HYDROPHONE_LEFT
│   ├── HYDROPHONE_REAR
│   └── HYDROPHONE_RIGHT
├── sweeps
│   ├── CAMERA_FRONT // no calibration for sweeps (it already exists for samples)
│   │   └── data
│   │      └── 1532402927647952.png
│   ├── CAMERA_LEFT
│   ├── CAMERA_RIGHT
│   ├── HYDROPHONE_FRONT
│   ├── HYDROPHONE_LEFT
│   ├── HYDROPHONE_REAR
│   ├── HYDROPHONE_RIGHT
│   └── LIDAR_TOP
├── category.json
└── ego_pose.json
```

#### Notes:

- `calibrated_sensor.json` only needs to exist for `CAMERA_*` folders inside the samples directory
- there is only an `annotations` folder for LIDAR_TOP. Nothing else should have annotations.

### The following is the format of the output data:

```
universal-data-format
├── logs
├── samples
│   ├── CAMERA_FRONT
│   │   └── frame0108.jpg
│   ├── CAMERA_LEFT
│   ├── CAMERA_RIGHT
│   ├── HYDROPHONE_FRONT
│   ├── HYDROPHONE_LEFT
│   ├── HYDROPHONE_REAR
│   ├── HYDROPHONE_RIGHT
│   └── LIDAR_TOP
├── sweeps
│   ├── CAMERA_FRONT
│   │   └── frame0109.jpg
│   ├── CAMERA_LEFT
│   ├── CAMERA_RIGHT
│   ├── HYDROPHONE_FRONT
│   ├── HYDROPHONE_LEFT
│   ├── HYDROPHONE_REAR
│   ├── HYDROPHONE_RIGHT
│   └── LIDAR_TOP
└── universal-data-format
    ├── calibrated_sensor.json
    ├── category.json
    ├── ego_pose.json
    ├── instance.json
    ├── log.json
    ├── sample.json
    ├── sample_annotation.json
    ├── sample_data.json
    ├── scene.json
    └── sensor.json
```

#### `instance.json`

Each instance is a single object in the real world tracked over a single scene.
For example, one buoy would be a single object.

```json
[
  {
    "token": "6dd2cbf4c24b4caeb625035869bca7b5",
    "category_token": "1fa93b757fc74fb197cdd60001ad8abf",
    "nbr_annotations": 39,
    "first_annotation_token": "ef63a697930c4b20a6b9791f423351da",
    "last_annotation_token": "8bb63134d48840aaa2993f490855ff0d"
  }
]
```

#### `sample.json`

A sample is a single snapshot of the world. It will include all the sensor data for this brief moment.

```json
[
  {
    "token": "ca9a282c9e77460f8360f564131a8af5", // identifies a single timestep
    "timestamp": 1532402927647951, // timestamp (ROS header timestamp)
    "prev": "",
    "next": "39586f9d59004284a7114a68825e8eec",
    "scene_token": "cc8c0bf57f984915a77078b10eb33198"
  }
]
```

#### `sample_data.json`

Sample data is a list of all the data files that exist (both sweeps and keyframes).

```json
[
  {
    "token": "5ace90b379af485b9dcb1584b01e7212",
    "sample_token": "39586f9d59004284a7114a68825e8eec",
    "ego_pose_token": "5ace90b379af485b9dcb1584b01e7212",
    "calibrated_sensor_token": "f4d2a6c281f34a7eb8bb033d82321f79",
    "timestamp": 1532402927814384,
    "fileformat": "pcd",
    "is_key_frame": false,
    "height": 0,
    "width": 0,
    "filename": "sweeps/RADAR_FRONT/n015-2018-07-24-11-22-45+0800__RADAR_FRONT__1532402927814384.pcd",
    "prev": "f0b8593e08594a3eb1152c138b312813",
    "next": "978db2bcdf584b799c13594a348576d2"
  },
  {
    "token": "512015c209c1490f906982c3b182c2a8",
    "sample_token": "39586f9d59004284a7114a68825e8eec",
    "ego_pose_token": "512015c209c1490f906982c3b182c2a8",
    "calibrated_sensor_token": "1d31c729b073425e8e0202c5c6e66ee1",
    "timestamp": 1532402927762460,
    "fileformat": "jpg",
    "is_key_frame": false,
    "height": 900,
    "width": 1600,
    "filename": "sweeps/CAM_FRONT/n015-2018-07-24-11-22-45+0800__CAM_FRONT__1532402927762460.jpg",
    "prev": "68e8e98cf7b0487baa139df808641db7",
    "next": "e9df123af5b747adbd9ddf6454e1abdc"
  }
]
```

Note that in the NuScenes dataset, each sensor has its own ego_pose_token because the sensors
aren't perfectly in sync (each camera takes a picture when the center of the LIDAR scan lines up with its FOV).

To simplify things, we could just assign an ego_pose_token closest to the sample timestamp and use this.

You can just use the ego pose timestamp that matched up with this sample data the closest.

#### `sample_annotation.json`

A sample annotation is a single annotation for a sample.
For NuScenes, this annotation is with respect to the ego of the vehicle,
so there is only one annotation per instance per sample.

In English, this means that one buoy will only have a single annotation per-timestamp
even if it appears in multiple sample data files.

```json
[
  {
    "token": "70aecbe9b64f4722ab3c230391a3beb8", // identifies the annotation
    "sample_token": "cd21dbfc3bd749c7b10a5c42562e0c42", // contains info about sensor, file, timestamp
    "instance_token": "6dd2cbf4c24b4caeb625035869bca7b5", // identifies a real-world object
    "visibility_token": "4", // how visible real-world object is
    "attribute_tokens": [
      "4d8821270b4a47e3a8a300cbec48188e" // any special attributes (ex. bouncing buoy, shaking buoy, etc)
    ],
    "translation": [
      // 3D translation
      373.214,
      1130.48,
      1.25
    ],
    "size": [
      // 3D size
      0.621,
      0.669,
      1.642
    ],
    "rotation": [
      // 3D rotation
      0.9831098797903927,
      0.0,
      0.0,
      -0.18301629506281616
    ],
    "prev": "a1721876c0944cdd92ebc3c75d55d693", // the prev annotation of the instance with this sensor modality
    "next": "1e8e35d365a441a18dd5503a0ee1c208", // the next annotation of the instance with this sensor modality
    "num_lidar_pts": 5,
    "num_radar_pts": 0
  }
]
```

# Full NuScenes

The following is the format your data should be in:

```
universal-data-format
├── logs
├── maps
├── samples
│   ├── CAMERA_FRONT
│   │   ├── calibrated_sensor.json
│   │   ├── data
│   │   │   └── frame0108.jpg
│   │   └── annotations
│   │       └── frame0108.jpg.json
│   ├── CAMERA_LEFT
│   ├── CAMERA_RIGHT
│   ├── HYDROPHONE_FRONT
│   ├── HYDROPHONE_LEFT
│   ├── HYDROPHONE_REAR
│   ├── HYDROPHONE_RIGHT
│   └── LIDAR_TOP
├── sweeps
│   ├── CAMERA_FRONT
│   ├── CAMERA_LEFT
│   ├── CAMERA_RIGHT
│   ├── HYDROPHONE_FRONT
│   ├── HYDROPHONE_LEFT
│   ├── HYDROPHONE_REAR
│   ├── HYDROPHONE_RIGHT
│   └── LIDAR_TOP
└── universal-data-format
    ├── attribute.json
    ├── category.json
    ├── ego_pose.json
    ├── instance.json
    └── visibility.json
```

The following is the format of the output data:

```
universal-data-format
├── logs
├── maps
├── samples
│   ├── CAMERA_FRONT
│   │   └── frame0108.jpg
│   ├── CAMERA_LEFT
│   ├── CAMERA_RIGHT
│   ├── HYDROPHONE_FRONT
│   ├── HYDROPHONE_LEFT
│   ├── HYDROPHONE_REAR
│   ├── HYDROPHONE_RIGHT
│   └── LIDAR_TOP
├── sweeps
│   ├── CAMERA_FRONT
│   ├── CAMERA_LEFT
│   ├── CAMERA_RIGHT
│   ├── HYDROPHONE_FRONT
│   ├── HYDROPHONE_LEFT
│   ├── HYDROPHONE_REAR
│   ├── HYDROPHONE_RIGHT
│   └── LIDAR_TOP
└── universal-data-format
    ├── attribute.json
    ├── calibrated_sensor.json
    ├── category.json
    ├── ego_pose.json
    ├── instance.json
    ├── log.json
    ├── map.json
    ├── sample.json
    ├── sample_annotation.json
    ├── sample_data.json
    ├── scene.json
    ├── sensor.json
    └── visibility.json
```
