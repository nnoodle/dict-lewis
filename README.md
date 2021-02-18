# dict-lewis
dictd database of "A Latin Dictionary" by Lewis and Short.

## dependencies
On Ubuntu, you'll need to install the following packages:
```sh
sudo apt-get install dictzip dictfmt dictd
```

## installation

First, clone this repository and the submodules.
```sh
git clone --recursive-submodules https://github.com/nnoodle/dict-lewis
```

Next, inside the `dict-lewis` folder, build and install the dictionary database.
```sh
cd dict-lewis
make
sudo make install
```

Then you'll need to write this to the end of your `/etc/dictd/dictd.conf` file.
```
database lewis
 {
  data  /usr/share/dictd/lewis.dict.dz
  index /usr/share/dictd/lewis.index
}
```
(Optionally, you may tweak the order in which dictionary entries appear by
adding `lewis` in `/etc/dictd/dictd.order`)


Finally, restart `dictd.service`.
```sh
systemctl restart dictd.service

```
Check that it's properly installed with:
```sh
dict -I # you should see the 'lewis' database
```

## license
The code is licensed under the MIT license. The XML data is available
under the CC BY-SA 3.0 from https://github.com/PerseusDL/lexica.

Forked from [ids1024's](https://github.com/ids1024) [lscli](https://github.com/ids1024/lscli).
