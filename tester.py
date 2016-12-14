import argparse
from base64 import b64decode
from re import findall
import signal
import sys
from statistics import mean, median, stdev
import boto3
from apscheduler.schedulers.blocking import BlockingScheduler
from scipy.stats import scoreatpercentile

l = boto3.client('lambda')

parser = argparse.ArgumentParser()
parser.add_argument('function',
    help='name/ARN of the lambda function to call')
parser.add_argument('--freq', type=int, default=60,
    help='number of seconds between each call (default: 60)')
parser.add_argument('--count', type=int, default=0,
    help='number of times to call function (default: 0 (infinite))')

args = parser.parse_args()

durations = []

scheduler = BlockingScheduler()

def endgame(*_):
    if args.count > 0:
        print('\a', end='') # sound the bell to alert the user
    print('\nEnding, with {} executions sent.'.format(len(durations)))
    if len(durations) >= 2:
        stats = [
            ('Mean', mean(durations)),
            ('Median', median(durations)),
            ('Standard deviation', stdev(durations)),
            ('5th percentile', scoreatpercentile(durations, 5)),
            ('95th percentile', scoreatpercentile(durations, 95)),
        ]
        for name, stat in stats:
            print('{0}: {1:.2f} ms'.format(name, stat))
    sys.exit(0)

def execute():
    print('Executing function...', end='  ', flush=True)
    response = l.invoke(
        FunctionName=args.function,
        InvocationType='RequestResponse',
        LogType='Tail'
    )
    log = b64decode(response['LogResult']).decode('UTF-8')
    duration = float(findall(r'\tDuration: (\d+(?:\.\d*)) ms', log)[0])
    print('{} ms'.format(duration))
    durations.append(duration)
    if args.count > 0 and len(durations) >= args.count:
        scheduler.shutdown(wait=False)

signal.signal(signal.SIGINT, endgame)

scheduler.add_job(execute, 'interval', seconds=args.freq)
print('Starting, {} seconds until first execution...'.format(args.freq))
scheduler.start()

# when the scheduler is killed
endgame()