#!/usr/bin/env python2

import argparse
import hashlib
import os
import posixpath
import sys
import time
import urllib #.parse #python3

import lxml.etree

HASHES = (
    'md5',
    'sha1',
    'sha256',
    'sha512',
    'ripemd160',
)

BASE = '/pub/qubes/repo/yum'

__version__ = '1.0'

class Metalink(object):
    def __init__(self, path):
        self.path = path

        self.root = lxml.etree.Element('metalink',
            nsmap={
                None: 'http://www.metalinker.org/',
                'mm0': 'http://fedorahosted.org/mirrormanager',
            },
            version='3.0',
            generator='mkmetalink/{}'.format(__version__))

        files = self._element('files')
        self.root.append(files)

        self.repomd = self._element('file', name='repomd.xml')
        files.append(self.repomd)

        self.repomd.append(self._element(
            '{http://fedorahosted.org/mirrormanager}timestamp',
            time.strftime('%s')))

        self.verification = self._element('verification')
        self.repomd.append(self.verification)

        self.resources = self._element('resources')
        self.repomd.append(self.resources)


    @staticmethod
    def _element(_tag, _text=None, **kwargs):
        element = lxml.etree.Element(_tag, **kwargs)
        if _text is not None:
            element.text = _text
        return element

    @property
    def filename(self):
        return os.path.join(self.path, 'repodata', 'repomd.xml')


    def add_hash(self, algo):
        h = hashlib.new(algo)
        f = open(self.filename, 'rb')

        while True:
            data = f.read(1024)
            if not data:
                break
            h.update(data)

        f.close()

        element = lxml.etree.Element('hash', type=algo)
        element.text = h.hexdigest()
        self.verification.append(element)

        return element


    def add_resource(self, mirror):
#       scheme = urllib.parse.urlsplit(mirror)[0] #python3
        scheme = urllib.splittype(mirror)[0] #python2
        element = lxml.etree.Element('url', protocol=scheme, type=scheme)
        element.text = posixpath.join(mirror, self.filename)
        self.resources.append(element)

        return element


    def write(self, stream):
        return lxml.etree.ElementTree(self.root).write(
            stream, encoding='utf-8', pretty_print=True)


parser = argparse.ArgumentParser()

parser.add_argument('--hash', '-H', metavar='ALGO',
    action='append',
    help='hash files with this algorithm; can be repeated')

parser.add_argument('mirrorlist', metavar='MIRRORLIST',
    help='mirror file containing list of mirrors')

parser.add_argument('repo', metavar='REPOSITORY',
    help='path to repository')

parser.set_defaults(hash=[])


def main():
    args = parser.parse_args()

    metalink = Metalink(args.repo)

    for algo in args.hash:
        metalink.add_hash(algo)

    for mirror in open(args.mirrorlist).read().strip().split():
        metalink.add_resource(mirror)

    metalink.write(sys.stdout) #.buffer


if __name__ == '__main__':
    main()

# vim: ts=4 sts=4 sw=4 et
