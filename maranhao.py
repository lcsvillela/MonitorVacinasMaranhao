import requests
import json
from unidecode import unidecode

class Maranhao:
    def __init__(self):
        self.__token = (
            requests.get(
                "https://painel-covid19.saude.ma.gov.br/main-es2015.1fd5ebecf22be55d7c2e.js"
            )
            .content.decode()
            .split('"')[5449]
        )
        self.__headers = {"Authorization": f"Bearer {self.__token}"}
        self.__endpoint = {
            "todas_cidades": "https://painel-covid19-back.saude.ma.gov.br/v1/covid19/municipios/vacinas/resumo",
            "cidade_detalhada": "https://painel-covid19-back.saude.ma.gov.br/v1/covid19/municipios/vacinas/",
        }
        self.__codigo_ibge = []
        self.__data = {}

    def start(self):
        self.get_cidades_ibge()
        data = self.get_cidade()
        self.save(data)

    def make_request(self, url):
        return json.loads(requests.get(url, headers=self.__headers).content)

    def get_cidades_ibge(self):
        cidades = self.make_request(self.__endpoint["todas_cidades"])
        for cidade in cidades:
            self.__codigo_ibge.append(cidade["codigo_ibge"])

    def save(self, data):
        for _data in data:
            city = unidecode(_data["prefeitura"]).replace(" ", "_")
            file = open(f"{city}.json", "w")
            file.write(json.dumps(_data))
            file.close()

    def get_cidade(self):
        _data = []
        for codigo in self.__codigo_ibge:
            cidade = self.make_request(
                self.__endpoint["cidade_detalhada"] + str(codigo)
            )
            _data.append({
                "prefeitura": cidade["municipio"],
                "pupulacao-12+": cidade["populacao_vacina_12_17"]
                + cidade["populacao_vacina_18"],
                "doses-imunizacao": "8.658",
                "cobertura-populacional": round(
                    cidade["cobertura_populacional"] * 100, 2
                ),
                "doses-distribuidas-total": cidade["doses_recebidas"],
                "doses-aplicadas-total": cidade["doses_aplicadas"],
                "cobertura-de-doses-aplicadas": round(
                    cidade["cobertura_geral"] * 100, 2
                ),
                "doses-distribuidas-tipo": {
                    "coronavac": {
                        "1a_dose": cidade["vacinas"][0]["doses_recebidas_d1"],
                        "2a_dose": cidade["vacinas"][0]["doses_recebidas_d2"],
                        "dr-cv": cidade["vacinas"][0]["doses_recebidas_d3"],
                        "total-recebidas-cv": cidade["vacinas"][0][
                            "doses_recebidas_total"
                        ],
                    },
                    "astrazeneca": {
                        "1a_dose": cidade["vacinas"][1]["doses_recebidas_d1"],
                        "2a_dose": cidade["vacinas"][1]["doses_recebidas_d2"],
                        "dr-az": cidade["vacinas"][1]["doses_recebidas_d3"],
                        "total-recebidas-az": cidade["vacinas"][1][
                            "doses_recebidas_total"
                        ],
                    },
                    "pfizer": {
                        "1a_dose": cidade["vacinas"][2]["doses_recebidas_d1"],
                        "2a_dose": cidade["vacinas"][2]["doses_recebidas_d2"],
                        "dr-pfz": cidade["vacinas"][2]["doses_recebidas_d3"],
                        "total-recebidas-pf": cidade["vacinas"][2][
                            "doses_recebidas_total"
                        ],
                    },
                    "janssen": {"du": cidade["vacinas"][3]["doses_recebidas_total"]},
                },
                "doses-aplicadas-tipo": {
                    "coronavac": {
                        "1a_dose": cidade["vacinas"][0]["doses_aplicadas_d1"],
                        "2a_dose": cidade["vacinas"][0]["doses_aplicadas_d2"],
                        "dr-cv": cidade["vacinas"][0]["doses_aplicadas_d3"],
                        "total-aplicada-cv": cidade["vacinas"][0][
                            "doses_aplicadas_total"
                        ],
                    },
                    "astrazeneca": {
                        "1a_dose": cidade["vacinas"][1]["doses_aplicadas_d1"],
                        "2a_dose": cidade["vacinas"][1]["doses_aplicadas_d2"],
                        "dr-az": cidade["vacinas"][1]["doses_aplicadas_d3"],
                        "total-aplicada-az": cidade["vacinas"][1][
                            "doses_aplicadas_total"
                        ],
                    },
                    "pfizer": {
                        "1a_dose": cidade["vacinas"][2]["doses_aplicadas_d1"],
                        "2a_dose": cidade["vacinas"][2]["doses_aplicadas_d2"],
                        "dr-pfz": cidade["vacinas"][2]["doses_aplicadas_d3"],
                        "total-aplicada-pfz": cidade["vacinas"][2][
                            "doses_aplicadas_total"
                        ],
                    },
                    "janssen": {"du": cidade["vacinas"][3]["doses_aplicadas_total"]},
                },
                "cobertura-aplicadas-tipo": {
                    "coronavac": {
                        "1a_dose": cidade["vacinas"][0]["cobertura_d1"],
                        "2a_dose": cidade["vacinas"][0]["cobertura_d2"],
                        "dr-cv": cidade["vacinas"][0]["cobertura_d3"],
                        "total-cobertura-aplicada-cv": cidade["vacinas"][0][
                            "cobertura_total"
                        ],
                    },
                    "astrazeneca": {
                        "1a_dose": cidade["vacinas"][1]["cobertura_d1"],
                        "2a_dose": cidade["vacinas"][1]["cobertura_d2"],
                        "dr-az": cidade["vacinas"][1]["cobertura_d3"],
                        "total-cobertura-aplicada-az": cidade["vacinas"][1][
                            "cobertura_total"
                        ],
                    },
                    "pfizer": {
                        "1a_dose": cidade["vacinas"][2]["cobertura_d1"],
                        "2a_dose": cidade["vacinas"][2]["cobertura_d2"],
                        "dr-pfz": cidade["vacinas"][2]["cobertura_d3"],
                        "total-cobertura-aplicada-pfz": cidade["vacinas"][2][
                            "cobertura_total"
                        ],
                    },
                    "janssen": {"du": cidade["vacinas"][3]["cobertura_total"]},
                },
                "grupo_vacina": {
                    "coronavac": {
                        "doses_recebidas_coronavac_d2_indigena": cidade["vacinas"][0][
                            "doses_aplicadas"
                        ][0],
                        "doses_recebidas_coronavac_d3_indigena": cidade["vacinas"][0][
                            "doses_aplicadas"
                        ][1],
                    },
                    "astrazeneca": {
                        "doses_recebidas_coronavac_d2_indigena": cidade["vacinas"][1][
                            "doses_aplicadas"
                        ][0],
                        "doses_recebidas_coronavac_d3_indigena": cidade["vacinas"][1][
                            "doses_aplicadas"
                        ][1],
                    },
                    "pfizer": {
                        "doses_recebidas_coronavac_d2_indigena": cidade["vacinas"][2][
                            "doses_aplicadas"
                        ][0],
                        "doses_recebidas_coronavac_d3_indigena": cidade["vacinas"][2][
                            "doses_aplicadas"
                        ][1],
                    },
                },
            })
        
        return _data


Maranhao().start()
