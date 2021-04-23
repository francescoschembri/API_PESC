from pescriot import *
from pescgoogle import *

foglio = clonaFoglio("Soloq API Sheet PESC", nome_clonato = "Soloq di ClickJJ")
rows = makeSpreadSheetRowsOfPlayer("ClickJJ", 3)
appendiRigheFoglio("Soloq di ClickJJ", rows)