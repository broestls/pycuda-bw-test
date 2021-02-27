while getopts n:e:i: flag
do
    case "${flag}" in
        n) name=${OPTARG};;
        e) elements=${OPTARG};;
        i) iterations=${OPTARG};;
    esac
done
source env/bin/activate;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 4;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 8;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 16;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 64;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 128;
python mp2.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 256;
deactivate;
