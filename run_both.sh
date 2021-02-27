while getopts n:e:i:c: flag
do
    case "${flag}" in
        n) name=${OPTARG};;
        e) elements=${OPTARG};;
        i) iterations=${OPTARG};;
        c) count=${OPTARG};;
    esac
done
source env/bin/activate;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n "${name}_single_${count}" --single 4;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n "${name}_single_${count}" --single 8;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n "${name}_single_${count}" --single 16;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n "${name}_single_${count}" --single 64;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n "${name}_single_${count}" --single 128;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n "${name}_single_${count}" --single 256;
python mp2.py -d 1 -i $iterations -w 1 -e 1 -n "${name}_batch_${count}" --single 1024;
python mp2.py -d 1 -i $iterations -w 1 -e 1 -n "${name}_batch_${count}" --single 2048;
python mp2.py -d 1 -i $iterations -w 1 -e 1 -n "${name}_batch_${count}" --single 4096;
deactivate;
