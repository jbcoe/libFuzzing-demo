#!/usr/bin/env python
import sys
import os
import platform
import shutil
import subprocess


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--clean',
        help='remove build directory before build',
        action='store_true',
        dest='clean')

    test_options = parser.add_mutually_exclusive_group()
    test_options.add_argument(
        '-t', help='run tests', action='store_true', dest='run_tests')
    test_options.add_argument(
        '-T', help='run labelled tests', dest='labelled_tests')

    parser.add_argument(
        '-v', help='verbose', action='store_true', dest='verbose')
    parser.add_argument(
        '-o',
        help='output dir (relative to source dir)',
        default='build',
        dest='out_dir')
    parser.add_argument(
        '-c',
        help='config (Debug or Release)',
        default='Debug',
        dest='config')
    parser.add_argument(
        '--python-path',
        help='path to python executable ie "/usr/local/bin/python3"',
        dest='python_path')

    if platform.system() == "Windows":
        parser.add_argument(
            '--win32',
            help='Build 32-bit libraries',
            action='store_true',
            dest='win32')

    args = parser.parse_args()
    args.platform = platform.system()

    src_dir = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

    if args.clean and os.path.exists(args.out_dir):
        shutil.rmtree(args.out_dir)

    cmake_invocation = ['cmake', '.', '-B{}'.format(args.out_dir)]
    if args.platform == 'Windows':
        if args.win32:
            cmake_invocation.extend(['-G', 'Visual Studio 14 2015'])
        else:
            cmake_invocation.extend(['-G', 'Visual Studio 14 2015 Win64'])
    else:
        cmake_invocation.extend(['-GNinja', '-DCMAKE_BUILD_TYPE={}'.format(args.config)])

    if args.verbose:
        cmake_invocation.append('-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON')
    if args.python_path:
        cmake_invocation.append(
            '-DPYTHON_EXECUTABLE={}'.format(args.python_path))

    subprocess.check_call(cmake_invocation, cwd=src_dir)
    subprocess.check_call(
        'cmake --build ./{}'.format(args.out_dir).split(), cwd=src_dir)

    rc = 0
    if args.run_tests:
        rc = subprocess.call(
            'ctest . --output-on-failure -C {}'.format(args.config).split(),
            cwd=os.path.join(src_dir, args.out_dir))
    elif args.labelled_tests:
        rc = subprocess.call(
            'ctest . --output-on-failure -C {} -L {}'.format(args.config, args.labelled_tests).split(),
            cwd=os.path.join(src_dir, args.out_dir))
    if rc != 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
