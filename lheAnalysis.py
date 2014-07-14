#!/usr/bin/env python

from xml.dom.minidom import parse
import sys, os

from ROOT import *
from array import array

lheFileName = sys.argv[1]
rootFileName = sys.argv[2]

lheFile = parse(lheFileName)
rootFile = TFile(rootFileName, "RECREATE")

gROOT.ProcessLine(".x rootlogon.C")

## Analysis histograms
hNTquark = TH1F("hNTquark", "Top quark;Multiplicity;Events", 15, 0, 15)
hNBquark = TH1F("hNBquark", "Bottom quark;Multiplicity;Events", 15, 0, 15)
hNLquark = TH1F("hNLquark", "Light quarks;Multiplicity;Events", 15, 0, 15)
hNGluons = TH1F("hNGluons", "Gluons;Multiplicity;Events", 15, 0, 15)
hNLepton = TH1F("hNLepton", "Leptons;Multiplicity;Events", 15, 0, 15)
hNHquark = TH1F("hNHquark", "Heavy quark;Multiplicity;Events", 15, 0, 15)
hNJets = TH1F("hNJets", "All jets;Multiplicity;Events", 15, 0, 15)
hNPhoton = TH1F("hNPhoton", "Photons;Multiplicity;Events", 15, 0, 15)
hNHiggs = TH1F("hNHiggs", "Higgs;Multiplicity;Events", 15, 0, 15)
hNOthers = TH1F("hNOthers", "The others;Multiplicity;Events", 15, 0, 15)
hNTquarkVsNBquark = TH2F("hNTquarkVsNBquark", "Top vs Bottom;Top quark multiplicity;Bottom quark multiplicity", 15, 0, 15, 15, 0, 15)
hNTRemnant = TH1F("hNTRemnant","Remnant Top;Multiplicity;Events",15,0,15)
hNTHawking = TH1F("hNTHawking","Hawking Top;Multiplicity;Events",15,0,15)
hNTopFrame = TH1F("RS 14TeV all","Top quark;Multiplicity;Events",15,0,15)

hEnergy = TH1F("hEnergy","Energy;Energy (GeV);Candidates per 100GeV/c", 50, 0, 10)

hNSpinFrame = TH1F("hNSpinFrame","Spin Multiplicity;Multiplicity;Events",15,0,15)
hNScalar = TH1F("hNScalar","Scalar Multiplicity;Multiplicity;Events",15,0,15)
hNSpinor = TH1F("hNSpinor","Spinor Multiplicity;Multiplicity;Events",15,0,15)
hNVector = TH1F("hNVector","Vector Multiplicity;Multiplicity;Events",15,0,15)

hBhIniMass = TH1F("hBhIniMass","BH Mass;GeV/c^{2};Events", 100, 5000, 10000)

hSt  = TH1F("hSt" , "Scalar sum of transverse momentum;S_{T} (GeV/c);Events per 150GeV/c", 150, 0, 15000)
hPt  = TH1F("hPt" , "Transverse momentum;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 5000)
hEta = TH1F("hEta", "Pseudorapidity;Pseudorapidity #eta;Candidates", 150, -3, 3)
hMET = TH1F("hMET", "Missing E_{T};Missing transverse momentum;Events per 10GeV/c", 50, 0, 500)

hPtTquark = TH1F("hPtTquark", "Top quarks;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 5000)
hPtBquark = TH1F("hPtBquark", "Bottom quarks;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 5000)
hPtLquark = TH1F("hPtLquark", "Light quarks;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 5000)
hPtPhoton = TH1F("hPtPhoton", "Photons;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 5000)
hPtGluons = TH1F("hPtGluons", "Gluons;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 5000)
hPtLepton = TH1F("hPtLepton", "Lepton;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 5000)
hPtOthers = TH1F("hPtOthers", "Others;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 5000)
hPtHiggs = TH1F("hPtHiggs", "Higgs;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 5000)

hPtSpinFrame = TH1F("hPtSpinFrame", "Spin;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 3000)
hPtScalar = TH1F("hPtScalar", "Scalar;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 3000)
hPtSpinor = TH1F("hPtSpinor", "Spinor;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 3000)
hPtVector = TH1F("hPtVector", "Vector;Transverse momentum p_{T} (GeV/c);Candidates per 150GeV/c", 50, 0, 3000)

def fill(hist, value):
    valueUp = hist.GetXaxis().GetXmax()
    binWidth = hist.GetXaxis().GetBinWidth(hist.GetNbinsX()-1)
    hist.Fill(min(value, valueUp-binWidth*1e-9))

## Load init info
event = 0
for eventNode in lheFile.getElementsByTagName("event"):

    eventTexts = eventNode.childNodes[0].nodeValue.strip().split('\n')

    info = eventTexts[0].strip().split()
    if len(info)==7:
        n, proc = int(info[0]), int(info[1])        
        weight, qscale, mjmass = float(info[2]), float(info[3]), float(info[4])
        aqed, aqcd = float(info[5]), float(info[6])
        hBhIniMass.Fill(mjmass)
    elif len(info)==6:
        n, proc = int(info[0]), int(info[1])        
        weight, qscale = float(info[2]), float(info[3]) 
        aqed, aqcd = float(info[4]), float(info[5])


    event += 1

    st = 0.
    met = 0.
    nJets = 0
    nTquark, nBquark, nLquark = 0, 0, 0
    nGluons, nLepton, nPhoton, nOthers, nHiggs = 0, 0, 0, 0, 0
    nTopHawking, nTopRemnant = 0, 0
    nScalar, nSpinor, nVector = 0, 0, 0
    for i in range(n):
        pline = eventTexts[i+1].strip()
        if pline == "" or pline[0] == '#': continue
        pline = pline.split()

        pdgId   = int(pline[0])
        status  = int(pline[1])
        mother1 = int(pline[2])
        mother2 = int(pline[3])
        color1  = int(pline[4])
        color2  = int(pline[5])
        px = float(pline[ 6])
        py = float(pline[ 7])
        pz = float(pline[ 8])
        e  = float(pline[ 9])
        m  = float(pline[10])
        ctau = float(pline[11])
        spin = float(pline[12])

        #if status != 2 and status != 1: continue
        if status != 1 : continue
        #if status != 2 : continue

        absPdgId = abs(pdgId)
        candLVec = TLorentzVector(px, py, pz, e)
        pt = candLVec.Pt()

        fill(hPt, pt)
        fill(hEta, candLVec.Eta())

        if absPdgId == 6:
            nTquark += 1
            fill(hPtTquark, pt)
            if status == 1:
                nTopHawking += 1
            elif status == 2:
                nTopRemnant += 1
        elif absPdgId == 5:
            nBquark += 1
            nJets += 1
            fill(hPtBquark, pt)
        elif absPdgId == 21:
            nGluons += 1
            nJets += 1
            fill(hPtGluons, pt)
        elif absPdgId == 22:
            nPhoton += 1
            fill(hPtPhoton, pt)
        elif absPdgId in (1,2,3,4):
            nLquark += 1
            nJets += 1
            fill(hPtLquark, pt)
        elif absPdgId in (11, 13, 15):
            nLepton += 1
            fill(hPtLepton, pt)
        elif absPdgId in (12, 100, 16):
            met += pt
        elif absPdgId == 25:
            nHiggs += 1
            fill(hPtHiggs, pt)
        else:
            nOthers += 1
            fill(hPtOthers, pt)

        if absPdgId ==25:
            fill(hPtScalar, pt)
            fill(hEnergy, e)
            nScalar += 1
        elif absPdgId in (21,22,23,24):
            fill(hPtVector, pt)
            fill(hEnergy, e)
            nVector += 1
        elif absPdgId != 39:
            fill(hPtSpinor, pt)
            fill(hEnergy, e)
            nSpinor += 1

        if pt > 50 and absPdgId not in (11, 13, 15):
            st += pt
    if met > 50: st += met

    hNJets.Fill(nJets)
    hNTquark.Fill(nTquark)
    hNTRemnant.Fill(nTopRemnant)
    hNTHawking.Fill(nTopHawking)
    hNBquark.Fill(nBquark)
    hNHquark.Fill(nBquark+nTquark)
    hNLquark.Fill(nLquark)
    hNGluons.Fill(nGluons)
    hNLepton.Fill(nLepton)
    hNPhoton.Fill(nPhoton)
    hNOthers.Fill(nOthers)
    hNHiggs.Fill(nHiggs)
    hNTquarkVsNBquark.Fill(nTquark, nBquark)

    hNScalar.Fill(nScalar)
    hNSpinor.Fill(nSpinor)
    hNVector.Fill(nVector)

    fill(hSt, st)
    fill(hMET, met)

hNs  = hNJets, hNTquark, hNBquark, hNHquark, hNLquark, hNGluons, hNLepton, hNPhoton, hNHiggs, hNOthers
hPts = hPtTquark, hPtBquark, hPtLquark, hPtGluons, hPtPhoton, hPtOthers
hPtSpin = hPtScalar, hPtSpinor, hPtVector
hNSpin = hNScalar, hNSpinor, hNVector

for h in hNs + hPts + hPtSpin + hNSpin + (hNTquarkVsNBquark, hEnergy, hSt, hPt, hEta, hMET, hBhIniMass): h.SetLineWidth(2)
for h in hNs + hPts + hPtSpin + hNSpin + (hNTquarkVsNBquark, hEnergy, hSt, hPt, hEta, hMET, hBhIniMass): h.Write()

cN = TCanvas("cN", "cN", 500, 500)
hNFrame = TH1F("hNFrame", "RS 14TeV all, 100fb^{-1};Multiplicity;Events", 15, 0, 15)
hNFrame.SetMinimum(0)
hNFrame.SetMaximum(max(x.GetMaximum() for x in hNs)*1.2)
#hNFrame.Scale(1/1000.*6.861*100)
hNFrame.Draw()
hNTquark.SetLineColor(kBlack)
hNBquark.SetLineColor(kRed)
hNHquark.SetLineColor(kBlue)
hNLquark.SetLineColor(kMagenta)
hNGluons.SetLineColor(kGreen)
hNPhoton.SetLineColor(kYellow+1)
hNLepton.SetLineColor(kGray)
hNHiggs.SetLineColor(kOrange+1)
hNTRemnant.SetLineColor(kRed)
hNTHawking.SetLineColor(kBlue)
legN = TLegend(0.65, 0.65, 0.92, 0.92)
legN.SetFillStyle(0)
legN.SetBorderSize(0)
#for h in hNTquark, hNBquark, hNGluons, hNPhoton, hNHiggs:
for h in hNTquark,hNBquark,hNLquark,hNGluons,hNLepton,hNPhoton,hNHiggs:
    h.Draw("same")
    legN.AddEntry(h, h.GetTitle(), "l")
legN.Draw()
cN1 = TCanvas("BH Mass", "BH Mass", 500, 500)
hBhIniMass.Draw()

cPt = TCanvas("cPt", "cPt", 500, 500)
cPt.SetLogy()
hPtFrame = TH1F("hPtFrame", "RS 14TeV all, 100fb^{-1};Transverse momentum p_{T} (GeV/c);Entries/40GeV/c",100, 0, 3000)
hPtFrame.GetXaxis().SetNdivisions(505)
hPtFrame.SetMinimum(0.1)
hPtFrame.SetMaximum(max(x.GetMaximum() for x in hPts))
hPtFrame.Draw()
hPtTquark.SetLineColor(kBlue)
hPtBquark.SetLineColor(kRed)
hPtLquark.SetLineColor(kMagenta)
hPtPhoton.SetLineColor(kYellow)
hPtGluons.SetLineColor(kGreen)
hPtOthers.SetLineColor(kGray)
hPtHiggs.SetLineColor(kOrange+1)
hPtLepton.SetLineColor(kGray)

hPtScalar.SetLineColor(kRed)
hPtSpinor.SetLineColor(kBlue)
hPtVector.SetLineColor(kGreen)

legPt = TLegend(0.65, 0.65, 0.92, 0.92)
legPt.SetFillStyle(0)
legPt.SetBorderSize(0)
for h in hPtTquark, hPtBquark, hPtLquark, hPtGluons, hPtPhoton, hPtLepton, hPtHiggs:
#for h in hPtBquark, hPtLquark, hPtGluons, hPtPhoton, hPtOthers:
    h.Draw("same")
    legPt.AddEntry(h, h.GetTitle(), "l")
legPt.Draw()
cHvy = TCanvas("cHvy", "cHvy", 500, 500)
hNTquarkVsNBquark.Draw("colztext")

hNTops = hNTquark, hNTRemnant, hNTHawking
for h in hNTops:h.SetLineWidth(2)
hNTopFrame.SetMaximum(max(h.GetMaximum() for h in hNTops)*1.2)
legN1 = TLegend(0.65, 0.65, 0.92, 0.92)
legN1.SetFillStyle(0)
legN1.SetBorderSize(0)
cN2 = TCanvas("cN2", "cN2", 500, 500)
hNTopFrame.Draw()
for h in hNTops:
    h.Draw("same")
    legN1.AddEntry(h,h.GetTitle(),"l")   
legN1.Draw()

legSpinPt = TLegend(0.65, 0.65, 0.92, 0.92)
legSpinPt.SetFillStyle(0)
legSpinPt.SetBorderSize(0)
cN3 = TCanvas("cN3", "cN3", 500, 500)
cN3.SetLogy()
hPtSpinFrame.SetMaximum(max(h.GetMaximum() for h in (hPtScalar,hPtSpinor,hPtVector))*1.2)
hPtSpinFrame.Draw()
for h in hPtScalar, hPtSpinor, hPtVector:
    h.Draw("same")
    legSpinPt.AddEntry(h,h.GetTitle(),"l")
legSpinPt.Draw()

hNSpinFrame.SetMinimum(0)
hNSpinFrame.SetMaximum(max(x.GetMaximum() for x in hNSpin)*1.2)
hNScalar.SetLineColor(kRed)
hNSpinor.SetLineColor(kBlue)
hNVector.SetLineColor(kGreen)

legSpinN = TLegend(0.65, 0.65, 0.92, 0.92)
legSpinN.SetFillStyle(0)
legSpinN.SetBorderSize(0)
cN4 = TCanvas("cN4", "cN4", 500, 500)
hNSpinFrame.Draw()
for h in hNSpin:
    h.Draw("same")
    legSpinN.AddEntry(h,h.GetTitle(),"l")
legSpinPt.Draw()

hEnergy.SetLineWidth(2)
hEnergy.Scale(1/(hEnergy.Integral()))
cN5 = TCanvas("cN5", "cN5", 500, 500)
cN5.SetLogy()
hEnergy.Draw()

