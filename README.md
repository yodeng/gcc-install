## gcc-install

gcc-install is used for build, install, update gcc/g++/c++ compile tools in rootless.



### requirement

+ linux64
+ python >=3.7
+ gcc     (lower version)



### install

```
pip3 install git+https://github.com/yodeng/gcc-install.git
```



### Usage

```
usage: gcc-install [-h] -g <str> -d <str> -i <str> [-t <int>] [-v]

build, install, update gcc/g++/c++ compile tools in rootless.

support gcc version: 
	['gcc-5.1.0', 'gcc-5.2.0', 'gcc-5.3.0', 'gcc-5.4.0', 'gcc-5.5.0',
	 'gcc-6.1.0', 'gcc-6.2.0', 'gcc-6.3.0', 'gcc-6.4.0', 'gcc-6.5.0', 
	 'gcc-7.1.0', 'gcc-7.2.0', 'gcc-7.3.0', 'gcc-7.4.0', 'gcc-7.5.0',
	 'gcc-8.1.0', 'gcc-8.2.0', 'gcc-8.3.0', 'gcc-8.4.0', 'gcc-8.5.0', 
	 'gcc-9.1.0', 'gcc-9.2.0', 'gcc-9.3.0', 'gcc-9.4.0', 'gcc-9.5.0',
	 'gcc-10.1.0', 'gcc-10.2.0', 'gcc-10.3.0', 'gcc-10.4.0',
	 'gcc-11.1.0', 'gcc-11.2.0', 'gcc-11.3.0', 
	 'gcc-12.1.0', ]	 

optional arguments:
  -h, --help            show this help message and exit
  -g <str>, --gcc <str>
                        which gcc version to install
  -d <str>, --download-dir <str>
                        download directory for gcc source code packages
  -i <str>, --install-dir <str>
                        install directory
  -t <int>, --threads <int>
                        threads number of build gcc, 10 by default
  -v, --version         show program's version number and exit
```



**After install finished,  download-dir can be removed, and you might need to add `${install-dir}/bin` to `PATH` environment variables and `${install-dir}/lib64` to `LD_LIBRARY_PATH`  environment variables like this:**

```shell
export PATH=${install-dir}/bin:$PATH
export LD_LIBRARY_PATH=${install-dir}/lib64:$LD_LIBRARY_PATH
```
