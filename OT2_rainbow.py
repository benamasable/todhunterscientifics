from opentrons import protocol_api
import csv

#opentrons api metadata
metadata = {'apiLevel': '2.12'}

#PSEUDOCODE
#start
#
#load reagents.csv
#
#pick up a P1000 pipet tip
#for j in reagent_columns:
#    sum=0
#    for i in reagent_rows:
#        sum += (i,j)
#    move to tube rack
#    pipet up (500-sum) uL water from 50mL conical tube
#    move to output plate (a 24-well plate)
#    dispense pipet contents into well j
#trash pipet tip
#
#for i in reagent_rows:
#    pick up a P20 pipet tip
#    for j in reagent_columns:
#        move to input plate (a 96-well plate)
#        pipet up (i,j) uL from input plate at well i
#        move to output plate (a 24-well plate)
#        dispense pipet contents into well j (leave an air gap when dispensing)
#    trash pipet tip
#
#for j in reagent_columns:
#    pick up a P1000 pipet tip
#    move to output plate (a 24-well plate)
#    mix contents at well j by pipetting 250uL up/down 10 times
#    trash pipet tip
#
#end

#load reagents.csv
#color order is R Y G B
f = open('reagents.csv')
drops_r = []
drops_y = []
drops_g = []
drops_b = []
drops_w = []

print('!! Reading reagents.csv')
csv_reader = csv.reader(f, delimiter='\t') #and you call them comma-separated value files... despite the fact that they are obviously tab delimited
rowcount = 0
for row in csv_reader:
    rowcount += 1
    if rowcount > 1:    #ignore first row
        columncount = 0
        for x in row:
            columncount += 1
            if columncount > 1: # ignore first column
                if x == '':
                    foo = 0
                else:
                    foo = int(x)
 
                #write read number to appropriate array
                # apparently python doesn't have a real case select
                if rowcount == 2: #red
                    drops_r.append(foo)
                if rowcount == 3: #yellow
                    drops_y.append(foo)
                if rowcount == 4: #green
                    drops_g.append(foo)
                if rowcount == 5: #blue
                    drops_b.append(foo)                

#print('!! jsut kidding, im setting these manually')
#drops_r = [20, 8, 4, 0, 0, 0, 0, 14, 4, 0, 0, 0, 5, 1, 0, 0, 3, 5, 0, 10, 18, 1, 20, 0]
#drops_y = [0, 8, 10, 20, 0, 6, 0, 0, 0, 3, 4, 0, 0, 3, 6, 0, 17, 20, 0, 0, 0, 1, 20, 0]
#drops_g = [0, 0, 0, 0, 20, 12, 0, 0, 0, 1, 3, 1, 0, 0, 14, 15, 0, 1, 10, 5, 1, 1, 20, 0]
#drops_b = [0, 0, 0, 0, 0, 2, 20, 6, 20, 0, 0, 4, 1, 0, 0, 5, 0, 0, 2, 2, 1, 1, 20, 0]

#determine water amount                
print('!! Calculating water amounts')
columncount = 0
for x in drops_r:
    drops_w.append(500 - (drops_r[columncount] + drops_y[columncount] + drops_g[columncount] + drops_b[columncount]))
    columncount += 1

print(drops_r)    
print(drops_y)
print(drops_g)
print(drops_b)
print(drops_w)
            
def run(protocol: protocol_api.ProtocolContext):
    tiprackbig = protocol.load_labware('opentrons_96_tiprack_1000ul', 1)
    tipracksmall = protocol.load_labware('opentrons_96_tiprack_20ul', 2)
    
    inputplate = protocol.load_labware('corning_96_wellplate_360ul_flat', 3)
    outputplate = protocol.load_labware('corning_24_wellplate_3.4ml_flat', 4)
    inputwater = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 5)
    
    pipettebig = protocol.load_instrument('p1000_single', tip_racks=[tiprackbig], mount='left')
    pipettesmall = protocol.load_instrument('p20_single_gen2', tip_racks=[tipracksmall], mount='right')
    
    #first load the water
    print('!! Sending commands to transfer water')
    pipettebig.pick_up_tip()
    columncount = 0
    for x in drops_w:
        pipettebig.aspirate(x, inputwater['A1'])
        pipettebig.dispense(x, outputplate.wells()[columncount]) #default position
        pipettebig.blow_out() #squirt
        columncount += 1
    pipettebig.drop_tip()
    
    #now do the colors
    print('!! Sending commands to transfer red')
    columncount = 0
    pipettesmall.pick_up_tip()
    for x in drops_r:
        if x > 0:
            pipettesmall.aspirate(x, inputplate['A1'])
            pipettesmall.dispense(x, outputplate.wells()[columncount].bottom(z=5)) #5mm above bottom
            pipettesmall.blow_out() #spurt
        columncount += 1
    pipettesmall.drop_tip()

    print('!! Sending commands to transfer yellow')
    columncount = 0
    pipettesmall.pick_up_tip()
    for x in drops_y:
        if x > 0:
            pipettesmall.aspirate(x, inputplate['A2'])
            pipettesmall.dispense(x, outputplate.wells()[columncount].bottom(z=5))
            pipettesmall.blow_out() #poot
        columncount += 1
    pipettesmall.drop_tip()
    
    print('!! Sending commands to transfer green')
    columncount = 0
    pipettesmall.pick_up_tip()
    for x in drops_g:
        if x > 0:
            pipettesmall.aspirate(x, inputplate['A3'])
            pipettesmall.dispense(x, outputplate.wells()[columncount].bottom(z=5))
            pipettesmall.blow_out() #frrp
        columncount += 1
    pipettesmall.drop_tip()
    
    print('!! Sending commands to transfer blue')
    columncount = 0
    pipettesmall.pick_up_tip()
    for x in drops_b:
        if x > 0:
            pipettesmall.aspirate(x, inputplate['A4'])
            pipettesmall.dispense(x, outputplate.wells()[columncount].bottom(z=5))
            pipettesmall.blow_out() #splot
        columncount += 1
    pipettesmall.drop_tip()
    
    #mix em up
    print('!! Sending commands to mix colors')
    columncount = 0
    for x in drops_w:
        pipettebig.pick_up_tip()
        pipettebig.mix(10,100,outputplate.wells()[columncount])
        pipettebig.blow_out() #fwoo
        pipettebig.drop_tip()
        columncount += 1