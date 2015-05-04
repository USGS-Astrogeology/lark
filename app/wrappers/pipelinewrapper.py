import subprocess
import os
import logging

logger = logging.getLogger('ThemisTi')

def themis_davinci(imagepath, uddw, tesatm, deplaid, rtilt, force, workingpath):
    """
    Calls a processing pipeline script, written in Davinci, to convert from
    a spiceinited cube to calibrated temperature data.

    Parameters
    ----------
    imagepath       str The input PATH to the image to be processed
    uddw            int Davinci script parameter
    tesatm          int Davinci script parameter
    deplaid         int DAvinci script parameter

    Returns
    --------
    outputimage     str PATH to the output image, in ISIS3 cube format

    """
    basepath = os.path.dirname(__file__)
    davincipath = '../davinvi'
    spath = os.path.join(basepath, davincipath)
    basepath, fname = os.path.split(imagepath)
    outname, ext = os.path.splitext(fname)
    outpath = os.path.join(workingpath, outname) + '_dvprocessed.cub'
    cmd = r'/home/jlaura/krc_application/app/davinci/ti_pipeline.dv {} {} {} {} {} {} {}'.format(uddw, tesatm, deplaid, rtilt, force, imagepath, outpath)
    logger.debug(cmd)
    cmd = cmd.split()
    response = subprocess.check_output(cmd)
    logger.debug(response)
    return outpath