import subprocess
import requests
import itertools
import re


class Machine(object):
    def __init__(self, ip, port = 5008):
        self.ip = ip
        self.port = port


    def __repr__(self):
        return f'[{self.name}] [{self.region}.{self.instance}] [{self.ip}]'


    def inspect(self):
        r = requests.get(url = f'http://{self.ip}:{self.port}/status')
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
        jobs = []
        for machine in self.machines:
            data = machine.inspect()
            for job_status in data['jobs']:
                jobs.append({
                    'machine': machine.ip,
                    'jobName': job_status['name'],
                    'age': job_status['age'],
                    'stage': job_status['stage'],
                    'progress': job_status['progress'],
                })
        return {
            'jobs': jobs
        }
