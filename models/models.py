Operadora = db.define_table("portabilidade_operadora",
    Field("id"),
    Field("nome_ope"),
    format="%(nome_ope)s",
    migrate=False)

Log_portabilidade = db.define_table("log_portabilidade",
	Field("id"),
    Field("data_port"),
    Field("origem"),
    Field("destino"),
    Field("operadora", db.portabilidade_operadora),
    Field("tipo_consulta"),
	migrate=False)

Portabilidade = db.define_table("portabilidade",
	Field("id"),
    Field("data_port"),
    Field("numero"),
    Field("cod_operadora"),
    Field("nome_operadora"),
    migrate=False)

Blacklist = db.define_table("port_blacklist",
    Field("id"),
    Field("numero"),
    Field("descricao"),
    Field("operadora", db.portabilidade_operadora),
    #format="%(operadora)s",
    migrate=False)






