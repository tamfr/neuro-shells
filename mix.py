# -*- coding: utf-8 -*-
"""
Created on Wed May 15 18:10:54 2013

@author: Mott
"""
from collections import OrderedDict
class mix:
    def __init__(self):        
        pass         
    def define(self):
        self.PDRa = float(raw_input('Desired PPF:DEF ratio antecedent? (e.g. enter 1.5 if ratio is 1.5:1) '))
        self.PDRc = float(raw_input('Desired PPF:DEF ratio consequent? (e.g. enter 2 if ratio is 3:2) '))
        self.pB = float(raw_input('%BAPO? '))/100
        self.pH = float(raw_input('%HMB? '))/100
        self.pT = float(raw_input('%TiO2? '))/100
        self.pI = float(raw_input('%I784? '))/100 
    def label(self,text):
        self.label = text
    def create(self):
        self.BM = float(raw_input('What is the mass of your beaker? ')) # Mass of beaker mix will reside in.
        self.TM = float(raw_input('What is the desired final mass of the new mixture? ')) # Desired mass of all combined ingredients.
        self.sPDRa = float(raw_input('Ratio antecedent of source PPF:DEF mxiture? (e.g if 3:1, then enter 3) ')) # Source PPF:DEF antecedent of the PPF/DEF mixture that the new mix will be created from.
        self.sPDRc = float(raw_input('Ratio consequent of source PPF:DEF mxiture? (e.g if 3:1, then enter 1) ')) # Source PPF:DEF consequent of the PPF/DEF mixture that the new mix will be created from.    
        massPPF2DEF = self.TM/(1 + self.pB + self.pH + self.pT + self.pI)
        DEF_factor = (1-(self.sPDRc/self.sPDRa)/(self.PDRc/self.PDRa))/(1+self.PDRa/self.PDRc)
        print '\n---------- Ingredients to ADD ----------\n'        
        print '     DEF to add: %s grams ' % (round(DEF_factor*massPPF2DEF,3))
        print '     BAPO to add: %s grams ' % (round(self.pB*massPPF2DEF,3))
        print '     I784 to add: %s grams ' % (round(self.pI*massPPF2DEF,3))
        print '     HMB to add: %s grams ' % (round(self.pH*massPPF2DEF,3))
        print '     %s:%s PPF:DEF to add: %s grams ' % (self.sPDRa,self.sPDRc,(round((1-DEF_factor)*massPPF2DEF,3)))
        print '     TiO2 to add: %s grams ' % (round(self.pT*massPPF2DEF,3))
    def update(self):
        self.RM = float(raw_input('\nWhat is the current mass of the remaining mixture and beaker? '))
        self.nPDRa = float(raw_input('Desired PPF:DEF ratio antecedent? (only enter antecedent, e.g. enter 1.5 if ratio is 1.5:1) '))
        self.nPDRc  = float(raw_input('Desired PPF:DEF ratio consequent? (only enter consequent, e.g. enter 1 if ratio is 1.5:1) '))
        self.npB = float(raw_input('%BAPO? '))/100
        self.npH = float(raw_input('%HMB? '))/100
        self.npT = float(raw_input('%TiO2? '))/100
        self.npI = float(raw_input('%I784? '))/100
        initialInputs = {'BAPO':self.pB,'HMB':self.pH,'TiO2':self.pT,'I784':self.pI}       
        newInputs = {'BAPO':self.npB,'HMB':self.npH,'TiO2':self.npT,'I784':self.npI} 
        massPPF2DEF = (self.RM-self.BM)/(1 + sum(initialInputs.values()))              
        RCa = float(raw_input('PPF:DEF ratio antecedent of PPF batch you\'re using for the update? (e.g. enter 1.5 if ratio is 1.5:1) ')) if self.nPDRa/self.nPDRc > self.PDRa/self.PDRc else 0
        RCc = float(raw_input('PPF:DEF ratio consequent of PPF batch you\'re using for the update? (e.g. enter 2 if ratio is 3:2) ')) if self.nPDRa/self.nPDRc > self.PDRa/self.PDRc else 1           
        MC = massPPF2DEF*(RCa+RCc)/(self.PDRa+self.PDRc)*(self.PDRa-self.PDRc*self.nPDRa/self.nPDRc)/(RCc*self.nPDRa/self.nPDRc-RCa)
        unOrdered = {}        
        for i in initialInputs:
            unOrdered[i] = (newInputs[i]-initialInputs[i]*massPPF2DEF/(massPPF2DEF + MC))/newInputs[i]
        massPPF2DEF = massPPF2DEF + MC
        order = OrderedDict(sorted(unOrdered.items(), key=lambda t: t[1]))      
        least = min(order, key=order.get)        
        if order[least]<0:
            add = massPPF2DEF*order[least]*-1
            print '\n---------- Ingredients to ADD ----------\n'            
            print '     %s:%s PPF:DEF to add: %s grams' % (RCa,RCc, round(add+MC,3))
            dilution = {}            
            for i in unOrdered:
                dilution[i] = (unOrdered[i]*-newInputs[i]+newInputs[i])*massPPF2DEF/(massPPF2DEF + add)
            massPPF2DEF = massPPF2DEF + add
            for i in newInputs:            
                print '     %s to add: %s grams' % (i, round(massPPF2DEF*(newInputs[i]-dilution[i]),3))
        else:
            print '\n---------- Ingredients to ADD ----------\n'            
            print '     DEF to add: %s grams' % (round(MC,3))
            for i in order:            
                print '     %s to add: %s grams' % (i,round(massPPF2DEF*order[i]*newInputs[i],3))
        self.PDRa,self.pB,self.pH,self.pT,self.pI = self.nPDRa/self.nPDRc,self.npB,self.npH,self.npT,self.npI
    def current(self):
        print '\n---------- Mixture %s ----------\n' % self.label   
        print '     %s:%s PPF:DEF' % (self.PDRa,self.PDRc)
        print '     %s%% BAPO' % self.pB
        print '     %s%% HMB' % self.pH
        print '     %s%% TiO2' % self.pT
        print '     %s%% I784' % self.pI