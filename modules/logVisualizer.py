import glob


def logVisualizer(logsDir: str, flag: str) -> None:

  files = glob.glob(f"{logsDir}/*.log")
  nodesFiles = glob.glob(f"{logsDir}/nodo*.log")
  logs = []
  genTxsLog = []
  nodesLog = []

  for f in files:
    with open(f) as file:
      lines = file.readlines()
      logs.extend([ line for line in lines ])

  for f in nodesFiles:
    with open(f, "r+") as file:
      lines = file.readlines()
      nodesLog.extend([ line for line in lines ])

  with open(f"{logsDir}/genTransac.log", "r+") as file:
    genTxsLog = (file.readlines())

  if flag == "-mt": __parallel(logs, genTxsLog, nodesLog)
  elif flag == "-mg": __sequential(logs)
  else:
    print("Modos permitidos: visualizador paralelo(-mt) o secuencial(-mg)")


def __sequential(logs: list[str]) -> None:
  
  logs.sort()
  for l in logs:
    print(l)


def __parallel(logs: list[str], genTxsLog: list[str], nodesLog: list[str]) -> None:
  pass
