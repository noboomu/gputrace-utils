#!/usr/bin/env python

import sys

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

names = sys.stdin.readline()
values = sys.stdin.readline()

names = names.split(';');
values = values.split(';');
 

currentName = None

currentValues = None

results = {};

for idx in range(0,len(names)):
    name = names[idx]
    name = name.split('[')[0]
    if currentName != name and currentValues != None:
        swiftType = 'Float'
        if len(currentValues) % 4 == 0:
            swiftType = 'simd_float4x4'
            currentValues = list(splitArray(currentValues,4))
            if len(currentValues) == 1:
                currentValues = currentValues[0]
                swiftType = 'float4'
        elif len(currentValues) % 3 == 0:
            swiftType = 'simd_float3x3'
            currentValues = list(splitArray(currentValues,3))
            if len(currentValues) == 1:
                currentValues = currentValues[0]
                swiftType = 'float3'
        elif len(currentValues) == 2:
            swiftType='float2' 
        results[currentName]={'value':currentValues,'type':swiftType}
        currentValues = []
        currentName = name
    elif currentName == None:
        currentName = name
        currentValues = []
    currentValues.append(values[idx])
 
swiftResults = ""

for key, record in results.iteritems():

     
    name = capitalizeName(key)
    values = record['value']

    swiftResults = swiftResults + "\nvar " + name + " : " + record['type'] + " = " + record['type'] + "("

    name = capitalizeName(key)

    if record['type'] == 'Float':
        swiftResults = swiftResults + str(float(values[0])) + ")\n"
    elif record['type'] == 'float2':
        swiftResults = swiftResults + str(float(values[1])) + "," + str(float(values[1])) + ")\n"
    elif record['type'] == 'float3':
        swiftResults = swiftResults + str(float(values[0])) + "," + str(float(values[1])) + "," + str(float(values[2])) + ")\n"
    elif record['type'] == 'float4':
        swiftResults = swiftResults + str(float(values[0])) + "," + str(float(values[1])) + "," + str(float(values[2])) + "," + str(float(values[3])) + ")\n"
    elif record['type'] == 'simd_float4x4':
        swiftResults += '\n'
        for idx in range(0,len(values)):
            value = values[idx]
            swiftResults =  swiftResults + indentString + 'float4(' + str(float(value[0])) + "," + str(float(value[1])) + "," + str(float(value[2])) + "," + str(float(value[3])) + ")"
            if idx < len(values) -1:
                swiftResults += ',\n'
            else:
                swiftResults += '\n'

        swiftResults += ')'

print swiftResults