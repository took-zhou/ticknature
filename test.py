from nature_analysis.dominant import dominant

dominant.paramInput['dataRootPath'] = '/share/baidunetdisk/reconstruct/tick/DCE/DCE/c2105'
dominant.paramInput['duration']['begin'] = '2021-01-01'
dominant.paramInput['duration']['end'] = '2121-03-01'
result = dominant.genConfidence()
print(result)