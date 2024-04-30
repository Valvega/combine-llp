from __future__ import print_function, division
import os
import rhalphalib as rl
import numpy as np
import pickle
import uproot
import logging
import sys
import string
from array import array
from collections import OrderedDict
rl.util.install_roofit_helpers()
rl.ParametericSample.PreferRooParametricHist = False
logging.basicConfig(level=logging.DEBUG)
adjust_posdef_yields = False


def get_hist(upfile, name, obs):
    hist_values = upfile[name].values()
    hist_edges  = upfile[name].axis().edges()
    hist_uncs   = upfile[name].variances()

    return (hist_values, hist_edges, obs.name, hist_uncs)


def symmetrize(effectUp, effectDown):
    envelopeUp = np.maximum(effectUp, effectDown)
    envelopeDown = np.minimum(effectUp, effectDown)
    effectUpSym = np.sqrt(envelopeUp/envelopeDown)
    effectDownSym = np.sqrt(envelopeDown/envelopeUp)
    return effectUpSym, effectDownSym


def create_datacard(vll_mass, llp_ctau, inputfile, carddir, nbins, nMCTF, nDataTF, passBinName, failBinName='fail', add_blinded=False, include_ac=False):

    # open uproot file once
    upfile = uproot.open(inputfile)

    regionPairs = [('SR'+passBinName, 'fitfail'+passBinName)]  # pass, fail region pairs

    regions = [item for t in regionPairs for item in t]  # all regions

    #rescaled axis to be compatible with Bernstein polymial
    if 'CSCOOT' in passBinName:
        #CSC OOT
        msdbins = np.array([50,56,62,68,74,84,98,122,220,240]) 
        msd = rl.Observable('nrechits', msdbins)
        msdpts = np.array([53,59,65,71,79,91,110,171,231]) 
        msdscaled = (msdpts-50.)/190
    if 'DTOOT' in passBinName:
        #DT OOT
        msdbins = np.array([50,56,62,68,74,84,98,130,140])
        msd = rl.Observable('nrechits', msdbins)
        msdpts = np.array([53,59,65,71,79,91,114,135])
        msdscaled = (msdpts-50.)/90
    if 'CSCINT' in passBinName:
        msdbins = np.array([50,56,62,68,74,84])
        msd = rl.Observable('nrechits', msdbins)
        msdpts = np.array([53,59,65,71,79])
        msdscaled = (msdpts-50.)/34      
    if 'DTINT' in passBinName:
        msdbins = np.array([50,56,62,68,74,84])
        msd = rl.Observable('nrechits', msdbins)
        msdpts = np.array([53,59,65,71,79])
        msdscaled = (msdpts-50.)/34
    if 'CSCB' in passBinName:
        #CSC Background 
        msdbins = np.array([50,56,62,68,74,84,98,122,220,240])
        msd = rl.Observable('nrechits', msdbins)
        msdpts = np.array([53,59,65,71,79,91,110,171,231]) 
        msdscaled = (msdpts-50.)/190
    if 'DTB' in passBinName:
        #DT Background
        msdbins = np.array([50,56,62,68,74,84,98,130,140])
        msd = rl.Observable('nrechits', msdbins)
        msdpts = np.array([53,59,65,71,79,91,114,135])
        msdscaled = (msdpts-50.)/90
    if 'CSCU' in passBinName:
        #CSC Background (unblinded)
        msdbins = np.array([50,56,62,68,74,84,98,122,220,240]) 
        msd = rl.Observable('cscnrechits', msdbins)
        msdpts = np.array([53,59,65,71,79,91,110,171,231]) 
        msdscaled = (msdpts-50.)/190
    if 'DTU' in passBinName:
        #DT Background (unblinded)
        msdbins = np.array([50,56,62,68,74,84,98,130,140]) 
        msd = rl.Observable('dtnrechits', msdbins)
        msdpts = np.array([53,59,65,71,79,91,114,135])
        msdscaled = (msdpts-50.)/90
    categ        = " "
    if 'CSC' in passBinName: categ ="csc"
    if 'DT'  in passBinName: categ ="dt"

    # Build qcd MC pass+fail model and fit to polynomial
    qcdmodel = rl.Model('qcdmodel')
    qcdpass, qcdfitfail = 0., 0.
    passCh = rl.Channel('passqcdmodel')
    fitfailCh = rl.Channel('fitfailqcdmodel')
    qcdmodel.addChannel(fitfailCh)
    qcdmodel.addChannel(passCh)

    passTempl = get_hist(upfile, 'h_pass_Data', obs=msd)
    fitfailTempl = get_hist(upfile, 'h_fail_Data', obs=msd)

    passCh.setObservation(passTempl[:-1])
    fitfailCh.setObservation(fitfailTempl[:-1])
    qcdpass = passCh.getObservation().sum()

    if 'CSCB' in passBinName:
      qcdfitfail = fitfailTempl[0][0] + fitfailTempl[0][1] + fitfailTempl[0][2] + fitfailTempl[0][3] + fitfailTempl[0][4] #  + fitfailTempl[0][5]
      qcdeffpass = qcdpass / qcdfitfail
    elif 'DTB'  in passBinName:
      qcdfitfail = fitfailTempl[0][0] + fitfailTempl[0][1] + fitfailTempl[0][2] + fitfailTempl[0][3] + fitfailTempl[0][4] # + fitfailTempl[0][5]
      qcdeffpass = qcdpass / qcdfitfail
    else:
      qcdfitfail = fitfailCh.getObservation().sum()
      qcdeffpass = qcdpass / qcdfitfail
    
    # transfer factor
    tf_dataResidual        = rl.BernsteinPoly("CMS_tf_"+passBinName, (nDataTF,), ['%snrechits'%categ], limits=(-20, 20))
    tf_dataResidual_params = tf_dataResidual(msdscaled)
    tf_params_pass         = qcdeffpass * tf_dataResidual_params

    # qcd params
    qcdparams = np.array([rl.IndependentParameter('CMS_param_msdbin%d_%s'%(i,passBinName), 0) for i in range(msd.nbins)])

    #Initialize systematics
    lumi_161718          = rl.NuisanceParameter('lumi',    'lnN') #luminosity
    trigger              = rl.NuisanceParameter('trigger', 'lnN') #trigger
    csc_reo_eff_161718   = rl.NuisanceParameter('vll_csc_readout'    , 'lnN')  #csc reconstruction eff
    csc_rec_eff_161718   = rl.NuisanceParameter('vll_csc_rec'        , 'lnN')  #csc reconstruction eff
    csc_jvt_eff_161718   = rl.NuisanceParameter('vll_csc_jetveto'    , 'lnN')  #csc jet veto eff 
    csc_mvt_eff_161718   = rl.NuisanceParameter('vll_csc_muonveto'   , 'lnN')  #csc muon veto eff 
    csc_cvt_eff_161718   = rl.NuisanceParameter('vll_csc_chamberveto', 'lnN')  #csc chamber veto (ME1/1,RB1,MB1) eff 
    csc_tsp_eff_161718   = rl.NuisanceParameter('vll_csc_timespread' , 'lnN')  #csc time spread eff 
    csc_tim_eff_161718   = rl.NuisanceParameter('vll_csc_time'       , 'lnN')  #csc time eff 
    dt_rec_eff_161718    = rl.NuisanceParameter('vll_dt_rec'         , 'lnN')  #dt reconstruction eff
    dt_jvt_eff_161718    = rl.NuisanceParameter('vll_dt_jetveto'     , 'lnN')  #dt jet veto eff 
    dt_mvt_eff_161718    = rl.NuisanceParameter('vll_dt_muonveto'    , 'lnN')  #dt muon veto eff 
    dt_rpm_eff_161718    = rl.NuisanceParameter('vll_dt_rpcmatch'    , 'lnN')  #dt rpc matching eff 
    dt_awv_eff_161718    = rl.NuisanceParameter('vll_dt_awheelveto'  , 'lnN')  #dt adjacent wheel veto eff 
    dt_tim_eff_161718    = rl.NuisanceParameter('vll_dt_time'        , 'lnN')  #dt time eff
    syst_dir     = 'inputs'
    if "v10" in inputfile:  syst_dir     = syst_dir + "_v10/"
    if "v9" in inputfile:   syst_dir     = syst_dir + "_v9/"
    if "v8" in inputfile:   syst_dir     = syst_dir + "_v8/"

    if 'OOT' in passBinName: syst_dir= syst_dir+"syst_oot/"
    elif 'INT' in passBinName: syst_dir= syst_dir+"syst_int/"
    else: syst_dir= syst_dir+"syst/"

    # build actual fit model now
    model = rl.Model("VLLModel_%s"%passBinName)
    for region in regions:
        logging.info('starting region: %s' % region)
        ch = rl.Channel(region)
        model.addChannel(ch)

        if 'SR' in region:
            tagname='pass'
            infilename  = syst_dir+"file_%s_VLLPair_VLLToTauS_MVLL%s_MS10_ctau%s.txt"%(categ, vll_mass, llp_ctau)
        else:
            tagname='fail'
            infilename  = syst_dir+"file_%s_0VVL_VLLPair_VLLToTauS_MVLL%s_MS10_ctau%s.txt"%(categ, vll_mass, llp_ctau)

        # dictionary of name in datacards -> name in ROOT file
        templateNames = OrderedDict([
            ('datadriven', 'h_%s_Data'%tagname),
            ('data', 'h_%s_Data'%tagname),
            ('vll_%s_%s'%(vll_mass,llp_ctau) , 'h_%s_VLL%s_ctau%s'%(tagname,vll_mass,llp_ctau)  ),
        ])

        #Add extra uncertainties
        systs = []
        with open(infilename, "r") as my_input_file:
            for line in my_input_file:
                line = line.split()
                if 'pileup' or 'JES' in line[0]:
                   var   = rl.NuisanceParameter('%s'%(line[0]) , 'lnN')
                else:
                   var   = rl.NuisanceParameter('vll_%s'%(line[0]) , 'lnN')
                value = line[1]
                systs.append([var,value])

        templates = {}
        for temp in templateNames:
            templates[temp] = get_hist(upfile, templateNames[temp], obs=msd)

        sNames = [proc for proc in templates.keys() if proc not in ['datadriven', 'data']]

        for sName in sNames:
            logging.info('get templates for: %s' % sName)
            # get templates
            templ = templates[sName]
            # don't allow them to go negative
            valuesNominal = np.maximum(templ[0], 0.)
            templ = (valuesNominal, templ[1], templ[2], templ[3])
            stype = rl.Sample.SIGNAL if 'vll' in sName else rl.Sample.BACKGROUND
            sample = rl.TemplateSample(ch.name + '_' + sName, stype, templ)
            if 'CSC' in passBinName:
                    sample.setParamEffect(csc_rec_eff_161718, 1.130)
                    sample.setParamEffect(csc_jvt_eff_161718, 1.001)
                    sample.setParamEffect(csc_mvt_eff_161718, 1.045)
                    sample.setParamEffect(csc_cvt_eff_161718, 1.001)
                    sample.setParamEffect(csc_tsp_eff_161718, 1.028)
                    sample.setParamEffect(csc_tim_eff_161718, 1.009)
                    sample.setParamEffect(csc_reo_eff_161718, 1.010)
            if 'DT' in passBinName:
                    sample.setParamEffect(dt_rec_eff_161718,  1.160)
                    #sample.setParamEffect(dt_jvt_eff_161718,  1.001)
                    #sample.setParamEffect(dt_mvt_eff_161718,  1.045)
                    #sample.setParamEffect(dt_rpm_eff_161718,  1.050)
                    #sample.setParamEffect(dt_awv_eff_161718,  1.080)
                    #sample.setParamEffect(dt_tim_eff_161718,  1.030)
            for syst in systs: sample.setParamEffect(syst[0], float(syst[1]) )
            # set mc stat uncs
            #sample.autoMCStats()
            ch.addSample(sample)

        # data observed
        yields = templates['data'][0] 
        data_obs = (yields, msd.binning, msd.name)
        ch.setObservation(data_obs) #-1?

    for passChName, failChName in regionPairs:
        logging.info('setting transfer factor for pass region %s, fail region %s' % (passChName, failChName))
        failCh = model[failChName]
        passCh = model[passChName]

        # sideband fail
        initial_qcd = failCh.getObservation().astype(float)  # was integer, and numpy complained about subtracting float from it

        sigmascale = 10  # to scale the deviation from initial
        scaledparams = initial_qcd * (1 + sigmascale/np.maximum(1., np.sqrt(initial_qcd)))**qcdparams

        # add samples
        fail_qcd = rl.ParametericSample(failChName+'_datadriven', rl.Sample.BACKGROUND, msd, scaledparams)
        failCh.addSample(fail_qcd)

        pass_qcd = rl.TransferFactorSample(passChName+'_datadriven', rl.Sample.BACKGROUND, tf_params_pass, fail_qcd)
        passCh.addSample(pass_qcd)

    with open(os.path.join(str(carddir), 'VLLModel_%s.pkl'%passBinName), "wb") as fout:
        pickle.dump(model, fout, 2)  # use python 2 compatible protocol

    logging.info('rendering combine model')
    model.renderCombine(os.path.join(str(carddir), 'VLLModel_%s'%passBinName))


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputfile', default='HHTo4BPlots_Run2_BDTv8p2_0311_syst_Trigv0.root', type=str, dest='inputfile', help='input ROOT file')
    parser.add_argument('--carddir', default='cards', type=str, dest='carddir', help='output card directory')
    parser.add_argument('--nbins', default=8, type=int, dest='nbins', help='number of bins')
    parser.add_argument('--nMCTF', default=0, type=int, dest='nMCTF', help='order of polynomial for TF from MC')
    parser.add_argument('--nDataTF', default=0, type=int, dest='nDataTF', help='order of polynomial for TF from Data')
    parser.add_argument('--passBinName', default='CSCOOT', type=str, choices=['CSCOOT', 'DTOOT','CSCINT', 'DTINT','CSCB','DTB','CSCU','DTU'], help='pass bin name')
    parser.add_argument('--blinded', action='store_true', help='run on data on SR')
    parser.add_argument('--vll_mass', default='300',  type=str, dest='vll_mass', help='vll mass [GeV]')
    parser.add_argument('--llp_ctau', default='1000', type=str, dest='llp_ctau', help='llp ctau [mm]')

    args = parser.parse_args()
    if not os.path.exists(args.carddir):
        os.mkdir(args.carddir)
    create_datacard(args.vll_mass, args.llp_ctau, args.inputfile, args.carddir, args.nbins, args.nMCTF, args.nDataTF, args.passBinName, "fail", args.blinded)
