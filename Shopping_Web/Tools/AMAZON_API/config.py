'''
Created on 2012-8-14
@content:amazon api config
@author: zxb
'''

#define api exception
EXCEPTION_NUM ={
                "ItemSearchException" : "40000"
                }

#Exception log file address
import os
BASE_LOG = os.path.join(os.path.dirname(__file__), "base_exception.log").replace('\\','/')
UNKNOWN_LOG = os.path.join(os.path.dirname(__file__), "uknown.log").replace('\\','/')

#API PATT
'''
Ancestors_START = "<Ancestors>"
Ancestors_END = "</Ancestors>"
BrowseNodeId_PATT = "<BrowseNodeId>(.*?)</BrowseNodeId>"
BrowseNode_PATT = "<BrowseNode>(.*)</BrowseNode>"
Ancestors_PATT = "<Ancestors>(.*)</Ancestors>"
NAME_PATT = "<Name>(.*?)</Name>"
IS_CATEGORY_ROOT = "<IsCategoryRoot>(.*?)</IsCategoryRoot>"
    '''

#API function configure
LOCALE = 'us'
ASSOCIATE_TAG = 'Version="2010-12-01"'
ACCESS_KEY_ID = [
    "AKIAIK6QCUBLIFFRPSPA", "AKIAIEH6LNUK425Y7Q2Q", "AKIAJDZNROKLVJKUCI3Q", "AKIAIGNDPDGRS4QFNKJA",
    "AKIAIO35ODXH6KSCGHEQ", "AKIAJLP7FULC4DHGHTRA", "AKIAJQWGOK3GT64YEVUA", "AKIAI5G5JMCZTPPU5BVA",
    "AKIAIH4XYL6PRFN3OHCA", "AKIAJLQU44TAUOR2ATUA", "AKIAJ4GMCCCQUV4TS5ZQ", "AKIAIYZR5YDBUNINHW4A",
    "AKIAJ4YAHRAVB5A6XMSA", "AKIAJLRGLSQAR2DAHX2A", "AKIAIAHJLZ25OOBGIHEQ","AKIAJODO3EBT6OTMZBDA",
    "AKIAJOJEYRHBGOXV6C4A","AKIAJQ4QWRPI3437W2YQ",  "AKIAJF4RVJI57Y5CJFTQ","AKIAIQWTSSFPM6F36HSA",
    "AKIAIU6PU2EITQXB2PTA","AKIAILUTCTZ7OYFLAVTA",  "AKIAJJUA3YRNNXBNG3JA","AKIAIIZHYX52IEM757SA",
    "AKIAJ7RNMZPI7CZ4SZZA","AKIAINEXL7ECLQOS2MKA",  "AKIAID7EQCA2JIQWPFQA","AKIAJ4JYQLHTWDIY5BMQ",
    "AKIAJ2LFAUZZAQSIJ2CQ","AKIAJLE6L62NGFVLJDIA"
                     ]
SECRET_ACCESS_KEY = [
    "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", "QqBejVRxyQU4ydefT0WHzvf/HKNwasoCk583qZZf",
    "SftKU70LhXFT8nnkt0efta845Lo5C4vFkiM7fiGT", "phs/FruDrwPMXKqPfDRExOqXAeiXjli0GIse7eG4",
    "b9gTPlw23p46kb1719hhnxa1rB2JdaDFLjHXzyxK", "+3xyKrpe6J1bWIXNsqzl74FABQjVoMqD3a9d3gjL",
    "VTit0mCnvc9Kb+t2rCc6RvhuZDILvvZTLfmM/5ss", "m24TTHYF6xq2XWkaRrxCGRVPE9zdJmevIP8rBQY9",
    "vGnrDmhhhHWMRxv44U/itYMNbVUMdxKhv/Jy1Y4r", "7U6ZYtvg8+H4uHmX6GqVVJRHHUjlv9JrRNVyqXEs",
    "2bzVtcjzrrJNmK+aegXCqEOFF9i7z0VmgEcB/6JD", "L99ZCVxK2+1hj5ENMFzgQgJCYGRlTbwc4pxLBj6r",
    "1f+lsRmRWTcAZ0nBO1VmddbX0bnjJ0lC1v3kn7fJ", "g01XrWzOd0aawqhUIWVWT8qF7LgdwjlaZobPJK3P",
    "dwuvlTagw89XbKh7Z2kJHvf0iO5PAJX2z9MrHAyn", "3SpWghDaX7w3vaLGadcFpdl14YHO+fByggNEfAcM",
    "CDukFgMlCf8f43YzM5vkmZduVY2KZ4qV5muxGxOt", "5AXyllIiUM1tTdNqjTMfITwLH3Q36zRPygm8gBQK",
    "2/Fy12c8ArZMH1VmxYDzSgYdQrPRL7ebilSkRYX6", "zfR7f7SC5mW2dvlp5HuNHq5cTnUQaOWrQ3clTpdM",
    "x3+buQrzOtcssayyobXkFuLFn4+GJpsKEzLPG98R", "rerTdWAVXsflW0ecaMcv/E9U0Ul/pOm+75y1hWjE",
    "8dCzgMWYd6pkq+tJI/+zvfR+rpyDFqps53oagCL8", "2vDLb9/lOB3900RgRsAoIK7bHEscj6ixV2E3Z/+g",
    "sTesLlNQK6sWe7ebaxfns+GBSHrIffS6bhOE1b/y", "fQg5qE7ARMsfZIBMHNOD0F6T8SiQ4RvNVDKVTv1a",
    "NwmaPfgSAiE4cC+UQbASZ/KxFKp+oKMT/dUKPr0n", "PJ5D8WKtXfKOijvhBDoGFI0r8fJMnSmBCatvvefl",
    "GOdwJkXi5CuezGnKjytdaGs7Vf291VcjkyW2GXPO", "gIttrmlGWbm8HrIMnL9DCquGdM7t70S1YiaW02ll"
                     ]