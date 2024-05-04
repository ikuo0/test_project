
import dataclasses
import typing

@dataclasses.dataclass
class ResultLog:
    resultCode: int
    resultMessage: str
    def toString(self):
        return "code={}, message={}".format(self.resultCode, self.resultMessage)

class ResultLogger:
    def __init__(self, resultLogList: typing.List[ResultLog]=[]):
        self.resultLogList = resultLogList
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.resultLogList.append(ResultLog(resultCode=1, resultMessage=str(exc_value)))
            return True # 例外を発生させない
        else:
            self.resultLogList.append(ResultLog(resultCode=0, resultMessage="OK"))
    
    def getResultLogList(self):
        return self.resultLogList
    
    def isAnyError(self):
        isError: bool = True if any(resultLog.resultCode != 0 for resultLog in self.resultLogList) else False
        return isError

    def dumps(self):
        strArray = [resultLog.toString() for resultLog in self.resultLogList]
        dumpString = "\n".join(strArray)
        return dumpString


def function3(resultLogList: typing.List[ResultLog]):
    with ResultLogger(resultLogList=resultLogList) as resultLogger:
        print("function3")

def function2(resultLogList: typing.List[ResultLog]):
    with ResultLogger(resultLogList=resultLogList) as resultLogger:
        print("function2")
        raise Exception("function2 Error!")
        function3(resultLogList=resultLogList)

def function1(resultLogList: typing.List[ResultLog]):
    with ResultLogger(resultLogList=resultLogList) as resultLogger:
        print("function1")
        function2(resultLogList=resultLogList)

def functionA(resultLogList: typing.List[ResultLog]):
    with ResultLogger(resultLogList=resultLogList) as resultLogger:
        print("functionA")

def functionB(resultLogList: typing.List[ResultLog]):
    with ResultLogger(resultLogList=resultLogList) as resultLogger:
        print("functionB")
        raise Exception("functionB Error!")

def functionC(resultLogList: typing.List[ResultLog]):
    with ResultLogger(resultLogList=resultLogList) as resultLogger:
        print("functionC")


def main():
    with ResultLogger() as resultLogger:
        resultLogList = resultLogger.getResultLogList()
        function1(resultLogList=resultLogList)
        functionA(resultLogList=resultLogList)
        functionB(resultLogList=resultLogList)
        functionC(resultLogList=resultLogList)
        if resultLogger.isAnyError():
            print("ERROR")
            print(resultLogger.dumps())
        else:
            print("OK")

if __name__ == "__main__":
    main()
#
