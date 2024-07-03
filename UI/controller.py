import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._currentCountry = None


    def handleCalcola(self, e):
        year = self._view._txtAnno.value

        try:
            yearN = int(year)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Perfavore inserire un valore numerico nel campo"))
            self._view.update_page()
            return

        if yearN < 1816 or yearN > 2016:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Please provide a value between 1816 and 2016. "))
            self._view.update_page()
            return

        #se sono qui vuol dire che rispetto il range dell'anno
        self._model.buildGraph(yearN)

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumCompConnesse()} componenti connesse."))
        self._view._txt_result.controls.append(ft.Text("Di seguito il dettaglio dei nodi:"))

        for n in self._model.getNodes():
            self._view._txt_result.controls.append(
                ft.Text(f"{n} -- {self._model.getNumConfinanti(n)} vicini."))

        self._view._ddStato.disabled = False
        self._view._btnRaggiungibili.disabled = False

        self._fillDD()

        self._view.update_page()


    def _fillDD(self):
        allStati= self._model.getNodes()

        for s in allStati:
            self._view._ddStato.options.append(ft.dropdown.Option(text=s.StateNme,
                                                                  data=s,
                                                                  on_click=self._read_DD_Stato))


    def _read_DD_Stato(self, e):
        print("read_DD_Stato called ")
        if e.control.data is None:
            self._currentCountry = None
        else:
            self._currentCountry = e.control.data

        print(self._currentCountry)

    def handleRaggiungibili(self, e):
        raggiungibili = self._model.getRaggiungibiliRecursive(self._currentCountry)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Da {self._currentCountry} è possibile raggiungere a piedi {len(raggiungibili)} stati: "))
        for r in raggiungibili:
            self._view._txt_result.controls.append(
                ft.Text(f"{r}"))

        self._view.update_page()


