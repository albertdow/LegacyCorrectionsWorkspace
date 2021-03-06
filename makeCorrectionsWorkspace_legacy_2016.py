#!/usr/bin/env python
import ROOT
import imp
import json
from array import array
wsptools = imp.load_source('wsptools', 'workspaceTools.py')


def GetFromTFile(str):
    f = ROOT.TFile(str.split(':')[0])
    obj = f.Get(str.split(':')[1]).Clone()
    f.Close()
    return obj


# Boilerplate
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.RooWorkspace.imp = getattr(ROOT.RooWorkspace, 'import')
ROOT.TH1.AddDirectory(0)
ROOT.gROOT.LoadMacro("CrystalBallEfficiency.cxx+")

w = ROOT.RooWorkspace('w')

# EGamma tracking SFs from https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaRunIIRecommendations#Electron_Scale_Factors
loc = 'inputs/2016/EGammaPOG'

histsToWrap = [
    (loc+'/EGM2D_BtoH_low_RecoSF_Legacy2016.root:EGamma_EffData2D',
     'e_trk_ST20_data'),
    (loc+'/EGM2D_BtoH_low_RecoSF_Legacy2016.root:EGamma_EffMC2D',           
    'e_trk_ST20_mc'),
    (loc+'/EGM2D_BtoH_low_RecoSF_Legacy2016.root:EGamma_SF2D',
     'e_trk_ST20_ratio'),
    (loc+'/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root:EGamma_EffData2D',
     'e_trk_GT20_data'),
    (loc+'/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root:EGamma_EffMC2D',
     'e_trk_GT20_mc'),
    (loc+'/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root:EGamma_SF2D',
     'e_trk_GT20_ratio')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_eta', 'e_pt'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_pt', [10., 20., 500.],
                                   'e_trk_data', ['e_trk_ST20_data', 'e_trk_GT20_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_pt', [10., 20., 500.],
                                   'e_trk_mc', ['e_trk_ST20_mc', 'e_trk_GT20_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_pt', [10., 20., 500.],
                                   'e_trk_ratio', ['e_trk_ST20_ratio', 'e_trk_GT20_ratio'])

# KIT electron/muon tag and probe results
# The trigger refers to OR(IsoMu22, IsoTkMu22, IsoMu22_eta2p1, IsoTkMu22_eta2p1)
loc = 'inputs/2016/KIT/legacy_16_v1'

histsToWrap = [
    (loc+'/ZmmTP_Data_sm_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',
     'm_id_data'),
    (loc+'/ZmmTP_DYJetsToLL_sm_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',              'm_id_mc'),
    (loc+'/ZmmTP_Embedding_sm_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',
     'm_id_emb'),
    (loc+'/ZmmTP_Data_sm_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',
     'm_iso_data'),
    (loc+'/ZmmTP_DYJetsToLL_sm_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',
     'm_iso_mc'),
    (loc+'/ZmmTP_Embedding_sm_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',
     'm_iso_emb'),
    (loc+'/ZmmTP_Data_sm_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',
     'm_aiso1_data'),
    (loc+'/ZmmTP_DYJetsToLL_sm_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',
     'm_aiso1_mc'),
    (loc+'/ZmmTP_Embedding_sm_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',
     'm_aiso1_emb'),
    (loc+'/ZmmTP_Data_sm_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',
     'm_aiso2_data'),
    (loc+'/ZmmTP_DYJetsToLL_sm_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',
     'm_aiso2_mc'),
    (loc+'/ZmmTP_Embedding_sm_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',
     'm_aiso2_emb'),
    (loc+'/ZmmTP_Data_sm_Fits_Trg_IsoMu22_Iso_pt_eta_bins.root:Trg_IsoMu22_Iso_pt_eta_bins',
     'm_trg_data'),
    (loc+'/ZmmTP_DYJetsToLL_sm_Fits_Trg_IsoMu22_Iso_pt_eta_bins.root:Trg_IsoMu22_Iso_pt_eta_bins',
     'm_trg_mc'),
    (loc+'/ZmmTP_Embedding_sm_Fits_Trg_IsoMu22_Iso_pt_eta_bins.root:Trg_IsoMu22_Iso_pt_eta_bins',
     'm_trg_emb'),
    (loc+'/ZmmTP_Data_sm_Fits_Trg_IsoMu22_AIso1_pt_bins_inc_eta.root:Trg_IsoMu22_AIso1_pt_bins_inc_eta',    'm_trg_aiso1_data'),
    (loc+'/ZmmTP_DYJetsToLL_sm_Fits_Trg_IsoMu22_AIso1_pt_bins_inc_eta.root:Trg_IsoMu22_AIso1_pt_bins_inc_eta',    'm_trg_aiso1_mc'),
    (loc+'/ZmmTP_Embedding_sm_Fits_Trg_IsoMu22_AIso1_pt_bins_inc_eta.root:Trg_IsoMu22_AIso1_pt_bins_inc_eta',    'm_trg_aiso1_emb'),
    (loc+'/ZmmTP_Data_sm_Fits_Trg_IsoMu22_AIso2_pt_bins_inc_eta.root:Trg_IsoMu22_AIso2_pt_bins_inc_eta',    'm_trg_aiso2_data'),
    (loc+'/ZmmTP_DYJetsToLL_sm_Fits_Trg_IsoMu22_AIso2_pt_bins_inc_eta.root:Trg_IsoMu22_AIso2_pt_bins_inc_eta',    'm_trg_aiso2_mc'),
    (loc+'/ZmmTP_Embedding_sm_Fits_Trg_IsoMu22_AIso2_pt_bins_inc_eta.root:Trg_IsoMu22_AIso2_pt_bins_inc_eta',    'm_trg_aiso2_emb')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])


wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_data', ['m_iso_data', 'm_aiso1_data', 'm_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_mc', ['m_iso_mc', 'm_aiso1_mc', 'm_aiso2_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_emb', ['m_iso_emb', 'm_aiso1_emb', 'm_aiso2_emb'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg_binned_data', ['m_trg_data', 'm_trg_aiso1_data', 'm_trg_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg_binned_mc', ['m_trg_mc', 'm_trg_aiso1_mc', 'm_trg_aiso2_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg_binned_emb', ['m_trg_emb', 'm_trg_aiso1_emb', 'm_trg_aiso2_emb'])


for t in ['id', 'iso', 'aiso1', 'aiso2', 'iso_binned', 'trg', 'trg_aiso1', 'trg_aiso2', 'trg_binned']:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))

for t in ['id', 'iso', 'aiso1', 'aiso2', 'iso_binned', 'trg', 'trg_aiso1', 'trg_aiso2', 'trg_binned']:
    w.factory('expr::m_%s_ratio_emb("@0/@1", m_%s_data, m_%s_emb)' % (t, t, t))

for t in ['data', 'mc', 'emb', 'ratio', 'ratio_emb']:
    w.factory('expr::m_idiso_%s("@0*@1", m_id_%s, m_iso_%s)' % (t, t, t))

loc = 'inputs/2016/KIT/legacy_16_v1'

histsToWrap = [
    (loc+'/ZeeTP_Data_Fits_ID80_pt_eta_bins.root:ID80_pt_eta_bins',
     'e_id80_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_ID80_pt_eta_bins.root:ID80_pt_eta_bins',
     'e_id80_mc'),
    (loc+'/ZeeTP_Embedding_Fits_ID80_pt_eta_bins.root:ID80_pt_eta_bins',
     'e_id80_emb'),
    (loc+'/ZeeTP_Data_Fits_ID90_pt_eta_bins.root:ID90_pt_eta_bins',
     'e_id90_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_ID90_pt_eta_bins.root:ID90_pt_eta_bins',
     'e_id90_mc'),
    (loc+'/ZeeTP_Embedding_Fits_ID90_pt_eta_bins.root:ID90_pt_eta_bins',
     'e_id90_emb'),
    (loc+'/ZeeTP_Data_Fits_ID90_pt_eta_bins.root:ID90_pt_eta_bins',
     'e_id_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_ID90_pt_eta_bins.root:ID90_pt_eta_bins',
     'e_id_mc'),
    (loc+'/ZeeTP_Embedding_Fits_ID90_pt_eta_bins.root:ID90_pt_eta_bins',
     'e_id_emb'),
    (loc+'/ZeeTP_Data_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',
     'e_iso_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',
     'e_iso_mc'),
    (loc+'/ZeeTP_Embedding_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',
     'e_iso_emb'),
    (loc+'/ZeeTP_Data_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',
     'e_aiso1_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',
     'e_aiso1_mc'),
    (loc+'/ZeeTP_Embedding_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',
     'e_aiso1_emb'),
    (loc+'/ZeeTP_Data_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',
     'e_aiso2_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',
     'e_aiso2_mc'),
    (loc+'/ZeeTP_Embedding_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',
     'e_aiso2_emb'),
    (loc+'/ZeeTP_Data_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',
     'e_trg_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',
     'e_trg_mc'),
    (loc+'/ZeeTP_Embedding_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',
     'e_trg_emb'),
    (loc+'/ZeeTP_Data_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',
     'e_trg_aiso1_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',    'e_trg_aiso1_mc'),
    (loc+'/ZeeTP_Embedding_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',
     'e_trg_aiso1_emb'),
    (loc+'/ZeeTP_Data_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',
     'e_trg_aiso2_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',    'e_trg_aiso2_mc'),
    (loc+'/ZeeTP_Embedding_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',
     'e_trg_aiso2_emb')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])


wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_iso_binned_data', ['e_iso_data', 'e_aiso1_data', 'e_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_iso_binned_mc', ['e_iso_mc', 'e_aiso1_mc', 'e_aiso2_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_iso_binned_emb', ['e_iso_emb', 'e_aiso1_emb', 'e_aiso2_emb'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg_binned_data', ['e_trg_data', 'e_trg_aiso1_data', 'e_trg_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg_binned_mc', ['e_trg_mc', 'e_trg_aiso1_mc', 'e_trg_aiso2_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg_binned_emb', ['e_trg_emb', 'e_trg_aiso1_emb', 'e_trg_aiso2_emb'])


for t in ['id', 'iso', 'aiso1', 'aiso2', 'iso_binned', 'trg', 'trg_aiso1', 'trg_aiso2', 'trg_binned']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))

for t in ['id', 'iso', 'aiso1', 'aiso2', 'iso_binned', 'trg', 'trg_aiso1', 'trg_aiso2', 'trg_binned']:
    w.factory('expr::e_%s_ratio_emb("@0/@1", e_%s_data, e_%s_emb)' % (t, t, t))

for t in ['data', 'mc', 'emb', 'ratio', 'ratio_emb']:
    w.factory('expr::e_idiso_%s("@0*@1", e_id_%s, e_iso_%s)' % (t, t, t))

# addressing muon selection for embedding:
loc = 'inputs/2016/KIT'  # so far not remeasured for legacy
Sel_histsToWrap = [
    (loc+'/ZmmTP_Data_Fits_muon_Selection_EmbeddedID.root:muon_Selection_EmbeddedID',
     'm_sel_idEmb_data'),
    (loc+'/ZmmTP_Data_Fits_muon_Selection_VVLIso.root:muon_Selection_VVLIso',
     'm_sel_vvliso_data')
]
for task in Sel_histsToWrap:
    wsptools.SafeWrapHist(w, ['gt_pt', 'expr::gt_abs_eta("TMath::Abs(@0)",gt_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])
for t in ['sel_idEmb', 'sel_vvliso']:
    w.factory('expr::m_%s_ratio("(1.0)/@0", m_%s_data)' % (t, t))


# DESY electron/muon tag and probe results
# Muons
loc = 'inputs/2016/LeptonEfficiencies'

desyHistsToWrap = [
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IdIso.root',
     'MC',   'm_idiso_desy_mc'),
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IdIso.root',
     'Data', 'm_idiso_desy_data'),
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IsoMu22.root',
     'MC',   'm_trgIsoMu22_desy_mc'),
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IsoMu22.root',
     'Data', 'm_trgIsoMu22_desy_data'),
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IsoMu24.root',
     'MC',   'm_trgIsoMu24_desy_mc'),
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IsoMu24.root',
     'Data', 'm_trgIsoMu24_desy_data'),

    # old crosstrigger weights for now
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_2016BtoH_eff.root',
     'MC', 'm_trgMu19leg_eta2p1_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_2016BtoH_eff.root',
     'Data', 'm_trgMu19leg_eta2p1_desy_data'),
]

for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])
for t in ['idiso_desy', 'trgIsoMu22_desy', 'trgIsoMu24_desy', 'trgMu19leg_eta2p1_desy']:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))

# Electrons
desyHistsToWrap = [
    (loc+'/Electron/Run2016_legacy/Electron_Run2016_legacy_IdIso.root',
     'MC',   'e_idiso_desy_mc'),
    (loc+'/Electron/Run2016_legacy/Electron_Run2016_legacy_IdIso.root',
     'Data', 'e_idiso_desy_data'),
    (loc+'/Electron/Run2016_legacy/Electron_Run2016_legacy_Ele25.root',
     'MC',   'e_trgEle25_desy_mc'),
    (loc+'/Electron/Run2016_legacy/Electron_Run2016_legacy_Ele25.root',
     'Data', 'e_trgEle25_desy_data')
]
for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])

for t in ['idiso_desy', 'trgEle25_desy']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))


# IC electron/muon embedded scale factors
loc_ic = 'inputs/2016/ICSF/'

histsToWrap = [
    (loc_ic+'MuMu8/muon_SFs.root:trg_data', 'm_sel_trg8_1_data'),
    (loc_ic+'MuMu17/muon_SFs.root:trg_data', 'm_sel_trg17_1_data')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['gt1_pt', 'expr::gt1_abs_eta("TMath::Abs(@0)",gt1_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

histsToWrap = [
    (loc_ic+'MuMu8/muon_SFs.root:trg_data', 'm_sel_trg8_2_data'),
    (loc_ic+'MuMu17/muon_SFs.root:trg_data', 'm_sel_trg17_2_data')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['gt2_pt', 'expr::gt2_abs_eta("TMath::Abs(@0)",gt2_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

    w.factory('expr::m_sel_trg_data("0.935*(@0*@3+@1*@2-@1*@3)", m_sel_trg8_1_data, m_sel_trg17_1_data, m_sel_trg8_2_data, m_sel_trg17_2_data)')
w.factory('expr::m_sel_trg_ratio("min(1./@0,2)", m_sel_trg_data)')

# LO DYJetsToLL Z mass vs pT correction
histsToWrap = [
    ('inputs/2016/KIT/zpt_reweighting/zptm_weights_2016_kit.root:zptmass_histo', 'zptmass_weight_nom')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['z_gen_mass', 'z_gen_pt'],
                          GetFromTFile(task[0]), name=task[1])

# emu and mu+tau trigger and loose (<0.2) muon isolation scale factors from IC

loc = 'inputs/2016/ICSF/'

histsToWrap = [
    (loc+'EM_HI/muon_SFs.root:data_trg_eff', 'm_trg_23_data'),
    (loc+'EM_HI/muon_SFs.root:ZLL_trg_eff', 'm_trg_23_mc'),
    (loc+'EM_LO/muon_SFs.root:data_trg_eff', 'm_trg_8_data'),
    (loc+'EM_LO/muon_SFs.root:ZLL_trg_eff', 'm_trg_8_mc'),
    (loc+'EM_HI/muon_SFs.root:data_iso_eff', 'm_looseiso_data'),
    (loc+'EM_HI/muon_SFs.root:ZLL_iso_eff', 'm_looseiso_mc'),

    (loc+'EM_HI/aiso/muon_SFs.root:data_trg_eff', 'm_trg_23_aiso_data'),
    (loc+'EM_HI/aiso/muon_SFs.root:ZLL_trg_eff', 'm_trg_23_aiso_mc'),
    (loc+'EM_LO/aiso/muon_SFs.root:data_trg_eff', 'm_trg_8_aiso_data'),
    (loc+'EM_LO/aiso/muon_SFs.root:ZLL_trg_eff', 'm_trg_8_aiso_mc'),
    (loc+'EM_LO/aiso/muon_SFs.root:data_iso_eff', 'm_looseiso_aiso_data'),
    (loc+'EM_LO/aiso/muon_SFs.root:ZLL_iso_eff', 'm_looseiso_aiso_mc'),

    (loc+'MU19/muon_SFs.root:data_trg_eff', 'm_trg_19_data'),
    (loc+'MU19/muon_SFs.root:ZLL_trg_eff', 'm_trg_19_mc'),
    (loc+'MU19/aiso1/muon_SFs.root:data_trg_eff', 'm_trg_19_aiso1_data'),
    (loc+'MU19/aiso1/muon_SFs.root:ZLL_trg_eff', 'm_trg_19_aiso1_mc'),
    (loc+'MU19/aiso2/muon_SFs.root:data_trg_eff', 'm_trg_19_aiso2_data'),
    (loc+'MU19/aiso2/muon_SFs.root:ZLL_trg_eff', 'm_trg_19_aiso2_mc'),
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.2, 0.50],
                                   'm_trg_binned_23_data', ['m_trg_23_data', 'm_trg_23_aiso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.2, 0.50],
                                   'm_trg_binned_23_mc', ['m_trg_23_mc', 'm_trg_23_aiso_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.2, 0.50],
                                   'm_trg_binned_8_data', ['m_trg_8_data', 'm_trg_8_aiso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.2, 0.50],
                                   'm_trg_binned_8_mc', ['m_trg_8_mc', 'm_trg_8_aiso_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg_binned_19_data', ['m_trg_19_data', 'm_trg_19_aiso1_data', 'm_trg_19_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trg_binned_19_mc', ['m_trg_19_mc', 'm_trg_19_aiso1_mc', 'm_trg_19_aiso2_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.2, 0.50],
                                   'm_looseiso_binned_data', ['m_looseiso_data', 'm_looseiso_aiso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.2, 0.50],
                                   'm_looseiso_binned_mc', ['m_looseiso_mc', 'm_looseiso_aiso_mc'])

w.factory('expr::m_looseiso_ratio("@0/@1", m_looseiso_data, m_looseiso_mc)')

w.factory('expr::m_looseiso_binned_ratio("@0/@1", m_looseiso_binned_data, m_looseiso_binned_mc)')

for t in ['trg','trg_binned']:
    w.factory('expr::m_%s_23_ratio("@0/@1", m_%s_23_data, m_%s_23_mc)' % (t, t, t))
    w.factory('expr::m_%s_8_ratio("@0/@1", m_%s_8_data, m_%s_8_mc)' % (t, t, t))
    w.factory('expr::m_%s_19_ratio("@0/@1", m_%s_19_data, m_%s_19_mc)' % (t, t, t))
    w.factory('expr::m_%s_8_embed_ratio("@0/@1", m_%s_8_data, m_%s_8_embed)' % (t, t, t))

# emu trigger electron scale factors from IC

loc = 'inputs/2016/ICSF/'

histsToWrap = [
    (loc+'EM_LO/electron_SFs.root:data_trg_eff', 'e_trg_12_data'),
    (loc+'EM_LO/electron_SFs.root:ZLL_trg_eff', 'e_trg_12_mc'),
    (loc+'EM_HI/electron_SFs.root:data_trg_eff', 'e_trg_23_data'),
    (loc+'EM_HI/electron_SFs.root:ZLL_trg_eff', 'e_trg_23_mc'),

    (loc+'EM_LO/aiso/electron_SFs.root:data_trg_eff', 'e_trg_12_aiso_data'),
    (loc+'EM_LO/aiso/electron_SFs.root:ZLL_trg_eff', 'e_trg_12_aiso_mc'),
    (loc+'EM_HI/aiso/electron_SFs.root:data_trg_eff', 'e_trg_23_aiso_data'),
    (loc+'EM_HI/aiso/electron_SFs.root:ZLL_trg_eff', 'e_trg_23_aiso_mc'),
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.5],
                                   'e_trg_binned_23_data', ['e_trg_23_data', 'e_trg_23_aiso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.50],
                                   'e_trg_binned_23_mc', ['e_trg_23_mc', 'e_trg_23_aiso_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.50],
                                   'e_trg_binned_12_data', ['e_trg_12_data', 'e_trg_12_aiso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.15, 0.50],
                                   'e_trg_binned_12_mc', ['e_trg_12_mc', 'e_trg_12_aiso_mc'])

for t in ['trg','trg_binned']:
    w.factory('expr::e_%s_12_ratio("@0/@1", e_%s_12_data, e_%s_12_mc)' % (t, t, t))
    w.factory('expr::e_%s_23_ratio("@0/@1", e_%s_23_data, e_%s_23_mc)' % (t, t, t))

## IC em qcd os/ss weights
loc = 'inputs/2016/ICSF/'
wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_maiso.root:qcd_factors'), 'em_qcd_factors')
wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_bothaiso.root:qcd_factors'), 'em_qcd_factors_bothaiso')
#wsptools.SafeWrapHist(w, ['expr::dR_max4p5("min(@0,4.5)",dR[0])','expr::njets_max1("min(@0,1)",njets[0])'],  GetFromTFile(loc+'/em_qcd/em_aiso_iso_extrap.root:extrap_uncert'), 'em_qcd_extrap_uncert')
wsptools.SafeWrapHist(w, ['expr::m_pt_max40("min(@0,40)",m_pt[0])','expr::e_pt_max40("min(@0,40)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_isoextrap.root:isoextrap_uncert'), 'em_qcd_extrap_uncert')

w.factory('expr::em_qcd_0jet("(2.162-0.05135*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_1jet("(2.789-0.2712*@0)*@1",dR[0],em_qcd_factors)')

w.factory('expr::em_qcd_0jet_bothaiso("(3.212-0.2186*@0)*@1",dR[0],em_qcd_factors_bothaiso)')
w.factory('expr::em_qcd_1jet_bothaiso("(3.425-0.3629*@0)*@1",dR[0],em_qcd_factors_bothaiso)')

w.factory('expr::em_qcd_0jet_shapeup("(2.162-(0.05135-0.0583)*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_0jet_shapedown("(2.162-(0.05135+0.0583)*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_1jet_shapeup("(2.789-(0.2712-0.0390)*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_1jet_shapedown("(2.789-(0.2712+0.0390)*@0)*@1",dR[0],em_qcd_factors)')

w.factory('expr::em_qcd_0jet_rateup("(2.162+0.192-0.05135*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_0jet_ratedown("(2.162-0.192-0.05135*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_1jet_rateup("(2.789+0.0105-0.2712*@0)*@1",dR[0],em_qcd_factors)')
w.factory('expr::em_qcd_1jet_ratedown("(2.789-0.0105-0.2712*@0)*@1",dR[0],em_qcd_factors)')

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_binned', ['em_qcd_0jet','em_qcd_1jet'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_binned_bothaiso', ['em_qcd_0jet_bothaiso','em_qcd_1jet_bothaiso'])


wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_shapeup_binned', ['em_qcd_0jet_shapeup','em_qcd_1jet_shapeup'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_shapedown_binned', ['em_qcd_0jet_shapedown','em_qcd_1jet_shapedown'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_rateup_binned', ['em_qcd_0jet_rateup','em_qcd_1jet_rateup'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_ratedown_binned', ['em_qcd_0jet_ratedown','em_qcd_1jet_ratedown'])


wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_2.root:qcd_factors'), 'em_qcd_factors_bothaiso') # TODO what is the difference between factors and factors_2

w.factory('expr::em_qcd_0jet_bothaiso("(3.208-0.217*@0)*@1",dR[0],em_qcd_factors_bothaiso)')
w.factory('expr::em_qcd_1jet_bothaiso("(3.426-0.3628*@0)*@1",dR[0],em_qcd_factors_bothaiso)')

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_binned_bothaiso', ['em_qcd_0jet_bothaiso','em_qcd_1jet_bothaiso'])

w.factory('expr::em_qcd_extrap_up("@0*@1",em_qcd_osss_binned,em_qcd_extrap_uncert)')
w.factory('expr::em_qcd_extrap_down("@0*(2-@1)",em_qcd_osss_binned,em_qcd_extrap_uncert)')

w.factory('expr::em_qcd_bothaiso_extrap_up("@0*@1",em_qcd_osss_binned_bothaiso,em_qcd_extrap_uncert)')
w.factory('expr::em_qcd_bothaiso_extrap_down("@0*(2-@1)",em_qcd_osss_binned_bothaiso,em_qcd_extrap_uncert)') # TODO check this

em_funcs = ['em_qcd_osss_binned','em_qcd_osss_shapeup_binned','em_qcd_osss_shapedown_binned','em_qcd_osss_rateup_binned','em_qcd_osss_ratedown_binned']
for i in em_funcs:
  w.factory('expr::%s_mva("(@0<=0)*@1 + (@0>0)*1.11632",nbjets[0],%s)' %(i,i))
# add uncertainty on n_bjets>0 bin = +/-36% (11% statistical + 18% background-subtraction + 29% aiso->iso extrapolation added in quadrature)
w.factory('expr::em_qcd_osss_binned_mva_nbjets_up("(@0<=0)*@1 + (@0>0)*1.11632*1.36",nbjets[0],em_qcd_osss_binned)')
w.factory('expr::em_qcd_osss_binned_mva_nbjets_down("(@0<=0)*@1 + (@0>0)*1.11632*0.64",nbjets[0],em_qcd_osss_binned)')

### Tau Trigger scale factors from Tau POG

loc = 'inputs/2016/TauPOGTriggerSFs/'
tau_trg_file = ROOT.TFile(loc+'tauTriggerEfficiencies2016.root')
w.factory('expr::t_pt_trig("min(max(@0,20),450)" ,t_pt[0])')
tau_id_wps=['vloose','loose','medium','tight','vtight']

for wp in tau_id_wps:
  for dm in ['0','1','10']:
    histsToWrap = [
      (loc+'tauTriggerEfficiencies2016.root:ditau_%sMVAv2_dm%s_DATA' % (wp,dm),  't_trg_phieta_%s_ditau_dm%s_data' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:ditau_%sMVAv2_dm%s_MC' % (wp,dm),  't_trg_phieta_%s_ditau_dm%s_mc' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:ditau_%sMVAv2_dm%s_DATA_AVG' % (wp,dm),  't_trg_ave_phieta_%s_ditau_dm%s_data' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:ditau_%sMVAv2_dm%s_MC_AVG' % (wp,dm),  't_trg_ave_phieta_%s_ditau_dm%s_mc' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:mutau_%sMVAv2_dm%s_DATA' % (wp,dm),  't_trg_phieta_%s_mutau_dm%s_data' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:mutau_%sMVAv2_dm%s_MC' % (wp,dm),  't_trg_phieta_%s_mutau_dm%s_mc' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:mutau_%sMVAv2_dm%s_DATA_AVG' % (wp,dm),  't_trg_ave_phieta_%s_mutau_dm%s_data' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:mutau_%sMVAv2_dm%s_MC_AVG' % (wp,dm),  't_trg_ave_phieta_%s_mutau_dm%s_mc' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:etau_%sMVAv2_dm%s_DATA' % (wp,dm),  't_trg_phieta_%s_etau_dm%s_data' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:etau_%sMVAv2_dm%s_MC' % (wp,dm),  't_trg_phieta_%s_etau_dm%s_mc' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:etau_%sMVAv2_dm%s_DATA_AVG' % (wp,dm),  't_trg_ave_phieta_%s_etau_dm%s_data' % (wp,dm)),
      (loc+'tauTriggerEfficiencies2016.root:etau_%sMVAv2_dm%s_MC_AVG' % (wp,dm),  't_trg_ave_phieta_%s_etau_dm%s_mc' % (wp,dm))
    ]
    for task in histsToWrap:  
      wsptools.SafeWrapHist(w, ['t_eta','t_phi'],
                            GetFromTFile(task[0]), name=task[1])

    for x in ['data', 'mc']:
      for y in ['ditau','mutau','etau']:
        func = tau_trg_file.Get("%s_%sMVAv2_dm%s_%s_fit" % (y,wp,dm,x.upper())) 
        params = func.GetParameters()
        w.factory('expr::t_trg_pt_%s_%s_dm%s_%s("%.12f - ROOT::Math::crystalball_cdf(-@0, %.12f, %.12f, %.12f, %.12f)*(%.12f)", t_pt_trig)' % (wp,y,dm,x, params[5],params[0],params[1],params[2],params[3],params[4]))
  
        w.factory('expr::t_trg_phieta_%s_%s_%s("(@0==0)*@1 + (@0==1)*@2 + (@0>=3)*@3", t_dm[0], t_trg_phieta_%s_%s_dm0_%s, t_trg_phieta_%s_%s_dm1_%s, t_trg_phieta_%s_%s_dm10_%s)' % (wp, y, x, wp, y, x, wp, y, x, wp, y, x))
        w.factory('expr::t_trg_ave_phieta_%s_%s_%s("(@0==0)*@1 + (@0==1)*@2 + (@0>=3)*@3", t_dm[0], t_trg_ave_phieta_%s_%s_dm0_%s, t_trg_ave_phieta_%s_%s_dm1_%s, t_trg_ave_phieta_%s_%s_dm10_%s)' % (wp, y, x, wp, y, x, wp, y, x, wp, y, x))
  
        w.factory('expr::t_trg_pt_%s_%s_%s("(@0==0)*@1 + (@0==1)*@2 + (@0>=3)*@3", t_dm[0], t_trg_pt_%s_%s_dm0_%s, t_trg_pt_%s_%s_dm1_%s, t_trg_pt_%s_%s_dm10_%s)' % (wp, y, x, wp, y, x, wp, y, x, wp, y, x)) 

        w.factory('expr::t_trg_%s_%s_data("min(@0*@1/@2,1)", t_trg_pt_%s_%s_data, t_trg_phieta_%s_%s_data, t_trg_ave_phieta_%s_%s_data)' % (wp, y, wp, y, wp, y, wp, y))  
        w.factory('expr::t_trg_%s_%s_mc("min(@0*@1/@2,1)", t_trg_pt_%s_%s_mc, t_trg_phieta_%s_%s_mc, t_trg_ave_phieta_%s_%s_mc)' % (wp, y, wp, y, wp, y, wp, y))

        w.factory('expr::t_trg_%s_%s_ratio("@0/@1", t_trg_%s_%s_data, t_trg_%s_%s_mc)' % (wp, y, wp, y, wp, y))


# now use the histograms to get the uncertainty variations
for wp in tau_id_wps:
  for dm in ['0','1','10']:
     histsToWrap = [
      ('ditau_%sMVAv2_dm%s_DATA_errorBand' % (wp,dm), 't_trg_uncert_%s_ditau_dm%s_data' % (wp,dm)),
      ('mutau_%sMVAv2_dm%s_DATA_errorBand' % (wp,dm), 't_trg_uncert_%s_mutau_dm%s_data' % (wp,dm)),
      ('etau_%sMVAv2_dm%s_DATA_errorBand' % (wp,dm), 't_trg_uncert_%s_etau_dm%s_data' % (wp,dm)),
      ('ditau_%sMVAv2_dm%s_MC_errorBand' % (wp,dm), 't_trg_uncert_%s_ditau_dm%s_mc' % (wp,dm)),
      ('mutau_%sMVAv2_dm%s_MC_errorBand' % (wp,dm), 't_trg_uncert_%s_mutau_dm%s_mc' % (wp,dm)),
      ('etau_%sMVAv2_dm%s_MC_errorBand' % (wp,dm), 't_trg_uncert_%s_etau_dm%s_mc' % (wp,dm))
    ]

     for task in histsToWrap:
       hist = tau_trg_file.Get(task[0])
       uncert_hists = wsptools.UncertsFromHist(hist) 
       wsptools.SafeWrapHist(w, ['t_pt'], uncert_hists[0], name=task[1]+'_up')
       wsptools.SafeWrapHist(w, ['t_pt'], uncert_hists[1], name=task[1]+'_down')

  for y in ['ditau','mutau','etau']:
    for x in ['data', 'mc']:
      w.factory('expr::t_trg_pt_uncert_%s_%s_%s_up("(@0==0)*@1 + (@0==1)*@2 + (@0>=3)*@3", t_dm[0], t_trg_uncert_%s_%s_dm0_%s_up, t_trg_uncert_%s_%s_dm1_%s_up, t_trg_uncert_%s_%s_dm10_%s_up)' % (wp, y, x, wp, y, x, wp, y, x, wp, y, x))
      w.factory('expr::t_trg_pt_uncert_%s_%s_%s_down("(@0==0)*@1 + (@0==1)*@2 + (@0>=3)*@3", t_dm[0], t_trg_uncert_%s_%s_dm0_%s_down, t_trg_uncert_%s_%s_dm1_%s_down, t_trg_uncert_%s_%s_dm10_%s_down)' % (wp, y, x, wp, y, x, wp, y, x, wp, y, x))

      w.factory('expr::t_trg_%s_%s_%s_up("min((@0+@1)*@2/@0,1)", t_trg_pt_%s_%s_%s, t_trg_pt_uncert_%s_%s_%s_up, t_trg_%s_%s_%s)' % (wp, y, x, wp, y, x, wp, y, x, wp, y, x))
      w.factory('expr::t_trg_%s_%s_%s_down("max((@0-@1)*@2/@0,0)", t_trg_pt_%s_%s_%s, t_trg_pt_uncert_%s_%s_%s_down, t_trg_%s_%s_%s)' % (wp, y, x, wp, y, x, wp, y, x, wp, y, x))

    w.factory('expr::t_trg_%s_%s_ratio_up("(sqrt(pow((@0-@1)/@1,2) + pow((@2-@3)/@3,2))+1.)*@4",t_trg_%s_%s_data_up, t_trg_%s_%s_data, t_trg_%s_%s_mc_up, t_trg_%s_%s_mc, t_trg_%s_%s_ratio)' % (wp, y, wp, y, wp, y, wp, y, wp, y, wp, y))

    w.factory('expr::t_trg_%s_%s_ratio_down("(1.-sqrt(pow((@1-@0)/@1,2) + pow((@3-@2)/@3,2)))*@4",t_trg_%s_%s_data_down, t_trg_%s_%s_data, t_trg_%s_%s_mc_down, t_trg_%s_%s_mc, t_trg_%s_%s_ratio)' % (wp, y, wp, y, wp, y, wp, y, wp, y, wp, y))

# differential tau ID SFs from tau POG

# dm binned SFs

loc='inputs/2016/TauPOGIDSFs/'

histsToWrap = [
  (loc+'/TauID_SF_dm_MVAoldDM2017v2_2016.root:VLoose', 't_id_dm_vloose'), 
  (loc+'/TauID_SF_dm_MVAoldDM2017v2_2016.root:Loose',  't_id_dm_loose'),
  (loc+'/TauID_SF_dm_MVAoldDM2017v2_2016.root:Medium', 't_id_dm_medium'),
  (loc+'/TauID_SF_dm_MVAoldDM2017v2_2016.root:Tight',  't_id_dm_tight'),
  (loc+'/TauID_SF_dm_MVAoldDM2017v2_2016.root:VTight', 't_id_dm_vtight'),
  (loc+'/TauID_SF_dm_MVAoldDM2017v2_2016.root:VVTight', 't_id_dm_vvtight')
]

w.factory('expr::t_dm_bounded("(@0<2)*@0 + (@0>2)*10" ,t_dm[0])')

for task in histsToWrap: 
  wsptools.SafeWrapHist(w, ['t_dm_bounded'], GetFromTFile(task[0]), name=task[1])
  uncert_hists = wsptools.UncertsFromHist(GetFromTFile(task[0]))
  wsptools.SafeWrapHist(w, ['t_dm_bounded'], uncert_hists[0], name=task[1]+'_abs_up')
  wsptools.SafeWrapHist(w, ['t_dm_bounded'], uncert_hists[1], name=task[1]+'_abs_down')
  w.factory('expr::%s_up("1.+@0/@1",%s_abs_up,%s)' % (task[1],task[1],task[1]))
  w.factory('expr::%s_down("1.-@0/@1",%s_abs_down,%s)' % (task[1],task[1],task[1]))

# pT dependent SFs

sf_funcs = {}

sf_funcs['vloose_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*1.0351641+ ( x > 25 && x <=30)*0.9901479+ ( x > 30 && x <=35)*0.9885759+ ( x > 35 && x <=40)*0.915416+ (x > 40 && x <=500)*1.03785416637+ (x > 500 && x <= 1000)*(0.994397720614 + 0.0434564457594*(x/500.))+ (x > 1000)*(0.994397720614 + 0.0869128915189)'
sf_funcs['vloose_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.7769241+ ( x > 25 && x <=30)*0.8708439+ ( x > 30 && x <=35)*0.8951739+ ( x > 35 && x <=40)*0.815878+ (x > 40 && x <= 500)*0.916727586761+ (x > 500 && x <= 1000)*(0.994397720614 - 0.0776701338527*(x/500.))+ (x > 1000)*(0.994397720614 - 0.155340267705)'
sf_funcs['loose'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.9455127+ ( x > 25 && x <=30)*0.8846971+ ( x > 30 && x <=35)*0.9378086+ ( x > 35 && x <=40)*0.9071475+ (x >40)*0.93317687081'
sf_funcs['loose_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*1.0379527+ ( x > 25 && x <=30)*0.9562731+ ( x > 30 && x <=35)*0.9732536+ ( x > 35 && x <=40)*0.9369315+ (x > 40 && x <= 500)*0.970668391301+ (x > 500 && x <= 1000)*(0.93317687081 + 0.0374915204912*(x/500.))+ (x > 1000)*(0.93317687081 + 0.0749830409824)'
sf_funcs['loose_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8530727+ ( x > 25 && x <=30)*0.8131211+ ( x > 30 && x <=35)*0.9023636+ ( x > 35 && x <=40)*0.8773635+ (x > 40 && x <= 500)*0.893490649713+ (x > 500 && x <= 1000)*(0.93317687081 - 0.0396862210967*(x/500.))+ (x > 1000)*(0.93317687081 - 0.0793724421934)'
sf_funcs['medium'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.9738206+ ( x > 25 && x <=30)*0.8908505+ ( x > 30 && x <=35)*0.9291307+ ( x > 35 && x <=40)*0.9109252+ (x >40)*0.89185502389'
sf_funcs['medium_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*1.0604636+ ( x > 25 && x <=30)*0.9352495+ ( x > 30 && x <=35)*0.9598017+ ( x > 35 && x <=40)*0.9377822+ (x > 40 && x <= 500)*0.922756928271+ (x > 500 && x <= 1000)*(0.89185502389 + 0.0309019043812*(x/500.))+ (x > 1000)*(0.89185502389 + 0.0618038087624)'
sf_funcs['medium_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8871776+ ( x > 25 && x <=30)*0.8464515+ ( x > 30 && x <=35)*0.8984597+ ( x > 35 && x <=40)*0.8840682+ (x > 40 && x <= 500)*0.862460980443+ (x > 500 && x <= 1000)*(0.89185502389 - 0.029394043447*(x/500.))+ (x > 1000)*(0.89185502389 - 0.058788086894)'
sf_funcs['tight'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.9378085+ ( x > 25 && x <=30)*0.9105335+ ( x > 30 && x <=35)*0.9130542+ ( x > 35 && x <=40)*0.896008+ (x >40)*0.928217208056'
sf_funcs['tight_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*1.0053955+ ( x > 25 && x <=30)*0.9501775+ ( x > 30 && x <=35)*0.9419702+ ( x > 35 && x <=40)*0.920895+ (x > 40 && x <=500)*0.965954742861+ (x > 500 && x <= 1000)*(0.928217208056 + 0.0377375348049*(x/500.))+ (x > 1000)*(0.928217208056 + 0.0754750696098)'
sf_funcs['tight_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8702215+ ( x > 25 && x <=30)*0.8708895+ ( x > 30 && x <=35)*0.8841382+ ( x > 35 && x <=40)*0.871121+ (x > 40 && x <= 500)*0.887186977688+ (x > 500 && x <= 1000)*(0.928217208056 - 0.041030230368*(x/500.))+ (x > 1000)*(0.928217208056 - 0.082060460736)'
sf_funcs['vtight'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.935252+ ( x > 25 && x <=30)*0.9029805+ ( x > 30 && x <=35)*0.8998639+ ( x > 35 && x <=40)*0.8812731+ (x >40)*0.949507022093'
sf_funcs['vtight_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.994107+ ( x > 25 && x <=30)*0.9357555+ ( x > 30 && x <=35)*0.9254669+ ( x > 35 && x <=40)*0.9055981+ (x > 40 && x <=500)*0.985309390622+ (x > 500 && x <= 1000)*(0.949507022093 + 0.035802368529*(x/500.))+ (x > 1000)*(0.949507022093 + 0.0716047370581)'
sf_funcs['vtight_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.876397+ ( x > 25 && x <=30)*0.8702055+ ( x > 30 && x <=35)*0.8742609+ ( x > 35 && x <=40)*0.8569481+ (x > 40 && x <=500)*0.900052228358+ (x > 500 && x <= 1000)*(0.949507022093 - 0.0494547937346*(x/500.))+ (x > 1000)*(0.949507022093 - 0.0989095874691)'
sf_funcs['vvtight'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.932887+ ( x > 25 && x <=30)*0.8966382+ ( x > 30 && x <=35)*0.9024921+ ( x > 35 && x <=40)*0.8745323+ (x >40)*0.907242313227'
sf_funcs['vvtight_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.978589+ ( x > 25 && x <=30)*0.9225292+ ( x > 30 && x <=35)*0.9255871+ ( x > 35 && x <=40)*0.8996693+ (x > 40 && x <=500)*0.945560083676+ (x > 500 && x <= 1000)*(0.907242313227 + 0.0383177704498*(x/500.))+ (x > 1000)*(0.907242313227 + 0.0766355408996)'
sf_funcs['vvtight_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.887185+ ( x > 25 && x <=30)*0.8707472+ ( x > 30 && x <=35)*0.8793971+ ( x > 35 && x <=40)*0.8493953+ (x > 40 && x <=500)*0.865580126851+ (x > 500 && x <= 1000)*(0.907242313227 - 0.0416621863752*(x/500.))+ (x > 1000)*(0.907242313227 - 0.0833243727504)'

import re
for x in sf_funcs:
  func = re.sub('x','@0',sf_funcs[x])
  w.factory('expr::t_id_pt_%s("%s",t_pt[0])' % (x, func))

# PRELIMINARY differential tau ID SFs for deepTau ID from Yuta

# dm binned SFs

loc='inputs/2016/TauPOGIDSFs/'

histsToWrap = [
  (loc+'/TauID_SF_dm_DeepTau2017v2_2016.root:VVVLoose', 't_deeptauid_dm_vvvloose'),
  (loc+'/TauID_SF_dm_DeepTau2017v2_2016.root:VVLoose',  't_deeptauid_dm_vvloose'),
  (loc+'/TauID_SF_dm_DeepTau2017v2_2016.root:VLoose',   't_deeptauid_dm_vloose'),
  (loc+'/TauID_SF_dm_DeepTau2017v2_2016.root:Loose',    't_deeptauid_dm_loose'),
  (loc+'/TauID_SF_dm_DeepTau2017v2_2016.root:Medium',   't_deeptauid_dm_medium'),
  (loc+'/TauID_SF_dm_DeepTau2017v2_2016.root:Tight',    't_deeptauid_dm_tight'),
  (loc+'/TauID_SF_dm_DeepTau2017v2_2016.root:VTight',   't_deeptauid_dm_vtight'),
  (loc+'/TauID_SF_dm_DeepTau2017v2_2016.root:VVTight',  't_deeptauid_dm_vvtight')
]

for task in histsToWrap:
  wsptools.SafeWrapHist(w, ['t_dm_bounded'], GetFromTFile(task[0]), name=task[1])
  uncert_hists = wsptools.UncertsFromHist(GetFromTFile(task[0]))
  wsptools.SafeWrapHist(w, ['t_dm_bounded'], uncert_hists[0], name=task[1]+'_abs_up')
  wsptools.SafeWrapHist(w, ['t_dm_bounded'], uncert_hists[1], name=task[1]+'_abs_down')
  w.factory('expr::%s_up("1.+@0/@1",%s_abs_up,%s)' % (task[1],task[1],task[1]))
  w.factory('expr::%s_down("1.-@0/@1",%s_abs_down,%s)' % (task[1],task[1],task[1]))

# pT dependent SFs

sf_funcs = {}
sf_funcs['vvvloose'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8894486+ ( x > 25 && x <=30)*0.9337315+ ( x > 30 && x <=35)*0.868918+ ( x > 35 && x <=40)*0.9164997+ (x >40)*0.911658476376'
sf_funcs['vvvloose_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*1.0701976+ ( x > 25 && x <=30)*1.1098135+ ( x > 30 && x <=35)*0.95326+ ( x > 35 && x <=40)*1.0465037+ (x > 40 && x <=500)*0.947729246985+ (x > 500 && x <= 1000)*(0.911658476376 + 0.036070770609*(x/500.))+ (x > 1000)*(0.911658476376 + 0.072141541218)'
sf_funcs['vvvloose_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.7086996+ ( x > 25 && x <=30)*0.7576495+ ( x > 30 && x <=35)*0.784576+ ( x > 35 && x <=40)*0.7864957+ (x > 40 && x <=500)*0.87566901777+ (x > 500 && x <= 1000)*(0.911658476376 - 0.0359894586064*(x/500.))+ (x > 1000)*(0.911658476376 - 0.0719789172128)'
sf_funcs['vvloose'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8413167+ ( x > 25 && x <=30)*0.8983791+ ( x > 30 && x <=35)*0.8636054+ ( x > 35 && x <=40)*0.9268016+ (x >40)*0.980853880905'
sf_funcs['vvloose_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*1.0203187+ ( x > 25 && x <=30)*1.0979131+ ( x > 30 && x <=35)*0.9259644+ ( x > 35 && x <=40)*1.0470576+ (x > 40 && x <=500)*1.02832264098+ (x > 500 && x <= 1000)*(0.980853880905 + 0.0474687600759*(x/500.))+ (x > 1000)*(0.980853880905 + 0.0949375201519)'
sf_funcs['vvloose_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.6623147+ ( x > 25 && x <=30)*0.6988451+ ( x > 30 && x <=35)*0.8012464+ ( x > 35 && x <=40)*0.8065456+ (x > 40 && x <=500)*0.926230667425+ (x > 500 && x <= 1000)*(0.980853880905 - 0.0546232134802*(x/500.))+ (x > 1000)*(0.980853880905 - 0.10924642696)'
sf_funcs['vloose'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8369484+ ( x > 25 && x <=30)*1.035287+ ( x > 30 && x <=35)*0.9369157+ ( x > 35 && x <=40)*0.9306706+ (x >40)*1.00908533907'
sf_funcs['vloose_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.9097164+ ( x > 25 && x <=30)*1.193655+ ( x > 30 && x <=35)*1.0377997+ ( x > 35 && x <=40)*1.0151396+ (x > 40 && x <=500)*1.04918519748+ (x > 500 && x <= 1000)*(1.00908533907 + 0.0400998584093*(x/500.))+ (x > 1000)*(1.00908533907 + 0.0801997168186)'
sf_funcs['vloose_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.7641804+ ( x > 25 && x <=30)*0.876919+ ( x > 30 && x <=35)*0.8360317+ ( x > 35 && x <=40)*0.8462016+ (x > 40 && x <=500)*0.95300310953+ (x > 500 && x <= 1000)*(1.00908533907 - 0.0560822295417*(x/500.))+ (x > 1000)*(1.00908533907 - 0.112164459083)'
sf_funcs['loose'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.9308471+ ( x > 25 && x <=30)*1.003229+ ( x > 30 && x <=35)*0.9678539+ ( x > 35 && x <=40)*0.9858704+ (x >40)*0.955958860685'
sf_funcs['loose_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*1.0678211+ ( x > 25 && x <=30)*1.106304+ ( x > 30 && x <=35)*1.0366559+ ( x > 35 && x <=40)*1.0375044+ (x > 40 && x <=500)*0.987048113163+ (x > 500 && x <= 1000)*(0.955958860685 + 0.0310892524782*(x/500.))+ (x > 1000)*(0.955958860685 + 0.0621785049565)'
sf_funcs['loose_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.7938731+ ( x > 25 && x <=30)*0.900154+ ( x > 30 && x <=35)*0.8990519+ ( x > 35 && x <=40)*0.9342364+ (x > 40 && x <=500)*0.928703281924+ (x > 500 && x <= 1000)*(0.955958860685 - 0.0272555787612*(x/500.))+ (x > 1000)*(0.955958860685 - 0.0545111575223)'
sf_funcs['medium'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.9520878+ ( x > 25 && x <=30)*0.9224484+ ( x > 30 && x <=35)*0.9114676+ ( x > 35 && x <=40)*0.9594463+ (x >40)*0.905346055645'
sf_funcs['medium_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*1.0295268+ ( x > 25 && x <=30)*1.0168824+ ( x > 30 && x <=35)*0.9349926+ ( x > 35 && x <=40)*1.0062033+ (x > 40 && x <=500)*0.948023407238+ (x > 500 && x <= 1000)*(0.905346055645 + 0.0426773515932*(x/500.))+ (x > 1000)*(0.905346055645 + 0.0853547031864)'
sf_funcs['medium_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8746488+ ( x > 25 && x <=30)*0.8280144+ ( x > 30 && x <=35)*0.8879426+ ( x > 35 && x <=40)*0.9126893+ (x > 40 && x <=500)*0.872336250599+ (x > 500 && x <= 1000)*(0.905346055645 - 0.0330098050462*(x/500.))+ (x > 1000)*(0.905346055645 - 0.0660196100925)'
sf_funcs['tight'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.9073559+ ( x > 25 && x <=30)*0.9692555+ ( x > 30 && x <=35)*0.8791896+ ( x > 35 && x <=40)*0.9511443+ (x >40)*0.892448024317'
sf_funcs['tight_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.9938669+ ( x > 25 && x <=30)*1.0678435+ ( x > 30 && x <=35)*0.9008826+ ( x > 35 && x <=40)*0.9951743+ (x > 40 && x <=500)*0.940803814505+ (x > 500 && x <= 1000)*(0.892448024317 + 0.0483557901887*(x/500.))+ (x > 1000)*(0.892448024317 + 0.0967115803774)'
sf_funcs['tight_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8208449+ ( x > 25 && x <=30)*0.8706675+ ( x > 30 && x <=35)*0.8574966+ ( x > 35 && x <=40)*0.9071143+ (x > 40 && x <=500)*0.854016666677+ (x > 500 && x <= 1000)*(0.892448024317 - 0.0384313576393*(x/500.))+ (x > 1000)*(0.892448024317 - 0.0768627152787)'
sf_funcs['vtight'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8758872+ ( x > 25 && x <=30)*0.9152035+ ( x > 30 && x <=35)*0.874832+ ( x > 35 && x <=40)*0.899913+ (x >40)*0.871494397918'
sf_funcs['vtight_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.9084352+ ( x > 25 && x <=30)*1.0830325+ ( x > 30 && x <=35)*0.923733+ ( x > 35 && x <=40)*0.966403+ (x > 40 && x <=500)*0.899744660517+ (x > 500 && x <= 1000)*(0.871494397918 + 0.028250262599*(x/500.))+ (x > 1000)*(0.871494397918 + 0.056500525198)'
sf_funcs['vtight_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8433392+ ( x > 25 && x <=30)*0.7473745+ ( x > 30 && x <=35)*0.825931+ ( x > 35 && x <=40)*0.833423+ (x > 40 && x <=500)*0.847077741701+ (x > 500 && x <= 1000)*(0.871494397918 - 0.0244166562174*(x/500.))+ (x > 1000)*(0.871494397918 - 0.0488333124348)'
sf_funcs['vvtight'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8852874+ ( x > 25 && x <=30)*0.8706893+ ( x > 30 && x <=35)*0.8362219+ ( x > 35 && x <=40)*0.8471247+ (x >40)*0.891124114465'
sf_funcs['vvtight_up'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.9598014+ ( x > 25 && x <=30)*0.9731673+ ( x > 30 && x <=35)*0.8638789+ ( x > 35 && x <=40)*0.8804427+ (x > 40 && x <=500)*0.942246532998+ (x > 500 && x <= 1000)*(0.891124114465 + 0.0511224185334*(x/500.))+ (x > 1000)*(0.891124114465 + 0.102244837067)'
sf_funcs['vvtight_down'] = '(x<=20)*0+ ( x > 20 && x <=25)*0.8107734+ ( x > 25 && x <=30)*0.7682113+ ( x > 30 && x <=35)*0.8085649+ ( x > 35 && x <=40)*0.8138067+ (x > 40 && x <=500)*0.835469026692+ (x > 500 && x <= 1000)*(0.891124114465 - 0.0556550877729*(x/500.))+ (x > 1000)*(0.891124114465 - 0.111310175546)'

for x in sf_funcs:
  func = re.sub('x','@0',sf_funcs[x])
  w.factory('expr::t_deeptauid_pt_%s("%s",t_pt[0])' % (x, func))

w.importClassCode('CrystalBallEfficiency')
w.Print()
w.writeToFile('output/htt_scalefactors_legacy_2016.root')
w.Delete()
