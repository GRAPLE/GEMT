#!/usr/bin/env python
import os
from os import listdir
from os.path import isdir, isfile, join
import tarfile
import subprocess
import argparse
import logging
import shutil
import time
import json
import pandas
import csv


RUNCMD = '''#!/bin/sh\npython Graple.py -r\n'''
#RUNCMD = '''C:\Python27\python.exe Graple.py -r\n'''

SUBMIT = '''universe=vanilla
executable=Condor/run.sh
output=Logs/sim{JobNumber}.out
error=Logs/sim{JobNumber}.err
log=Logs/sim{JobNumber}.log
request_memory=512M
requirements=(TARGET.Arch == "X86_64") && (TARGET.OpSys == "LINUX")
transfer_input_files=Scratch/job{JobNumber}.tar.bz2, Graple.py
transfer_output_files=Results.tar.bz2, graple.log
transfer_output_remaps="Results.tar.bz2=Results/Results{JobNumber}.tar.bz2; graple.log=Logs/graple{JobNumber}.log"
should_transfer_files=YES
when_to_transfer_output=ON_EXIT
notification=never
Queue {QueueCount}'''

class Graple:
    def __init__(self, topdir):
        self.CONFIG = {
            'SimsPerJob' : '5',
            'RunR' : 'True',
            'Rmain' : 'PostProcessFilter.R',
            'Rexe' : '/usr/bin/Rscript',
            'LogFile' : 'graple.log',
            'SubmitMode' : 'SingleSubmit',
            'SimRoot' : topdir
        }
        if 'SimRoot' in self.CONFIG:
            self.top_dir = self.CONFIG['SimRoot']
        else:
            self.top_dir = os.getcwd()
        self.SetupLogger()
        self.ParseArgs()
        self.ScriptsDir = os.path.join(self.top_dir, 'Scripts')
        self.SimsDir = os.path.join(self.top_dir, 'Sims')
        self.CondorDir = os.path.join(self.top_dir, 'Condor')
        self.TempDir = os.path.join(self.top_dir, 'Scratch')
        self.LogsDir = os.path.join(self.top_dir, 'Logs')
        self.ResultsDir = os.path.join(self.top_dir, 'Results')
        self.ZipBasename = join(self.TempDir, 'job')
        self.logger.debug("CONFIG: %s", self.CONFIG)
        self.logger.debug("top_dir: %s", self.top_dir)

    def ParseArgs(self,):
        self.parser = argparse.ArgumentParser(prog='Graple', description='Helper program to prep, run & collect sim results')
        self.parser.add_argument('-p', '--prep', dest='prep', action='store_true', help='Creates a series archives each containing a batch of simulations')
        self.parser.add_argument('-r', '--run', dest='run', action='store_true', help='Unpacks archives and executes simulations')
        self.parser.add_argument('-f', '--fixup', dest='fixup', action='store_true', help='Puts the output of each Sim into its orignial source folder')
        self.parser.add_argument('-m', '--mkdirs', dest='mkdirs', action='store_true', help='Creates the working folder structure')
        
    def isCreateWorkingFolders(self):
        if self.parser.parse_args().mkdirs:
            return True

    def isSimPrep(self,):
        arg = self.parser.parse_args()
        if arg.prep or (not arg.prep and not arg.run and not arg.fixup and not arg.mkdirs):
            return True
        else: return False

    def isSimRun(self,):
        if self.parser.parse_args().run:
            return True
        else: return False

    def isSimFixup(self,):
        if self.parser.parse_args().fixup:
            return True
        else: return False

    def SetupLogger(self,):
        self.logger = logging.basicConfig(filename = os.path.join(self.top_dir, self.CONFIG['LogFile']), level = logging.DEBUG, format = '%(asctime)s:%(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def CreateWorkingFolders(self, NumSims=0):
        if not isdir(self.ScriptsDir):
            os.mkdir(self.ScriptsDir)
        
        if not isdir(self.TempDir):
            os.mkdir(self.TempDir)

        if not isdir(self.CondorDir):
            os.mkdir(self.CondorDir)

        if not isdir(self.SimsDir):
            os.mkdir(self.SimsDir)

        if not isdir(self.LogsDir):
            os.mkdir(self.LogsDir)

        if not isdir(self.ResultsDir):
            os.mkdir(self.ResultsDir)

        for i in range(NumSims):
            if not isdir(os.path.join(self.SimsDir, 'Sim' + str(i))):
                os.mkdir(os.path.join(self.SimsDir, 'Sim' + str(i)))
        self.logger.info("Created working folders")

    def ZipDir(self, path, archiver):
        for root, dirs, files in os.walk(path):
            for file in files:
                archiver.write(os.path.join(root, file))

    def CreateJob(self, SimDirList, JobName):
        ## Creates a single job ZIP file
        with tarfile.open(JobName, 'w:bz2', compresslevel=9) as tar:
            tar.add(self.ScriptsDir, 'Scripts')
            for adir in SimDirList:
                tar.add(adir, 'Sims/' + os.path.basename(os.path.normpath(adir)))
                shutil.rmtree(adir)
        self.logger.info(JobName + ' created')

    def SubmitAJob(self, JobNum):
        submitFile = open(join(self.CondorDir, 'jobs.submit'), 'w')
        SubmitStr=SUBMIT.format(JobNumber=JobNum, QueueCount=1)   
        submitFile.write(SubmitStr)
        submitFile.close()
        runFile = open(join(self.CondorDir, 'run.sh'), 'w')
        runFile.write(RUNCMD)
        runFile.close()
        self.logger.info('Submitting simulation {JobNumber} to HTCondor pool.'.format(JobNumber=JobNum))
        subprocess.call(['condor_submit', os.path.join(self.CondorDir, 'jobs.submit')], cwd = self.top_dir)
        
    def SimPrepSingleSubmit(self,):
        self.logger.info('Preparing simulations for HTCondor submission...')
        ## Creates the series of job archives
        SimsForJob = []
        count = 0
        jobSuffix = 0
        #build the list of Simxxx dirs to add to the job archives
        for dirname in listdir(self.SimsDir):
            fqdn = os.path.join(self.SimsDir, dirname)
            if isdir(fqdn):
                SimsForJob.append(fqdn)
                count += 1  #count is used to limit how many sims are packed into a job
                if count % int(self.CONFIG['SimsPerJob']) == 0: # Submit Job Just If It Is a Directory
                    jn = self.ZipBasename + str(jobSuffix) + '.tar.bz2'
                    self.CreateJob(SimsForJob, jn)
                    self.SubmitAJob(jobSuffix)
                    jobSuffix += 1
                    SimsForJob = []
        if len(SimsForJob) > 0:
            jn = self.ZipBasename + str(jobSuffix) + '.tar.bz2'
            self.CreateJob(SimsForJob, jn)
            self.SubmitAJob(jobSuffix)
            jobSuffix += 1
            SimsForJob = []
        self.logger.info('All jobs submitted')
    
    def SubmitJobs(self, NumberOfJobs):
        submitFile = open(join(self.CondorDir, 'jobs.submit'), 'w')
        SubmitStr=SUBMIT.format(JobNumber='$(Process)', QueueCount=NumberOfJobs) 
        submitFile.write(SubmitStr)
        submitFile.close()
        runFile = open(join(self.CondorDir, 'run.sh'), 'w')
        runFile.write(RUNCMD)
        runFile.close()
        self.logger.info('Submitting simulations to HTCondor pool.')
        subprocess.call(['condor_submit', join(self.CondorDir, 'jobs.submit')])

    def SimPrepBatchSubmit(self):
        self.logger.info('Preparing simulations for HTCondor submission...')
        ## Creates the series of job archives
        SimsForJob = []
        count = 0
        jobSuffix = 0
        #build the list of Simxxx dirs to add to the job archives
        for dir in listdir(self.SimsDir):
            fqdn = join(self.SimsDir, dir)
            if isdir(fqdn):
                SimsForJob.append(fqdn)
                count += 1  #count is used to limit how many sims are packed into a job
            if count % int(self.CONFIG['SimsPerJob']) == 0:
                jn = self.ZipBasename + str(jobSuffix) + '.tar.bz2'
                self.CreateJob(SimsForJob, jn)
                jobSuffix += 1
                SimsForJob = []
        if len(SimsForJob) > 0:
            jn = self.ZipBasename + str(jobSuffix) + '.tar.bz2'
            self.CreateJob(SimsForJob, jn)
            jobSuffix += 1
            SimsForJob = []
        self.SubmitJobs(jobSuffix)

    def SimPrep(self):
        start = end = 0
        if self.CONFIG['SubmitMode'] == 'SingleSubmit':
            start = time.clock()
            self.SimPrepSingleSubmit()
            end = time.clock()
        if self.CONFIG['SubmitMode'] == 'BatchSubmit':
            start = time.clock()
            self.SimPrepBatchSubmit()
            end = time.clock()
        self.logger.debug('Duration for {0} is {1}'.format(self.CONFIG['SubmitMode'], end-start))
        
    def RunJob(self, simdir):
        rexe = self.CONFIG['Rexe']
        glm = "/usr/local/bin/glm"
        rscript = os.path.join(self.ScriptsDir, self.CONFIG['Rmain'])
        self.logger.info("Running simulation at path %s", simdir)
        if isdir(simdir):
            results_dir = os.path.join(simdir, 'Results')
            os.mkdir(results_dir)
            res = subprocess.call([glm], cwd = simdir)
            for filename in os.listdir(simdir):
                filename = os.path.join(simdir, filename)
                if (os.path.isdir(filename) == False):
                    shutil.move(os.path.join(simdir, filename), results_dir)
            if os.path.isfile(rscript): 
                if self.CONFIG['RunR'] == 'True':
                    self.logger.info("Running post processing filter")
                    res = subprocess.call([rexe, '--vanilla', rscript], cwd = simdir)
                    if res != 0:
                        if os.path.isfile(os.path.join(results_dir, 'output.nc')):
                            os.remove(os.path.join(results_dir, 'output.nc'))
                            self.logger.error('Post Processing filter failed at {0}. Removing output file'.format(results_dir))
            else: 
                for filename in os.listdir(results_dir):
                    fullname = os.path.join(results_dir, filename)
                    if(os.path.isdir(fullname) == False and filename != 'output.nc'):
                        os.remove(fullname)

    def SimRun(self,):
        ## Runs a single job on the Condor execute node and packages the
        ## results that are returned to the client.
        self.logger.info("Simulation invoked at path %s", self.top_dir)
              
        for JobName in listdir(self.top_dir):
            if isfile(JobName) and JobName.endswith('.tar.bz2'):
                with tarfile.open(JobName, 'r') as tar:
                    tar.extractall()
                break

        self.logger.info("Simulations extracted")
        # before entering loop, create multiple subdirectories in SimsDir for a generate job
        sims_list = listdir(self.SimsDir)
        if len(sims_list) > 0:
            generate_file = os.path.join(self.SimsDir, sims_list[0], "generate.json")
            if os.path.exists(generate_file):
                master_copy = os.path.join(self.SimsDir, sims_list[0])
                with open(generate_file) as jfd:
                    to_generate = json.load(jfd)
                varcomb = to_generate[0]
                iterprod = to_generate[1]
                for subSimNo in range(len(iterprod)):
                    subSimDir = os.path.join(self.SimsDir, sims_list[0] + "_" + str(subSimNo + 1))
                    shutil.copytree(master_copy, subSimDir)
                    # look at to_generate and modify csv files in subSimDir
                    for i in range(len(varcomb)):
                        var_list = varcomb[i].split(",")
                        base_file = os.path.join(subSimDir, var_list[0])
                        field = var_list[1]
                        operation = var_list[3]
                        delta = iterprod[subSimNo][i]
                        data = pandas.read_csv(base_file)
                        data = data.rename(columns=lambda x: x.strip())
                        if (((" "+field) in data.columns) or (field in data.columns)):
                        # handle variations in filed names in csv file, some field names have leading spaces.
                            if " "+field in data.columns:
                                field_modified = " "+field
                            else:
                                field_modified = field
                        if (operation=="add"):
                            data[field_modified]=data[field_modified].apply(lambda val:val+delta)
                        elif (operation=="sub"):
                            data[base_file][field_modified]=data[field_modified].apply(lambda val:val-delta)
                        elif (operation=="mul"):
                            data[field_modified]=data[field_modified].apply(lambda val:val*delta)
                        elif (operation=="div"):
                            data[field_modified]=data[field_modified].apply(lambda val:val/delta)
                        data.to_csv(base_file,index=False)
                    self.RunJob(subSimDir)
                shutil.rmtree(master_copy)
                self.logger.info("Generate and run job complete")
            else:
                for d in sims_list:
                    simdir = os.path.join(self.SimsDir, d)
                    self.RunJob(simdir)

        self.logger.info("All simulations complete. Starting compression")
        
        with tarfile.open(os.path.join(self.top_dir, 'Results.tar.bz2'), 'w:bz2',compresslevel=9) as tar:
            for d in listdir(self.SimsDir):
                #resultsdir = join(join(join(topdir, 'Sims'), d), 'Results')
                resultsdir = os.path.join(self.SimsDir, d, 'Results')
                if isdir(resultsdir):
                    tar.add(resultsdir, 'Sims/' + d + '/Results')

        self.logger.info("SimRun finished")


    def SimFixup(self,):
        ## Unpacks the result archives on the client side and cleans 
        ## up unused directories.
        if not isdir(self.ResultsDir):
             self.logger.error('Results directory does not exist')
             return
        for f in listdir(self.top_dir):
            try:
                if f.endswith('.tar.bz2'):
                    with tarfile.open(f, 'r') as tar:
                        tar.extractall()
                    self.logger.debug(f + ' extracted')
                    os.remove(f)
            except Exception as e:
                self.logger.exception('Failed to open tarfile ' + f)
        if isdir(self.TempDir):
            shutil.rmtree(self.TempDir)
        if isdir(self.CondorDir):
            shutil.rmtree(self.CondorDir)
        
if __name__ == '__main__':
    sm = Graple(os.getcwd())
    if sm.isCreateWorkingFolders():
        sm.CreateWorkingFolders()
    if sm.isSimPrep():
        sm.SimPrep()
    if sm.isSimRun():
        sm.SimRun()
    if sm.isSimFixup():
        sm.SimFixup()
