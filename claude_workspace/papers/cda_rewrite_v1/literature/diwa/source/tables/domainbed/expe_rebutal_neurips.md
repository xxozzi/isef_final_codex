
# scaling number of runs from 1 to M


/gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm601shhps0406home

CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/sam203shhps0426home --mode iterg_train-out-acc-soup_1_60 --ood_data train,test --do_ens 0 --trial_seed 0 &
CUDA_VISIBLE_DEVICES=1 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/sam203shhps0426home --mode iterg_train-out-acc-soup_1_60 --ood_data train,test --do_ens 0 --trial_seed 1 &
CUDA_VISIBLE_DEVICES=2 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/sam203shhps0426home --mode iterg_train-out-acc-soup_1_60 --ood_data train,test --do_ens 0 --trial_seed 2 &
wait


home_erm601shhps0406_env0.slurm

/gpfsdswork/projects/rech/edr/utr15kn/slurmconfig/0406/combinhome0_erm601_1to60.slurm


# hpl


/gpfsdswork/projects/rech/edr/utr15kn/slurmconfig/home00415/runs/combinhome0_erm203shhpl0501.slurm_1603091.out


/gpfswork/rech/edr/utr15kn/slurmconfig/home00415/combinhome0_erm203shhpl0501.slurm


SEED=0 SWAMEMBER=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhpl0501home --regexes net0_net1 --do_ens net --mode combin_2_3_500 --trial_seed 0 &
SEED=0 SWAMEMBER=0 CUDA_VISIBLE_DEVICES=1 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhpl0501home --regexes net0_net1 --do_ens net --mode combin_2_3_500 --trial_seed 1 &
SEED=0 SWAMEMBER=0 CUDA_VISIBLE_DEVICES=2 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhpl0501home --regexes net0_net1 --do_ens net --mode combin_2_3_500 --trial_seed 2 &
wait

# SAM

iterghome0_sam203shhps0426.slu


# ens table 1

(bias) rame@hacienda:~/slurmconfig/dnlp0502$ squeue | grep rame
             25413     jazzy   ensdn5     rame  R       0:03      1 pas
             25411     jazzy   ensdn4     rame  R       0:27      1 pas
             25410     jazzy   ensdn3     rame  R       0:40      1 pas
             25409     jazzy   ensdn2     rame  R       0:53      1 cal
             25408     jazzy   ensdn1     rame  R       1:05      1 cal
             25407     jazzy   ensdn0     rame  R       3:33      1 cal




INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 0
INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 1 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 0
INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 2 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 0
INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 3 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 0

INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 1
INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 1 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 1
INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 2 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 1
INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 3 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 1

INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 2
INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 1 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 2
INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 2 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 2
INFOLDER=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --mode ens --do_ens net --dataset TerraIncognita --test_envs 3 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shlphps0424terra --trial_seed 2

# ens random

INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 0
INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 1 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 0
INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 2 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 0
INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 3 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 0

INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 1
INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 1 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 1
INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 2 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 1
INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 3 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 1

INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 2
INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 1 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 2
INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 2 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 2
INFOLDER=1 SWAMEMBER=0 PRETRAINED=0 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.soup --dataset OfficeHome --test_envs 3 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/erm203shhps0406home --mode ens --do_ens net --ood_data test --trial_seed 2


# last layer retraining
     JOBID PARTITION                           NAME     USER ST       TIME  NODES NODELIST(REASON)
   1610568   gpu_p13 home0ontest8_ermllr_lpe_0727.s  utr15kn PD       0:00      1 (None)
   1610015   gpu_p13  home0ontest_ermllr_0727.slurm  utr15kn  R    1:16:30      1 r12i3n6
   1609995   gpu_p13 home0ontest_ermllr_lpd_0727.sl  utr15kn  R    1:19:06      1 r10i4n5
   1610073   gpu_p13 home0ontest_ermllr_lpe_0727.sl  utr15kn  R      57:07      1 r13i6n6
   1610566   gpu_p13 home0ontest8_ermllr_0727.slurm  utr15kn  R       0:05      1 r10i0n4
   1610552   gpu_p13 home0ontest8_ermllr_lpd_0727.s  utr15kn  R       1:06      1 r11i0n7

Tolaunch inference: enshomeontest_lp_0727.slurm


KEEP_ALL_ENV=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.diwa --dataset OfficeHome --test_env 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/home0ontest_ermllr_lpd_0727 --trial_seed 0 --data_dir /gpfswork/rech/edr/utr15kn/dataplace/data/domainbed
KEEP_ALL_ENV=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.diwa --dataset OfficeHome --test_env 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/home0ontest_ermllr_lpd_0727 --trial_seed 1 --data_dir /gpfswork/rech/edr/utr15kn/dataplace/data/domainbed
KEEP_ALL_ENV=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.diwa --dataset OfficeHome --test_env 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/home0ontest_ermllr_lpd_0727 --trial_seed 2 --data_dir /gpfswork/rech/edr/utr15kn/dataplace/data/domainbed

KEEP_ALL_ENV=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.diwa --dataset OfficeHome --test_env 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/home0ontest_ermllr_lpe_0727 --trial_seed 0 --data_dir /gpfswork/rech/edr/utr15kn/dataplace/data/domainbed
KEEP_ALL_ENV=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.diwa --dataset OfficeHome --test_env 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/home0ontest_ermllr_lpe_0727 --trial_seed 1 --data_dir /gpfswork/rech/edr/utr15kn/dataplace/data/domainbed
KEEP_ALL_ENV=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.diwa --dataset OfficeHome --test_env 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/home0ontest_ermllr_lpe_0727 --trial_seed 2 --data_dir /gpfswork/rech/edr/utr15kn/dataplace/data/domainbed

KEEP_ALL_ENV=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.diwa --dataset OfficeHome --test_env 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/home0ontest_ermllr_0727 --trial_seed 0 --data_dir /gpfswork/rech/edr/utr15kn/dataplace/data/domainbed
KEEP_ALL_ENV=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.diwa --dataset OfficeHome --test_env 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/home0ontest_ermllr_0727 --trial_seed 1 --data_dir /gpfswork/rech/edr/utr15kn/dataplace/data/domainbed
KEEP_ALL_ENV=1 CUDA_VISIBLE_DEVICES=0 python3 -m domainbed.scripts.diwa --dataset OfficeHome --test_env 0 --output_dir /gpfswork/rech/edr/utr15kn/dataplace/experiments/domainbed/home0ontest_ermllr_0727 --trial_seed 2 --data_dir /gpfswork/rech/edr/utr15kn/dataplace/data/domainbed
