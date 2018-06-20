#!/usr/bin/env python

import sys
from sets import Set

indentString = '\t\t\t'

def splitArray(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def capitalizeName(parameter):
    m = ""

    parameter = parameter.replace("_",".")

    parts = parameter.split('.')

    for idx in range(0,len(parts)):
        j = parts[idx]
        if idx == 0:
            m += j
        else:
            m += j[0].upper() + j[1:] 
    return m 

def lowerCaseName(parameter):
    m = ""
    m += parameter[0].lower() + parameter[1:] 
    return m

rawNames = sys.stdin.readline()
rawValues = sys.stdin.read() 
tmpNames = rawNames.split()

names = []

nameSet = Set([])

for name in tmpNames:
    if name in nameSet:
        name = 'out' + str.capitalize(name)
    nameSet.add(name)
    names.append(name)

values = rawValues.split();

currentName = None

currentValues = None

rowLength = 0

parameterLengths = []

results = {};

parameters = []

for idx in range(0,len(names)):
    name = names[idx]
    
    if name == 'Row':
        rowLength += 1
        parameterLength = 1
        parameterType = 'Int'
    elif name == 'Offset':
        rowLength += 1
        parameterLength = 1
        parameterType = 'Int'
    elif name == 'Vertex':
        rowLength += 1
        parameterLength = 1
        parameterType = 'Int'
    elif name == 'Index':
        rowLength += 1
        parameterLength = 1
        parameterType = 'Int'
    elif 'Transform' in name:
        rowLength += 16
        parameterLength = 16
        parameterType = 'float4x4'
    elif 'excoord' in name:
        rowLength += 2
        parameterLength = 2
        parameterType = 'float2'
    elif name == 'fragmentPosition':
        rowLength += 4
        parameterLength = 4
        parameterType = 'float4'
    elif 'position' in name or 'outPosition' in name or name == 'normal':
        rowLength += 3
        parameterLength = 3
        parameterType = 'float3'
     

    name = lowerCaseName(name)
    parameters.append({'length':parameterLength,'name':name,'type':parameterType})


rows = list(splitArray(values,rowLength))

swiftResults = ""

for rowIndex, row in enumerate(rows):
    currentRowLength = 0

    rowName = ""

    for idx in range(0,len(parameters)):
        parameter = parameters[idx]

        if idx == 0:
            if parameter['name'] == 'row':
                rowName = "row" + str(rowIndex)
                swiftResults = swiftResults + "\nvar " + rowName + " = SCNNodeFrameConstantRow()\n"
            else:
                rowName = "vertex" + str(rowIndex)
                swiftResults = swiftResults + "\nvar " + rowName + " = VertexAttributeRow(\n"

        parameterValues = row[currentRowLength:currentRowLength+parameter['length']]
        currentRowLength += parameter['length']

        swiftResults = swiftResults + " " +  indentString + parameter['name'] + ": " + parameter['type'] + "("

        if parameter['type'] == 'Float':
            swiftResults = swiftResults + str(float(parameterValues[0])) + ")"
        elif parameter['type'] == 'Int' and parameter['name'] == 'offset':
            swiftResults = swiftResults + str(int(parameterValues[0],16)) + ")"
        elif parameter['type'] == 'Int':
            swiftResults = swiftResults + str(int(parameterValues[0])) + ")"
        elif parameter['type'] == 'float2':
            swiftResults = swiftResults + str(float(parameterValues[0])) + "," + str(float(parameterValues[1])) + ")"
        elif parameter['type'] == 'float3':
            swiftResults = swiftResults + str(float(parameterValues[0])) + "," + str(float(parameterValues[1])) + "," + str(float(parameterValues[2])) + ")"
        elif parameter['type'] == 'float4':
            swiftResults = swiftResults + str(float(parameterValues[0])) + "," + str(float(parameterValues[1])) + "," + str(float(parameterValues[2])) + "," + str(float(parameterValues[3])) + ")"
        elif parameter['type'] == 'float4x4':
            swiftResults += '\n'
            for valueIndex in range(0,len(parameterValues)/4):
                value = parameterValues[valueIndex*4:(valueIndex*4)+4]
                swiftResults =  swiftResults + indentString + '\tfloat4(' + str(float(value[0])) + "," + str(float(value[1])) + "," + str(float(value[2])) + "," + str(float(value[3])) + ")"
                if valueIndex < len(value) -1:
                    swiftResults += ',\n'
                else:
                    swiftResults += '\n'
            swiftResults += indentString + '\t)'
        if idx < len(parameters) -1:
            swiftResults += ',\n'
        else:
            swiftResults += '\n'
    swiftResults += indentString + ')'
    swiftResults += '\n'

print swiftResults

# for key, record in results.iteritems():

     
#     name = capitalizeName(key)
#     values = record['value']

#     swiftResults = swiftResults + "\nvar " + name + " : " + record['type'] + " = " + record['type'] + "("

#     name = capitalizeName(key)

#     if record['type'] == 'Float':
#         swiftResults = swiftResults + str(float(values[0])) + ")\n"
#     elif record['type'] == 'float2':
#         swiftResults = swiftResults + str(float(values[0])) + "," + str(float(values[1])) + ")\n"
#     elif record['type'] == 'float3':
#         swiftResults = swiftResults + str(float(values[0])) + "," + str(float(values[1])) + "," + str(float(values[2])) + ")\n"
#     elif record['type'] == 'float4':
#         swiftResults = swiftResults + str(float(values[0])) + "," + str(float(values[1])) + "," + str(float(values[2])) + "," + str(float(values[3])) + ")\n"
#     elif record['type'] == 'simd_float4x4':
#         swiftResults += '\n'
#         for idx in range(0,len(values)):
#             value = values[idx]
#             swiftResults =  swiftResults + indentString + 'float4(' + str(float(value[0])) + "," + str(float(value[1])) + "," + str(float(value[2])) + "," + str(float(value[3])) + ")"
#             if idx < len(values) -1:
#                 swiftResults += ',\n'
#             else:
#                 swiftResults += '\n'

#         swiftResults += ')'

# print swiftResults