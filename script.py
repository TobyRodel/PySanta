import numpy as np
import pandas as pd
from argparse import ArgumentParser
from pysanta import Santas

parser = ArgumentParser(prog='PySanta', description='A Python module for organising secret Santa gift exchanges.')
parser.add_argument('-f', '--inputfile', type=str, help='Path to csv file containing participant info')
parser.add_argument('-u', '--username', type=str, help='Email address to send emails from', default=None)
parser.add_argument('-p', '--password', type=str, help='Email account password (app password for gmail)', default=None)
parser.add_argument('-o', '--spoilerfile', type=str, default='spoilers.csv', help='Path to output spoiler file, defaults to current directory.')
args = parser.parse_args()

gen = np.random.default_rng()

df = pd.read_csv(args['inputfile'])
santas = Santas(names=df['name'], emails=df['email'], hints=df['hint'], account=args['username'], password=args['password'])
santas.createidx()
santas.assignpairs()
santas.createspoilerdf(path=args['spoilerfile'])
santas.sendemails()