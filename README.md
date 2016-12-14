# lambda-stopwatch

[![asciicast](https://asciinema.org/a/cei4arkpb01n2kc7c2psz3sju.png)](https://asciinema.org/a/cei4arkpb01n2kc7c2psz3sju)
lambda-stopwatch is a simple Python script that calls your AWS Lambda function repeatedly and outputs statistics about its response time.

## How do I use it?

First, you'll want to install the dependencies:
```
pip3 install boto3 apscheduler scipy
```

Then you can start the script. At a minimum you must specify the Lambda function to use, but you can also use a couple other arguments:
```
usage: tester.py [-h] [--freq FREQ] [--count COUNT] function

positional arguments:
  function       name/ARN of the lambda function to call

optional arguments:
  -h, --help     show this help message and exit
  --freq FREQ    number of seconds between each call (default: 60)
  --count COUNT  number of times to call function (default: 0 (infinite))
```
(with a `--count` of 0, the script will run until you stop it with Ctrl-C)

Protip: If you run this script for a long period of time (>30 minutes) you can use Amazon CloudWatch Metrics to generate pretty charts of the latency.
