import os
import re

from .utils import *


class BuildGCC(Utils):

    def __init__(self, version, download_dir, verbose=True, threads=20):
        self.version = re.match("^\d", version) and "gcc-" + version or version
        self.download_dir = os.path.abspath(download_dir)
        self.verbose = verbose
        self.threads = threads

    def download_gcc(self):
        url = os.path.join(gcc_base_url, self.version,
                           self.version + ".tar.gz")
        self.mkdirs(self.download_dir)
        filename = os.path.basename(url)
        outfile = os.path.join(self.download_dir, filename)
        if not os.path.isfile(outfile) or os.path.isfile(outfile+".ht"):
            hget(url=url, outfile=os.path.join(self.download_dir,
                 filename), quite=True, timeout=30)
        self.uncompress(os.path.join(self.download_dir, filename),
                        self.download_dir, verbose=False)
        with open(os.path.join(self.download_dir, self.version, "contrib/download_prerequisites")) as fo:
            ctx = fo.read()
        try:
            base_url = re.findall("\s+base_url='(.+)'\s+", ctx)[0]
            gmp = re.findall("\s+gmp='(gmp-.+)'\s+", ctx)[0]
            mpfr = re.findall("\s+mpfr='(mpfr-.+)'\s+", ctx)[0]
            mpc = re.findall("\s+mpc='(mpc-.+)'\s+", ctx)[0]
            isl = re.findall("\s+isl='(isl-.+)'\s+", ctx)[0]
        except:
            base_url = re.findall("wget (.+?)\s+", ctx)
            gmp = re.findall("\s+GMP=(gmp-.+)\s", ctx)[0]
            mpfr = re.findall("\s+MPFR=(mpfr-.+)\s", ctx)[0]
            mpc = re.findall("\s+MPC=(mpc-.+)\s", ctx)[0]
            isl = re.findall("\s+ISL=(isl-.+)\s", ctx)[0]
            for i, _ in enumerate(base_url):
                t = string.Template(base_url[i])
                u = t.safe_substitute(
                    {"GMP": gmp, "MPFR": mpfr, "MPC": mpc, "ISL": isl})
                base_url[i] = u
            gmp, mpfr, mpc, isl = base_url
        for n in [gmp, mpfr, mpc, isl]:
            if ":" in n:
                url = n
            else:
                url = os.path.join(base_url, n)
            n = os.path.basename(url)
            outfile = os.path.join(
                self.download_dir, self.version, os.path.basename(url))
            if not os.path.isfile(outfile) or os.path.isfile(outfile+".ht"):
                hget(url=url, outfile=outfile, timeout=30, quite=True)
            self.uncompress(os.path.join(self.download_dir, self.version, n), os.path.join(
                self.download_dir, self.version), verbose=False)
            self.call(["ln", "-sf", os.path.join(self.download_dir, self.version, n.split(".tar.")
                                                 [0]), os.path.join(self.download_dir, self.version, n.split("-")[0])], shell=False, verbose=False)

    def build(self, install_dir):
        configure_cmd = "./configure --prefix=%s -enable-checking=release --enable-languages=c,c++ --disable-multilib" % install_dir
        make_cmd = "make -j %s" % self.threads
        make_install_cmd = "make install -j %s" % self.threads
        os.chdir(os.path.join(self.download_dir, self.version))
        for c in [configure_cmd, make_cmd, make_install_cmd]:
            self.call(c, shell=True, verbose=False)

    @property
    def loger(self):
        return logging.getLogger()

    def install(self, install_dir):
        self.loger.info(
            "starting download %s and all dependancy", self.version)
        self.download_gcc()
        self.loger.info("download %s success", self.version)
        time.sleep(3)
        self.loger.info("starting build %s", self.version)
        install_dir = os.path.abspath(install_dir)
        self.build(install_dir)
        self.loger.info("install %s success: %s", self.version, install_dir)
