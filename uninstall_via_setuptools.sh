sudo python setup.py install --record rm_me1.txt
sudo python3 setup.py install --record rm_me2.txt

cat rm_me1.txt | xargs sudo rm -rf
cat rm_me2.txt | xargs sudo rm -rf

rm rm_me1.txt
rm rm_me2.txt

sudo rm -rf build/
sudo rm -rf dist/
sudo rm -rf pysh_gp.egg-info/

if [ "$1" == "--reinstall" ]; then
	sudo python setup.py install
	sudo python3 setup.py install
fi
