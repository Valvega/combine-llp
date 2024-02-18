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
   #l.DrawLine(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin());
   #l.DrawLine(ROOT.gPad.GetUxmax(), 0.01, ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax());
   #l.DrawLine(ROOT.gPad.GetUxmin(), 0.01, ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymax());
   #l.DrawLine(ROOT.gPad.GetUxmin(), 0.01, ROOT.gPad.GetUxmax(), 0.01);

   l.DrawLine(0.01, 0.00001, 10, 0.00001);
   l.DrawLine(0.01, 10, 10, 10);
   l.DrawLine(0.01, 0.00001, 0.01, 10);
   l.DrawLine(10, 0.00001, 10, 10);

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
args = parser.parse_args()
version= args.version
###########


#Plot it
c1 = ROOT.TCanvas("c1", "c1", 1300, 1300)
c1.SetFrameLineWidth(3)
c1.SetBottomMargin (0.10)
c1.SetRightMargin (0.05)
c1.SetLeftMargin (0.20)
#c1.SetGridx()
#c1.SetGridy()

mg = ROOT.TMultiGraph()
gr2sigma = ROOT.TGraphAsymmErrors()
gr1sigma = ROOT.TGraphAsymmErrors()
grexp = ROOT.TGraph()
grobs = ROOT.TGraph()


#coupling_xs  = []
#coupling_xs2 = []
#2d+
#n2p  = 10
#y2p  = array('d', [0.040, 0.03, 0.08, 0.1, 0.3, 0.8, 1.0, 3.0, 8.0, 10.0])
#x2p  = array('d', [  300,  260,  440, 450, 440, 380, 360, 280, 250,  240])
#1d+
#n1p  = 10
#y1p  = array('d', [0.027, 0.03, 0.08, 0.1, 0.3, 0.8, 1.0, 3.0, 8.0, 10.0])
#x1p  = array('d', [  300,  350,  560, 570, 520, 440, 420, 330, 280,  270])
#median
#n    = 10
#y    = array('d', [0.022, 0.03, 0.08, 0.1, 0.3, 0.8, 1.0, 3.0, 8.0, 10.0])
#x    = array('d', [  300,  470,  710, 720, 630, 530, 500, 390, 330,  320])
#1n+
#n1n  = 10
#y1n  = array('d', [0.018, 0.03, 0.08, 0.1, 0.3, 0.8, 1.0, 3.0, 8.0, 10.0])
#x1n  = array('d', [  300,  690,  800, 805, 730, 630, 600, 460, 390,  380])
#2n+
#n2n  = 10
#y2n  = array('d', [0.015, 0.03, 0.08, 0.1, 0.3, 0.8, 1.0, 3.0, 8.0, 10.0])
#x2n  = array('d', [  300,  790,  880, 885, 800, 710, 680, 510, 440,  430])

#n  = 8
#y  = array('d', [0.022,0.03,0.08, 0.1, 0.3, 0.8, 1.0,10.0])
#x  = array('d', [300, 500, 710, 720, 650, 540, 520, 300])

xvalues = [
   0.02,
   0.03,
   0.08,
   0.10,
   0.20,
   0.30,
   0.80,
   1.00,
   2.00,
   3.00,
   8.00,
   10.0,
]

#v4
#yvalues = [
#    [100,200,300,420,600], #0.02
#    [250,350,470,690,790], #0.03
#    [440,560,710,800,880], #0.08
#    [450,570,720,805,885], #0.10
#    [445,550,680,770,840], #0.20
#    [440,520,650,750,810], #0.30
#    [380,440,530,630,710], #0.80
#    [360,420,500,600,680], #1.00
#    [310,360,430,500,560], #2.00
#    [280,330,390,460,520], #3.00
#    [250,280,330,390,450], #8.00
#    [240,270,320,380,430],#10.00
#]

##v5
#yvalues = [
#    [100,200,310,440,700], #0.02
#    [280,360,510,730,830], #0.03
#    [460,580,740,840,905], #0.08
#    [470,600,750,830,910], #0.10
#    [465,580,720,800,870], #0.20
#    [450,560,690,770,820], #0.30
#    [380,460,550,680,730], #0.80
#    [360,440,520,630,700], #1.00
#    [310,370,440,520,590], #2.00
#    [280,340,400,470,540], #3.00
#    [250,280,340,400,460], #8.00
#    [240,270,330,390,450],#10.00
#]

#v6
#yvalues = [
#    [160,190,260,290,380], #0.02
#    [250,280,350,500,730], #0.03
#    [380,480,660,750,840], #0.08
#    [390,490,670,770,850], #0.10
#    [385,480,640,740,800], #0.20
#    [380,470,590,710,770], #0.30
#    [330,390,470,560,650], #0.80
#    [310,370,440,530,600], #1.00
#    [250,310,370,440,500], #2.00
#    [210,280,340,390,460], #3.00
#    [180,240,290,340,380], #8.00
#    [160,210,270,330,370],#10.00
#]

yvalues = [
    [100,200,260,320,440], #0.02
    [250,350,400,560,740], #0.03
    [380,490,670,770,850], #0.08
    [400,520,680,780,850], #0.10
    [420,510,660,760,820], #0.20
    [400,480,620,730,780], #0.30
    [340,390,470,570,650], #0.80
    [320,370,450,530,620], #1.00
    [250,310,370,440,500], #2.00
    [220,280,340,400,460], #3.00
    [190,250,300,340,380], #8.00
    [170,220,260,330,370],#10.00
]


##print coupling_xs
ptsList = [] 

#fill out the arrays for limits
for k in range(0, len(xvalues) ):
	xs    = xvalues[k]
	obs   = 0.0 ## FIXME
	m2s_t = yvalues[k][0]
	m1s_t = yvalues[k][1]
	exp   = yvalues[k][2]
	p1s_t = yvalues[k][3]
	p2s_t = yvalues[k][4]
	## because the other code wants +/ sigma vars as deviations, without sign, from the centeal exp value...
	p2s  = p2s_t - exp
	p1s  = p1s_t - exp
	m2s  = exp - m2s_t
	m1s  = exp - m1s_t
	xval = xvalues[k]
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

mg.Add(gr2sigma, "3")
mg.Add(gr1sigma, "3")
mg.Add(grexp, "L")
mg.Add(grobs, "L")

##### text
pt = ROOT.TPaveText(0.1663218+0.04,0.886316-0.02,0.3045977,0.978947,"brNDC")
pt.SetBorderSize(0)
pt.SetTextAlign(12)
pt.SetTextFont(62)
pt.SetTextSize(0.05)
pt.SetFillColor(0)
pt.SetFillStyle(0)
pt.AddText("CMS #font[52]{Preliminary}")

pt2 = ROOT.TPaveText(0.70-0.06,0.9066667-0.02,0.8997773,0.957037,"brNDC")
pt2.SetBorderSize(0)
pt2.SetFillColor(0)
pt2.SetTextSize(0.040)
pt2.SetTextFont(42)
pt2.SetFillStyle(0)
pt2.AddText("          138 fb^{-1} (13 TeV)")

pt4 = ROOT.TPaveText(0.23,0.84,0.45,0.87,"brNDC")
pt4.SetTextAlign(12)
pt4.SetFillColor(ROOT.kWhite)
pt4.SetFillStyle(1001)
pt4.SetTextFont(42)
pt4.SetTextSize(0.040)
pt4.SetBorderSize(0)
#pt4.SetTextAlign(32)
pt4.AddText("")
pt4.AddText("m_{LLP} = 10 GeV")
#pt4.AddText("")
#pt4.AddText("c#tau_{a}= %.2f m"%(float(ctau)/1000) )  

pt5 = ROOT.TPaveText(0.4819196+0.036+0.04,0.7780357+0.015+0.05,0.9008929+0.036-0.02,0.8675595+0.017,"brNDC")
pt5.SetTextAlign(12)
pt5.SetFillColor(ROOT.kWhite)
pt5.SetFillStyle(1001)
pt5.SetTextFont(42)
pt5.SetTextSize(0.040)
pt5.SetBorderSize(0)
pt5.SetTextAlign(32)
pt5.AddText("CSC+DT Combination")

#th_2p = ROOT.TGraph( n2p, x2p, y2p )
#th_2p.SetFillColor(ROOT.kWhite)
#th_2p.SetFillStyle(3001)
#th_2p.SetLineColor(ROOT.kGreen+1)
#th_2p.SetLineWidth(3)
##th_2p.SetLineStyle(2)

#th_1p = ROOT.TGraph( n1p, x1p, y1p )
#th_1p.SetFillColor(ROOT.kWhite)
#th_1p.SetFillStyle(3001)
#th_1p.SetLineColor(ROOT.kGreen+2)
#th_1p.SetLineWidth(3)
#th_1p.SetLineStyle(2)

#th = ROOT.TGraph( n, x, y )
#th.SetFillColor(ROOT.kBlue)
#th.SetFillStyle(3004) #3001
#th.SetLineColor(ROOT.kGreen+2)
#th.SetLineWidth(3)
##th.SetLineWidth(+7002)
##th.SetLineStyle(3)

#th_1n = ROOT.TGraph( n1n, x1n, y1n )
#th_1n.SetFillColor(ROOT.kWhite)
#th_1n.SetFillStyle(3001)
#th_1n.SetLineColor(ROOT.kGreen+2)
#th_1n.SetLineWidth(3)
#th_1n.SetLineStyle(2)

#th_2n = ROOT.TGraph( n2n, x2n, y2n )
#th_2n.SetFillColor(6)
#th_2n.SetFillStyle(3001)
#th_2n.SetLineColor(ROOT.kWhite)
#th_2n.SetLineWidth(3)
##th_2n.SetLineStyle(2)

###########
legend = ROOT.TLegend(0,0,0,0)
legend.SetX1(0.56)
legend.SetY1(0.55+0.12)
legend.SetX2(0.75)
legend.SetY2(0.72+0.12)
legend.SetTextSize(0.040)
legend.SetFillColor(ROOT.kWhite)
legend.SetBorderSize(0)
# legend
legend.SetHeader('95% CL limits')
legend.AddEntry(grexp, "Expected", "l")
legend.AddEntry(gr1sigma, "Expected #pm 1 s.d.", "f")
legend.AddEntry(gr2sigma, "Expected #pm 2 s.d.", "f")

hframe = ROOT.TH1F('hframe', '', 100, 0.02, 10)
hframe.SetMinimum(300)
hframe.SetMaximum(1000)
hframe.GetYaxis().SetTitleSize(0.055)
hframe.GetXaxis().SetTitleSize(0.055)
hframe.GetYaxis().SetLabelSize(0.045)
hframe.GetXaxis().SetLabelSize(0.045)
hframe.GetXaxis().SetLabelOffset(-0.015)
hframe.GetYaxis().SetTitleOffset(1.5)
hframe.GetXaxis().SetTitleOffset(0.8)
#hframe.GetYaxis().SetNdivisions(505)
hframe.GetYaxis().SetTitle("m_{VLL} [GeV]")
hframe.GetXaxis().SetTitle("c#tau [m]")
hframe.SetStats(0)
ROOT.gPad.SetTicky()
#ROOT.gPad.SetLogy()
ROOT.gPad.SetLogx()
hframe.Draw()
gr2sigma.Draw("3same")
gr1sigma.Draw("3same")
grexp.Draw("Lsame")
#th.Draw( 'l same' )
#th_2p.Draw( 'l same' )
#th_1p.Draw( 'l same' )
#th_2n.Draw( 'l same' )
#th_1n.Draw( 'l same' )
#grobs.Draw("Lsame")
pt.Draw()
pt2.Draw()
redrawBorder()
c1.Update()
c1.RedrawAxis("g")
legend.Draw()
#pt3.Draw()
pt4.Draw()
#pt6.Draw()
pt5.Draw()
c1.Update()
c1.SaveAs("plots_%s/vlllimits_vs_mvll_ctau/vlllimits_2d.pdf"%version)
