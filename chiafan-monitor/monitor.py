import subprocess
import requests
import itertools
import re


class Machine(object):
    def __init__(self, ip, port = 5008):
        self.ip = ip
        self.port = port


    def name(self):
        return f'{self.ip}'


    def __repr__(self):
        return f'[{self.ip}]'


    def inspect_fake(self):
        return {
            'server': {
                'pipeline': 'working',
            },
            'jobs': [{
                'name': 'worker1.job1',
                'age': '5:05:05',
                'stage': 'SUCCESS',
                'progress': '100.0 %',
            }, {
                'name': 'worker1.job1',
                'age': '01:02:50',
                'stage': 'FORWARD',
                'progress': '9.71 %',
            }, {
                'name': 'worker2.job1',
                'age': '4:18:18',
                'stage': 'FAIL',
                'progress': '75.00 %',
            }]
        }


    def inspect(self):
        try:
            r = requests.get(url = f'http://{self.ip}:{self.port}/status', verify = False, timeout = 1)
        except:
            return None
        return r.json()


class Monitor(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Monitor, cls).__new__(cls)
            cls._instance.machines = []
        return cls._instance


    def add_machine(self, machine_address):
        address = machine_address.split(':')
        if len(address) == 1:
            self.machines.append(Machine(ip = machine_address))
        elif len(address) == 2:
            self.machines.append(Machine(ip = address[0], port = address[1]))


    def inspect(self):
        active_jobs = []
        past_jobs = []
        machines = []
        for machine in self.machines:
            data = machine.inspect()
            if data is None:
                machines.append({
                    'name': machine.name(),
                    'pipeline': 'dead',
                })
                continue
            machines.append({
                'name': machine.name(),
                'pipeline': data['server']['pipeline'],
            })
            for job_status in data['jobs']:
                job_entry = {
                    'machine': machine.ip,
                    'jobName': job_status['name'],
                    'age': job_status['age'],
                    'stage': job_status['stage'],
                    'progress': job_status['progress'],
                }
                if job_status['stage'] in ['SUCCESS', 'FAIL']:
                    past_jobs.append(job_entry)
                else:
                    active_jobs.append(job_entry)

        jobs = active_jobs + past_jobs
        return {
            'jobs': jobs,
            'machines': machines,
        }
