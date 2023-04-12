import os
import numpy as np
import argparse
from tqdm import tqdm
parser = argparse.ArgumentParser(description='Easy video feature extractor')
parser.add_argument("-input_file_list", type=str, default='/data03/shichengshun-slurm/dataset/vggsound/scratch/shared/beegfs/hchen/train_data/VGGSound_final/video', help="Should be a csv file of a single columns, each row is the input video path.")
parser.add_argument("-target_fold", type=str, default='/data03/shichengshun-slurm/dataset/vggsound/scratch/shared/beegfs/hchen/train_data/VGGSound_final/audio_mono', help="The place to store the video frames.")
parser.add_argument("-target_fold2", type=str, default='/data03/shichengshun-slurm/dataset/vggsound/scratch/shared/beegfs/hchen/train_data/VGGSound_final/audio', help="The place to store the video frames.")
args = parser.parse_args()

# input_filelist = np.loadtxt(args.input_file_list, delimiter=',', dtype=str)
input_filelist = os.listdir(args.input_file_list) # list
if os.path.exists(args.target_fold) == False:
    os.makedirs(args.target_fold)

# first resample audio
for input_f in tqdm(input_filelist):
    input_f = os.path.join(args.input_file_list, input_f)
    ext_len = len(input_f.split('.')[-1])
    video_id = input_f.split('/')[-1][:-ext_len-1]
    output_f_1 = args.target_fold + '/' + video_id + '_intermediate.wav'
    os.system('ffmpeg -hide_banner -loglevel error -y -i {:s} -vn -ac 1 -ar 16000 {:s}'.format(input_f, output_f_1)) # save an intermediate file

print("stage2!!")
# then extract the first channel
for input_f in tqdm(input_filelist):
    input_f = os.path.join(args.input_file_list, input_f)
    ext_len = len(input_f.split('/')[-1].split('.')[-1])
    video_id = input_f.split('/')[-1][:-ext_len-1]
    output_f_1 = args.target_fold + '/' + video_id + '_intermediate.wav'
    output_f_2 = args.target_fold2 + '/' + video_id + '.wav'
    os.system('sox {:s} {:s} remix 1'.format(output_f_1, output_f_2))
    # remove the intermediate file
    # os.remove(output_f_1)