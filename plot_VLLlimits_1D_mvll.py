import re, optparse
import os.path,sys
import argparse
from math import *
# from ROOT import *
import ROOT
from array import array
ROOT.gROOT.SetBatch(True)

def seq(start, stop, step=1):
	n = int(round((stop - start)/float(step)))
	if n > 1:
		return([start + step*i for i in range(n+1)])
	elif n == 1:
		return([start])
	else:
		return([])

#####
def redrawBorder():
   # this little macro redraws the axis tick marks and the pad border lines.
   ROOT.gPad.Update();
   ROOT.gPad.RedrawAxis();
   l = ROOT.TLine()
   l.SetLineWidth(3)
   l.DrawLine(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin());
   l.DrawLine(ROOT.gPad.GetUxmax(), 0.0001, ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax());
   l.DrawLine(ROOT.gPad.GetUxmin(), 0.0001, ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymax());
   l.DrawLine(ROOT.gPad.GetUxmin(), 0.0001, ROOT.gPad.GetUxmax(), 0.0001);

def getVals(fname):
	fIn = ROOT.TFile.Open(fname)
	tIn = fIn.Get('limit')
	if tIn.GetEntries() != 5:
		print "*** WARNING: cannot parse file", fname, "because nentries != 6"
		raise RuntimeError('cannot parse file')
	vals = []
	for i in range(0, tIn.GetEntries()):
		tIn.GetEntry(i)
		qe = tIn.quantileExpected
		lim = tIn.limit
		vals.append((qe,lim))
	return vals

################################################################################################
###########OPTIONS
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--version', dest='version',help='version', required = True)
parser.add_argument('--ctau', dest='ctau',help='ctau', required = True)
parser.add_argument('--categ',    dest='categ', action='store_true', help='Do signal')
args = parser.parse_args()
###########
###CREATE TAGS
ctau   = args.ctau
categ  = args.categ
version= args.version

#Plot it
c1 = ROOT.TCanvas("c1", "c1", 1300, 1000)
c1.SetFrameLineWidth(3)
c1.SetBottomMargin (0.15)
c1.SetRightMargin (0.05)
c1.SetLeftMargin (0.15)
c1.SetGridx()
c1.SetGridy()

mg = ROOT.TMultiGraph()
gr2sigma = ROOT.TGraphAsymmErrors()
gr1sigma = ROOT.TGraphAsymmErrors()
grexp = ROOT.TGraph()
grobs = ROOT.TGraph()
grexp_csc = ROOT.TGraph()
grexp_dt  = ROOT.TGraph()

#coupling_xs  = []
#coupling_xs2 = []

masses         = [300, 700, 1000]
xsections      = [0.01927,  0.00044, 0.00006]

#Get XS predicted for vll vs mass
n  = 8
x  = array('d', [300,400,500,600,700,800,900,1000])
y  = array('d', [0.01927,0.00720*(0.01927/0.0229),0.00274*(0.01927/0.0229),0.00119*(0.01927/0.0229), 0.00044,0.000277*(0.01927/0.0229),0.000145*(0.01927/0.0229),0.00006])

##print coupling_xs
ptsList = [] 

#fill out the arrays for limits
for k in range(0, len(masses) ):
	fname = "datacards_%s/cards_%i_%s/higgsCombine_%i_%s.AsymptoticLimits.mH120.root"%(version,masses[k],ctau,masses[k],ctau)
	vals  = getVals(fname)
	xs    = xsections[k]
	obs   = 0.0 ## FIXME
	m2s_t = vals[0][1]*xs
	m1s_t = vals[1][1]*xs
	exp   = vals[2][1]*xs
	p1s_t = vals[3][1]*xs
	p2s_t = vals[4][1]*xs

	## because the other code wants +/ sigma vars as deviations, without sign, from the centeal exp value...
	p2s  = p2s_t - exp
	p1s  = p1s_t - exp
	m2s  = exp - m2s_t
	m1s  = exp - m1s_t
	xval = masses[k]
	ptsList.append((xval, obs, exp, p2s, p1s, m1s, m2s))
ptsList.sort()
for ipt, pt in enumerate(ptsList):
	xval = pt[0]
	obs  = pt[1]
	exp  = pt[2]
	p2s  = pt[3]
	p1s  = pt[4]
	m1s  = pt[5]
	m2s  = pt[6]
	grexp.SetPoint(ipt, xval, exp)
	grobs.SetPoint(ipt, xval, obs)
	gr1sigma.SetPoint(ipt, xval, exp)
	gr2sigma.SetPoint(ipt, xval, exp)
	gr1sigma.SetPointError(ipt, 0,0,m1s,p1s)
	gr2sigma.SetPointError(ipt, 0,0,m2s,p2s)

if categ==True:
	ptsList_csc = []
	ptsList_dt  = []
	#CSC fill
	for j in range(0, len(masses) ):
		fname = "datacards_%s/cards_%s_%s/VLLModel_CSCB/higgsCombine_%s_%s.AsymptoticLimits.mH120.root"%(version,masses[j],ctau,masses[j],ctau)
		vals  = getVals(fname)
		xs    = xsections[j]
		obs   = 0.0 ## FIXME
		m2s_t = vals[0][1]*xs
		m1s_t = vals[1][1]*xs
		exp   = vals[2][1]*xs
		p1s_t = vals[3][1]*xs
		p2s_t = vals[4][1]*xs
		## because the other code wants +/ sigma vars as deviations, without sign, from the centeal exp value...
		p2s  = p2s_t - exp
		p1s  = p1s_t - exp
		m2s  = exp - m2s_t
		m1s  = exp - m1s_t
		xval = masses[j]
		ptsList_csc.append((xval, obs, exp, p2s, p1s, m1s, m2s))    
	ptsList_csc.sort()
	for ipt, pt in enumerate(ptsList_csc):
		xval = pt[0]
		exp  = pt[2]
		grexp_csc.SetPoint(ipt, xval, exp)
	#DT fill
	for k in range(0, len(masses) ):
		fname = "datacards_%s/cards_%s_%s/VLLModel_DTB/higgsCombine_%s_%s.AsymptoticLimits.mH120.root"%(version,masses[k],ctau,masses[k],ctau)
		vals  = getVals(fname)
		xs    = xsections[k]
		obs   = 0.0 ## FIXME
		m2s_t = vals[0][1]*xs
		m1s_t = vals[1][1]*xs
		exp   = vals[2][1]*xs
		p1s_t = vals[3][1]*xs
		p2s_t = vals[4][1]*xs
		## because the other code wants +/ sigma vars as deviations, without sign, from the centeal exp value...
		p2s  = p2s_t - exp
		p1s  = p1s_t - exp
		m2s  = exp - m2s_t
		m1s  = exp - m1s_t
		xval = masses[k]
		ptsList_dt.append((xval, obs, exp, p2s, p1s, m1s, m2s))    
	ptsList_dt.sort()
	for ipt, pt in enumerate(ptsList_dt):
		xval = pt[0]
		exp  = pt[2]
		grexp_dt.SetPoint(ipt, xval, exp)
	#set styles
	grexp_csc.SetMarkerStyle(24)
	grexp_csc.SetMarkerColor(4)
	grexp_csc.SetMarkerSize(0.8)
	grexp_csc.SetLineColor(ROOT.kRed+2)
	grexp_csc.SetLineWidth(3)
	grexp_csc.SetLineStyle(2)
	grexp_csc.SetFillColor(0) 
	grexp_dt.SetMarkerStyle(24)
	grexp_dt.SetMarkerColor(4)
	grexp_dt.SetMarkerSize(0.8)
	grexp_dt.SetLineColor(ROOT.kGreen+2)
	grexp_dt.SetLineWidth(3)
	grexp_dt.SetLineStyle(2)
	grexp_dt.SetFillColor(0) 

######## set styles
grexp.SetMarkerStyle(24)
grexp.SetMarkerColor(4)
grexp.SetMarkerSize(0.8)
grexp.SetLineColor(ROOT.kBlue+2)
grexp.SetLineWidth(3)
grexp.SetLineStyle(2)
grexp.SetFillColor(0)
grobs.SetLineColor(1)
grobs.SetLineWidth(3)
grobs.SetMarkerColor(1)
grobs.SetMarkerStyle(20)
grobs.SetFillStyle(0)
gr1sigma.SetMarkerStyle(0)
gr1sigma.SetMarkerColor(3)
gr1sigma.SetFillColor(ROOT.kGreen+1)
gr1sigma.SetLineColor(ROOT.kGreen+1)
gr1sigma.SetFillStyle(1001)
gr2sigma.SetMarkerStyle(0)
gr2sigma.SetMarkerColor(5)
gr2sigma.SetFillColor(ROOT.kOrange)
gr2sigma.SetLineColor(ROOT.kOrange)
gr2sigma.SetFillStyle(1001)

###########
legend = ROOT.TLegend(0,0,0,0)
legend.SetFillColor(ROOT.kWhite)
legend.SetBorderSize(0)
# legend
if categ==True:
   legend.SetX1(0.17284)
   legend.SetY1(0.730526)
   legend.SetX2(0.520062)
   legend.SetY2(0.88)
   legend.SetHeader('95% CL median expected upper limts')
   legend.AddEntry(grexp_csc, "CSC Category", "l")
   legend.AddEntry(grexp_dt, "DT Category", "l")
   legend.AddEntry(grexp, "Combination", "l")
   fakePlot3 = ROOT.TGraphAsymmErrors()
   fakePlot3.SetFillColor(6)
   fakePlot3.SetFillStyle(3001)
   fakePlot3.SetLineColor(6)
   fakePlot3.SetLineWidth(3)
   legend.AddEntry(fakePlot3, "Theoretical prediction", "l")
else:
   legend.SetX1(0.17284)
   legend.SetY1(0.630526+0.05)
   legend.SetX2(0.520062)
   legend.SetY2(0.88)
   legend.SetHeader('95% CL upper limits')
   legend.AddEntry(grexp, "Median expected", "l")
   legend.AddEntry(gr1sigma, "68% expected", "f")
   legend.AddEntry(gr2sigma, "95% expected", "f")
   fakePlot3 = ROOT.TGraphAsymmErrors()
   fakePlot3.SetFillColor(6)
   fakePlot3.SetFillStyle(3001)
   fakePlot3.SetLineColor(6)
   fakePlot3.SetLineWidth(3)
   legend.AddEntry(fakePlot3, "Theoretical prediction", "l")

##### text
pt = ROOT.TPaveText(0.1663218-0.02,0.886316,0.3045977-0.02,0.978947,"brNDC")
pt.SetBorderSize(0)
pt.SetTextAlign(12)
pt.SetTextFont(62)
pt.SetTextSize(0.05)
pt.SetFillColor(0)
pt.SetFillStyle(0)
pt.AddText("CMS #font[52]{Preliminary}")

pt2 = ROOT.TPaveText(0.70,0.9066667,0.8997773,0.957037,"brNDC")
pt2.SetBorderSize(0)
pt2.SetFillColor(0)
pt2.SetTextSize(0.040)
pt2.SetTextFont(42)
pt2.SetFillStyle(0)
pt2.AddText("          138 fb^{-1} (13 TeV)")

pt4 = ROOT.TPaveText(0.6819196+0.036,0.7180357+0.015+0.02-0.05,0.9008929+0.036,0.8075595+0.015,"brNDC")
pt4.SetTextAlign(12)
pt4.SetFillColor(ROOT.kWhite)
pt4.SetFillStyle(1001)
pt4.SetTextFont(42)
pt4.SetTextSize(0.05)
pt4.SetBorderSize(0)
pt4.SetTextAlign(32)
pt4.AddText("")
pt4.AddText("m_{a} = 10 GeV")
pt4.AddText("")
pt4.AddText("c#tau_{a}= %.2f m"%(float(ctau)/1000) )  

pt5 = ROOT.TPaveText(0.4819196+0.036,0.7780357+0.015+0.02,0.9008929+0.036,0.8675595+0.015,"brNDC")
pt5.SetTextAlign(12)
pt5.SetFillColor(ROOT.kWhite)
pt5.SetFillStyle(1001)
pt5.SetTextFont(42)
pt5.SetTextSize(0.05)
pt5.SetBorderSize(0)
pt5.SetTextAlign(32)
pt5.AddText("CSC+DT Combination")

th = ROOT.TGraph( n, x, y )
th.SetFillColor(6)
th.SetFillStyle(3001)
th.SetLineColor(6)
th.SetLineWidth(3)

hframe = ROOT.TH1F('hframe', '', 100, 300, 1000)
hframe.SetMinimum(0.0001)
hframe.SetMaximum(10)
hframe.GetYaxis().SetTitleSize(0.047)
hframe.GetXaxis().SetTitleSize(0.055)
hframe.GetYaxis().SetLabelSize(0.045)
hframe.GetXaxis().SetLabelSize(0.045)
hframe.GetXaxis().SetLabelOffset(0.012)
hframe.GetYaxis().SetTitleOffset(1.4)
hframe.GetXaxis().SetTitleOffset(1.1)
hframe.GetYaxis().SetNdivisions(505)
hframe.GetYaxis().SetTitle("#sigma [pb]")
hframe.GetXaxis().SetTitle("m_{VLL} [GeV]")

hframe.SetStats(0)
ROOT.gPad.SetTicky()
ROOT.gPad.SetLogy()
hframe.Draw()
if categ==True:
  grexp.Draw("L same")
  grexp_csc.Draw("L same")
  grexp_dt.Draw("L same")
  th.Draw( 'l same' )
  pt.Draw()
  pt2.Draw()
  pt4.Draw()
else:
  gr2sigma.Draw("3same")
  gr1sigma.Draw("3same")
  grexp.Draw("Lsame")
  th.Draw( 'l same' )
  pt.Draw()
  pt2.Draw()
  pt4.Draw()
  pt5.Draw()
redrawBorder()
c1.Update()
legend.Draw()
c1.Update()
if categ==True:
   c1.SaveAs("plots_%s/vlllimits_vs_mvll/vlllimits_vs_mvll_%s_categ.pdf"%(version,ctau)  )
else:
   c1.SaveAs("plots_%s/vlllimits_vs_mvll/vlllimits_vs_mvll_%s.pdf"%(version,ctau) )
