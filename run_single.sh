while getopts n:e:i: flag
do
    case "${flag}" in
        n) name=${OPTARG};;
        e) elements=${OPTARG};;
        i) iterations=${OPTARG};;
    esac
done
source env/bin/activate;
python bwt.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 4;
python bwt.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 8;
python bwt.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 16;
python bwt.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 64;
python bwt.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 128;
python bwt.py -d 1 -i $iterations -w 1 -e $elements -n $name --single 256;
deactivate;
