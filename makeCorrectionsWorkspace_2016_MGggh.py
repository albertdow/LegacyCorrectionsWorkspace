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

# correction for quark mass dependence to ggH
wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/quarkmass_uncerts_hnnlo.root:nom'), 'ggH_quarkmass_hist')
w.factory('expr::ggH_quarkmass_corr("1.006*@0", ggH_quarkmass_hist)') # the constant factor is to ensure the normalization doesn't change - it is sample specific

wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/quarkmass_uncerts_hnnlo.root:up'), 'ggH_quarkmass_hist_up')
w.factory('expr::ggH_quarkmass_corr_up("1.006*@0", ggH_quarkmass_hist_up)')
wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/quarkmass_uncerts_hnnlo.root:down'), 'ggH_quarkmass_hist_down')
w.factory('expr::ggH_quarkmass_corr_down("1.006*@0", ggH_quarkmass_hist_down)')

wsptools.SafeWrapHist(w, ['HpT'],  GetFromTFile('inputs/ICSF/ggH/top_mass_weights.root:pt_weight'), 'ggH_fullquarkmass_hist')
w.factory('expr::ggH_fullquarkmass_corr("0.985*@0", ggH_fullquarkmass_hist)') # the constant factor is to ensure the normalization doesn't change - it is sample specific


loc = 'inputs/ICSF/ggH/MG_ps_uncerts.root:'
histsToWrap = [
    (loc + 'ps_0jet_up', 'ps_0jet_up'),
    (loc + 'ps_0jet_down', 'ps_0jet_down'),
    (loc + 'ps_1jet_up', 'ps_1jet_up'),
    (loc + 'ps_1jet_down', 'ps_1jet_down'),
    (loc + 'ps_2jet_up', 'ps_2jet_up'),
    (loc + 'ps_2jet_down', 'ps_2jet_down'),
    (loc + 'ps_3jet_up', 'ps_3jet_up'),
    (loc + 'ps_3jet_down', 'ps_3jet_down')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['HpT'],
                          GetFromTFile(task[0]), name=task[1])

for shift in ['up', 'down']:
  wsptools.MakeBinnedCategoryFuncMap(w, 'ngenjets', [0, 1, 2, 3, 1000],
                                     'ggH_mg_ps_%s' % shift, ['ps_0jet_%s' % shift, 'ps_1jet_%s' % shift, 'ps_2jet_%s' % shift, 'ps_3jet_%s' % shift])


histsToWrap = [
    (loc + 'ue_up', 'ggH_mg_ue_up'),
    (loc + 'ue_down', 'ggH_mg_ue_down')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['ngenjets'],
                          GetFromTFile(task[0]), name=task[1])

w.importClassCode('CrystalBallEfficiency')

w.Print()
w.writeToFile('htt_scalefactors_2016_MGggh.root')
w.Delete()
