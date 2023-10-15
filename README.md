## Setup

Create the Virtual Environment.
```
python-m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## VCC2023 Dataset

Include 2 datasets: both two female voices
vcc2023/vcc2023_training/VIVOSSPK01
vcc2023/vcc2023_training/VIVOSSPK42


## Data Preprocessing

To expedite training, we preprocess the dataset by converting waveforms to melspectograms:

For example:

```
python data_preprocessing/preprocess_vcc2023.py \
  --data_directory vcc2023/vcc2023_training \
  --preprocessed_data_directory vcc2023_preprocessed/vcc2023_training \
  --speaker_ids VIVOSSPK01 VIVOSSPK42
```

## Training

Train MaskCycleGAN-VC to convert between `<speaker_A_id>` and `<speaker_B_id>`. You should start to get excellent results after only several hundred epochs.
```
python -W ignore::UserWarning -m mask_cyclegan_vc.train \
    --name mask_cyclegan_vc_VIVOSSPK01_VIVOSSPK42 \
    --seed 0 \
    --save_dir results/ \
    --preprocessed_data_dir vcc2023_preprocessed/vcc2023_training/ \
    --speaker_A_id VIVOSSPK01 \
    --speaker_B_id VIVOSSPK42 \
    --epochs_per_save 100 \
    --epochs_per_plot 10 \
    --num_epochs 1800 \
    --batch_size 1 \
    --decay_after 1e4 \
    --sample_rate 22050 \
    --num_frames 64 \
    --max_mask_len 25 \
    --gpu_ids 0 \
    --continue_train \
```

## Testing

Test your trained MaskCycleGAN-VC by converting between `<speaker_A_id>` and `<speaker_B_id>` on the evaluation dataset. Your converted .wav files are stored in `results/<name>/converted_audio`.

```
python -W ignore::UserWarning -m mask_cyclegan_vc.test \
    --name mask_cyclegan_vc_VIVOSSPK01_VIVOSSPK42 \
    --save_dir results/ \
    --preprocessed_data_dir vcc2023_preprocessed/vcc2023_evaluation \
    --gpu_ids 0 \
    --speaker_A_id VIVOSSPK01 \
    --speaker_B_id VIVOSSPK42 \
    --ckpt_dir results/mask_cyclegan_vc_VIVOSSPK01_VIVOSSPK42/ckpts \
    --load_epoch 1800 \
    --model_name generator_A2B \
```

Toggle between A->B and B->A conversion by setting `--model_name` as either `generator_A2B` or `generator_B2A`.

Select the epoch to load your model from by setting `--load_epoch`.


## Acknowledgements
Source code clone from source https://github.com/GANtastic3/MaskCycleGAN-VC.git and modify to increase stable and exactly in training model
