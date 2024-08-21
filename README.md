# Video Frame Interpolation of Hydra Regeneration

![Hydra Regeneration in the Lab](./doc/process.png)

## Authors

Barak Aharoni & Itay Erlich

## Table of Contents

1. [Introduction](#introduction)
   - [Hydra Regeneration](#hydra-regeneration)
   - [Video Frame Interpolation](#video-frame-interpolation)
2. [Method](#method)
   - [Model](#model)
   - [Fine Tuning the Model for Hydra Regeneration](#fine-tuning-the-model-for-hydra-regeneration)
   - [Dataset](#dataset)
   - [Preprocessing](#preprocessing)
3. [Training](#training)
   - [Infrastructure](#infrastructure)
   - [Training the Autoencoder](#training-the-autoencoder)
   - [Training the Consecutive Brownian Bridge Diffusion Module](#training-the-consecutive-brownian-bridge-diffusion-module)
4. [Results](#results)
5. [Command-Line Usage](#command-line-usage)
6. [Ethics Statement](#ethics-statement)
7. [Links](#links)

## Introduction

### Hydra Regeneration

In Kinneret Keren's lab at the Technion Physics Department, morphogenesis is studied using Hydra for its simple structure and regeneration ability. The Hydra is a small, freshwater organism from the phylum Cnidaria. The process involves:

1. Cutting a part of the Hydra.
2. The part becoming a ball.
3. The ball regenerates into a fully functional Hydra.

![Hydra Regeneration Process](./doc/hydra_regen.png)

### Video Frame Interpolation

Video frame interpolation generates intermediate frames between consecutive frames in a video, useful for higher frame rates, slow motion, and video stabilization. The project aims to improve observation and analysis of Hydra regeneration.

## Method

### Model

We used the Frame Interpolation with Consecutive Brownian Bridge Diffusion model, which introduces a novel technique to improve video frame interpolation by reducing randomness. This approach is suitable for capturing the detailed changes in Hydra regeneration.

![Model Architecture](./doc/overview.jpg)

### Fine Tuning the Model for Hydra Regeneration

We fine-tuned a pre-trained model on Hydra regeneration videos, using additional augmentations like rotation due to the unique characteristics of these videos.

### Dataset
The dataset consists of various Hydra regeneration videos recorded in the lab, systematically collected for fine-tuning.
To make use of the Hydra_triplets dataset defined in [bvi_vimeo.py](./LDMVFI/ldm/data/bvi_vimeo.py), the dataset is expected to be in the following structure:
```
└──── <hydra data directory>/
    └──── video_name_1/
        ├──── frame_name_1.tiff
        ├──── frame_name_2.tiff
        ...
    ├──── video_name_2/
        ├──── frame_name_1.tiff
        ├──── frame_name_2.tiff
        ...
    ...
    ├──── tri_testlist.txt
    ├──── tri_trainlist.txt
    └──── tri_vallist.txt
```
where ```tri_{test, train, val}list.txt``` is a text file containing a triplets of consecutive frames.

#### Dataset Creation
To create the Dataset in a relative ratio of test/train/val triplets from each video given the hydra data directory structure above, run the following command:
```
python ./hydra_create_dataset.py db_dirpath
```
where ```db_dirpath``` is the path to the hydra videos db in your server. 
if you want to create a small dataset from a hydra data directory in the above structure, run:
```
python ./hydra_create_dataset.py db_dirpath
```
We found it useful to use a small dataset to experiment and see reasonable results before running on the entire dataset.

## Model Usage
### Setup & Infrastructure
Training was performed on a DGX A100 Server with 8 A100 GPUs, using CUDA and PyTorch for accelerated processing.
running on the DGX Server is avaiable only in a container. To enable the model to run on the DGX server, we created a docker containing all of the dependencies 
needed for both submodules (LDMVFI, ConsecutiveBrownianBridge). the docker is available here: [link](https://hub.docker.com/layers/itayerlich/dl_project_docker/3/images/sha256-77732e57ecb1090670e15a8f21ee456532f18d155b66ba1b5971d04ccd4fe0a2?context=repo). 
However, if you want to run the model on another enviroment, you may use the following command to setup all of the neccessary requirements for the project:
```
pip install -r ./requirements.txt 
```

### Training LBBDM (Consecutive Brownian Bridge Diffusion Module)

To train the LBBDM model, use the following command (running from ConsecutiveBrownianBridge folder):
```
nohup python ./main.py --config ./configs/Template-LBBDM-video-hydra.yaml --train --save_top --gpu_ids 0,1 -r ./results_LBBDM > LBBDM_train_output.log 2>&1 &
```

#### Evaluating LBBDM
For model evaluation, use the following command:
```
python ./ConsecutiveBrownianBridge/main.py --config ./ConsecutiveBrownianBridge/configs/Template-LBBDM-video.yaml --gpu_ids 0 -r ./results_LBBDM --resume_model path/to/model.pth --sample_to_eval
```

### Training LDMVFI AutoEncoder
To train the LDMVFI AutoEncoder, use the following command (running from LDMVFI folder):
```
nohup python main.py --base ./configs/autoencoder/vqflow-f32-hydra.yaml -r "path/to/model/checkpoint" -t --gpus 0,1,2 > LDMVFI_train_output.log 2>&1 &
```
### Two Frame Interpolation
To interpolate frames only between two given frames using the trained model, use the following command:

```
python ./ConsecutiveBrownianBridge/interpolate.py --resume_model "/path/to/model/checkpoint" --frame0 "/path/to/frame0" --frame1 "/path/to/frame1" -r "/path/to/output" --xN <frame_rate_multiply_factor> --config ./ConsecutiveBrownianBridge/configs/Template-LBBDM-video.yaml --gpu_ids 0
```

### Entire Video Frame Interpolation
To interpolate an entire Hydra video, or a portion of the video (say frames 400-500), use the following command:
```
python ./interpolate_whole_video.py --resume_model "/path/to/model/checkpoint" --folder path/to/hydra/video/folder --frame_start 400 --frame_end  500 -r "path/to/result/folder"  --config ./configs/Template-LBBDM-video-hydra.yaml --gpu_ids 0
```
To interpolate an entire video just remove --frame_start and --frame_end argument. [interpolate_whole_video.py](./ConsecutiveBrownianBridge/interpolate_whole_video.py) currently multiplies framerate by 8 without other frame rates multiply factors available as in [interpolate.py](./ConsecutiveBrownianBridge/interpolate.py)


## Result Video - Comparison between original frames and our Frame Interpolation
![Demo gif](./doc/Hydra_comparison_gif.gif)

## Ethics Statement
While the project has great potential, it is crucial to acknowledge that generated frames cannot replace real data. Users must be aware of this limitation to prevent misleading outcomes.

## Links
Presentation Video: [link]