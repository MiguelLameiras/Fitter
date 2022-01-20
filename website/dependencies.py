from ctypes import sizeof
import re
import io
import os
import base64
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from flask import Flask, redirect, flash,url_for, render_template,request

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['ytick.direction'] = 'in'
matplotlib.rcParams['xtick.direction'] = 'in'

from scipy.interpolate import CubicSpline
import numpy as np
from scipy.optimize import curve_fit
from lmfit.models import ExpressionModel
from lmfit import Parameters,model
from plotter import *