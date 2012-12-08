#!/usr/bin/python -t

import optparse
import sys
import os
from os.path import join,splitext,isfile,isdir,basename

def main(argv):
    """
    Iterate over all directories in 'rawdir' and compare their contents to
    the corresponding directory in 'jpegdir'. First stripping off file extensions.

    This is helpful for syncing up raw and jpeg dirs after culling the obviously
    bad shots out of the jpeg dir

    """
    o = optparse.OptionParser()
    o.add_option("-r", "--rawdir", dest="rawdir",
            help="directory containing raw's to compare", metavar="DIR")
    o.add_option("-j", "--jpegdir", dest="jpegdir",
            help="directory containing jpeg's to compare", metavar="DIR")
    o.add_option("-d", "--dryrun", dest="dryrun",
            help="just print what you would delete", metavar="BOOL", default=False)

    (options, args) = o.parse_args()

    if not options.rawdir or not options.jpegdir:
        o.print_help()
        exit(1)

    raw_dirs = [ d for d in os.listdir(options.rawdir)
            if isdir(join(options.rawdir, d)) ]

    for raw_dir in raw_dirs:
        if not os.path.exists(join(options.jpegdir, raw_dir)):
            continue

        jpegs = [ f for f in os.listdir(join(options.jpegdir, raw_dir)) 
                if isfile(join(options.jpegdir, raw_dir, f)) ]
        raws = [ f for f in os.listdir(join(options.rawdir, raw_dir)) 
                if isfile(join(options.rawdir, raw_dir, f)) ]

        for r in raws:
            r_filename,_ = splitext(basename(r))
            found = False
            for j in jpegs:
                j_filename,_ = splitext(basename(j))
                if r_filename == j_filename:
                    found = True
            if not found:
                print("unlink {}".format(join(options.rawdir, raw_dir, r)))
                if not options.dryrun:
                    os.unlink(join(options.rawdir, raw_dir, r))


if __name__ == '__main__':
    main(sys.argv)
